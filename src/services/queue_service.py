"""
Queue Service - Business logic for queue management
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from models.queue_entry import QueueEntry


class QueueService:
    """
    Service class for queue management operations.
    
    This class encapsulates all business logic related to queue management,
    including priority sorting, capacity validation, and wait time calculations.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
    """
    
    # Average service time per patient in minutes (for wait time estimation)
    AVERAGE_SERVICE_TIME = 15
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize QueueService with database manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def add_patient_to_queue(self, patient_id: int, specialization_id: int, 
                            status: int = 0) -> int:
        """
        Add a patient to the queue.
        
        Args:
            patient_id: Patient identifier
            specialization_id: Specialization identifier
            status: Priority status (0=Normal, 1=Urgent, 2=Super-Urgent)
        
        Returns:
            int: The ID of the newly created queue entry
        
        Raises:
            ValueError: If capacity is exceeded or patient is already in queue
        """
        # Validate status
        if status not in [0, 1, 2]:
            raise ValueError("Status must be 0 (Normal), 1 (Urgent), or 2 (Super-Urgent)")
        
        # Check if patient is already in this queue
        existing = self.get_active_queue_entry(patient_id, specialization_id)
        if existing:
            raise ValueError(f"Patient is already in the queue for this specialization (Position: {existing.position})")
        
        # Check capacity
        active_queue = self.get_queue(specialization_id, active_only=True)
        
        # Get specialization max capacity
        spec_query = "SELECT max_capacity FROM specializations WHERE specialization_id = %s"
        spec_result = self.db.execute_query(spec_query, (specialization_id,))
        if not spec_result:
            raise ValueError(f"Specialization with ID {specialization_id} not found")
        
        # Handle both tuple and dict results (SQLite vs MySQL)
        if isinstance(spec_result[0], dict):
            max_capacity = spec_result[0]['max_capacity']
        else:
            max_capacity = spec_result[0][0]
        
        if len(active_queue) >= max_capacity:
            raise ValueError(f"Queue is at maximum capacity ({max_capacity}). Cannot add more patients.")
        
        # Calculate position (will be updated after insert)
        position = len(active_queue) + 1
        
        # Calculate estimated wait time
        estimated_wait = self._calculate_estimated_wait_time(
            specialization_id, status, position
        )
        
        # Insert queue entry
        query = """
            INSERT INTO queue_entries 
            (patient_id, specialization_id, status, position, estimated_wait_time, joined_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        joined_at = datetime.now()
        params = (patient_id, specialization_id, status, position, estimated_wait, joined_at)
        
        self.db.execute_update(query, params)
        queue_entry_id = self.db.get_last_insert_id()
        
        # Reorder queue positions
        self._reorder_queue_positions(specialization_id)
        
        return queue_entry_id
    
    def remove_patient_from_queue(self, queue_entry_id: int, 
                                  reason: Optional[str] = None) -> bool:
        """
        Remove a patient from the queue.
        
        Args:
            queue_entry_id: Queue entry identifier
            reason: Optional reason for removal
        
        Returns:
            bool: True if successful, False if not found
        """
        # Get queue entry
        entry = self.get_queue_entry(queue_entry_id)
        if not entry:
            return False
        
        # Update queue entry
        query = """
            UPDATE queue_entries 
            SET removed_at = %s, removal_reason = %s
            WHERE queue_entry_id = %s
        """
        
        params = (datetime.now(), reason, queue_entry_id)
        self.db.execute_update(query, params)
        
        # Reorder remaining queue positions
        if entry.specialization_id:
            self._reorder_queue_positions(entry.specialization_id)
        
        return True
    
    def serve_patient(self, queue_entry_id: int) -> bool:
        """
        Mark a patient as served (remove from active queue).
        
        Args:
            queue_entry_id: Queue entry identifier
        
        Returns:
            bool: True if successful, False if not found
        """
        # Get queue entry
        entry = self.get_queue_entry(queue_entry_id)
        if not entry:
            return False
        
        # Update queue entry
        query = """
            UPDATE queue_entries 
            SET served_at = %s, status = 3
            WHERE queue_entry_id = %s
        """
        
        params = (datetime.now(), queue_entry_id)
        self.db.execute_update(query, params)
        
        # Reorder remaining queue positions
        if entry.specialization_id:
            self._reorder_queue_positions(entry.specialization_id)
        
        return True
    
    def get_next_patient(self, specialization_id: int) -> Optional[QueueEntry]:
        """
        Get and serve the next patient in queue (highest priority).
        
        Args:
            specialization_id: Specialization identifier
        
        Returns:
            QueueEntry object or None if queue is empty
        """
        queue = self.get_queue(specialization_id, active_only=True)
        if not queue:
            return None
        
        # Get highest priority patient (first in sorted queue)
        next_entry = queue[0]
        
        # Serve the patient
        self.serve_patient(next_entry.queue_entry_id)
        
        return next_entry
    
    def get_queue(self, specialization_id: int, active_only: bool = True) -> List[QueueEntry]:
        """
        Get all patients in queue, sorted by priority.
        
        Args:
            specialization_id: Specialization identifier
            active_only: If True, only return active entries (not served/removed)
        
        Returns:
            List of QueueEntry objects, sorted by priority (highest first)
        """
        if active_only:
            query = """
                SELECT queue_entry_id, patient_id, specialization_id, status, 
                       position, joined_at, served_at, removed_at, removal_reason, 
                       estimated_wait_time
                FROM queue_entries
                WHERE specialization_id = %s 
                  AND (removed_at IS NULL AND served_at IS NULL)
                ORDER BY status DESC, joined_at ASC
            """
        else:
            query = """
                SELECT queue_entry_id, patient_id, specialization_id, status, 
                       position, joined_at, served_at, removed_at, removal_reason, 
                       estimated_wait_time
                FROM queue_entries
                WHERE specialization_id = %s
                ORDER BY status DESC, joined_at ASC
            """
        
        results = self.db.execute_query(query, (specialization_id,))
        
        entries = []
        for row in results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                entry = QueueEntry(
                    queue_entry_id=row.get('queue_entry_id'),
                    patient_id=row.get('patient_id', 0),
                    specialization_id=row.get('specialization_id', 0),
                    status=row.get('status', 0),
                    position=row.get('position'),
                    joined_at=row.get('joined_at') if isinstance(row.get('joined_at'), datetime) else datetime.fromisoformat(row.get('joined_at')) if row.get('joined_at') else None,
                    served_at=row.get('served_at') if isinstance(row.get('served_at'), datetime) else datetime.fromisoformat(row.get('served_at')) if row.get('served_at') else None,
                    removed_at=row.get('removed_at') if isinstance(row.get('removed_at'), datetime) else datetime.fromisoformat(row.get('removed_at')) if row.get('removed_at') else None,
                    removal_reason=row.get('removal_reason'),
                    estimated_wait_time=row.get('estimated_wait_time')
                )
            else:
                entry = QueueEntry(
                    queue_entry_id=row[0],
                    patient_id=row[1],
                    specialization_id=row[2],
                    status=row[3],
                    position=row[4],
                    joined_at=row[5] if isinstance(row[5], datetime) else datetime.fromisoformat(row[5]) if row[5] else None,
                    served_at=row[6] if isinstance(row[6], datetime) else datetime.fromisoformat(row[6]) if row[6] else None,
                    removed_at=row[7] if isinstance(row[7], datetime) else datetime.fromisoformat(row[7]) if row[7] else None,
                    removal_reason=row[8],
                    estimated_wait_time=row[9]
                )
            entries.append(entry)
        
        # Update positions based on sorted order
        for idx, entry in enumerate(entries, start=1):
            if entry.position != idx:
                self._update_position(entry.queue_entry_id, idx)
                entry.position = idx
        
        return entries
    
    def get_all_queues(self, active_only: bool = True) -> Dict[int, List[QueueEntry]]:
        """
        Get queues for all specializations.
        
        Args:
            active_only: If True, only return active entries
        
        Returns:
            Dictionary mapping specialization_id to list of QueueEntry objects
        """
        if active_only:
            query = """
                SELECT queue_entry_id, patient_id, specialization_id, status, 
                       position, joined_at, served_at, removed_at, removal_reason, 
                       estimated_wait_time
                FROM queue_entries
                WHERE removed_at IS NULL AND served_at IS NULL
                ORDER BY specialization_id, status DESC, joined_at ASC
            """
        else:
            query = """
                SELECT queue_entry_id, patient_id, specialization_id, status, 
                       position, joined_at, served_at, removed_at, removal_reason, 
                       estimated_wait_time
                FROM queue_entries
                ORDER BY specialization_id, status DESC, joined_at ASC
            """
        
        results = self.db.execute_query(query)
        
        queues = {}
        for row in results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                specialization_id = row.get('specialization_id', 0)
                entry = QueueEntry(
                    queue_entry_id=row.get('queue_entry_id'),
                    patient_id=row.get('patient_id', 0),
                    specialization_id=specialization_id,
                    status=row.get('status', 0),
                    position=row.get('position'),
                    joined_at=row.get('joined_at') if isinstance(row.get('joined_at'), datetime) else datetime.fromisoformat(row.get('joined_at')) if row.get('joined_at') else None,
                    served_at=row.get('served_at') if isinstance(row.get('served_at'), datetime) else datetime.fromisoformat(row.get('served_at')) if row.get('served_at') else None,
                    removed_at=row.get('removed_at') if isinstance(row.get('removed_at'), datetime) else datetime.fromisoformat(row.get('removed_at')) if row.get('removed_at') else None,
                    removal_reason=row.get('removal_reason'),
                    estimated_wait_time=row.get('estimated_wait_time')
                )
            else:
                specialization_id = row[2]
                entry = QueueEntry(
                    queue_entry_id=row[0],
                    patient_id=row[1],
                    specialization_id=row[2],
                    status=row[3],
                    position=row[4],
                    joined_at=row[5] if isinstance(row[5], datetime) else datetime.fromisoformat(row[5]) if row[5] else None,
                    served_at=row[6] if isinstance(row[6], datetime) else datetime.fromisoformat(row[6]) if row[6] else None,
                    removed_at=row[7] if isinstance(row[7], datetime) else datetime.fromisoformat(row[7]) if row[7] else None,
                    removal_reason=row[8],
                    estimated_wait_time=row[9]
                )
            
            if specialization_id not in queues:
                queues[specialization_id] = []
            queues[specialization_id].append(entry)
        
        return queues
    
    def get_queue_entry(self, queue_entry_id: int) -> Optional[QueueEntry]:
        """
        Get a specific queue entry by ID.
        
        Args:
            queue_entry_id: Queue entry identifier
        
        Returns:
            QueueEntry object or None if not found
        """
        query = """
            SELECT queue_entry_id, patient_id, specialization_id, status, 
                   position, joined_at, served_at, removed_at, removal_reason, 
                   estimated_wait_time
            FROM queue_entries
            WHERE queue_entry_id = %s
        """
        
        result = self.db.execute_query(query, (queue_entry_id,))
        if not result:
            return None
        
        row = result[0]
        # Handle both tuple and dict results (SQLite vs MySQL)
        if isinstance(row, dict):
            return QueueEntry(
                queue_entry_id=row.get('queue_entry_id'),
                patient_id=row.get('patient_id', 0),
                specialization_id=row.get('specialization_id', 0),
                status=row.get('status', 0),
                position=row.get('position'),
                joined_at=row.get('joined_at') if isinstance(row.get('joined_at'), datetime) else datetime.fromisoformat(row.get('joined_at')) if row.get('joined_at') else None,
                served_at=row.get('served_at') if isinstance(row.get('served_at'), datetime) else datetime.fromisoformat(row.get('served_at')) if row.get('served_at') else None,
                removed_at=row.get('removed_at') if isinstance(row.get('removed_at'), datetime) else datetime.fromisoformat(row.get('removed_at')) if row.get('removed_at') else None,
                removal_reason=row.get('removal_reason'),
                estimated_wait_time=row.get('estimated_wait_time')
            )
        else:
            return QueueEntry(
                queue_entry_id=row[0],
                patient_id=row[1],
                specialization_id=row[2],
                status=row[3],
                position=row[4],
                joined_at=row[5] if isinstance(row[5], datetime) else datetime.fromisoformat(row[5]) if row[5] else None,
                served_at=row[6] if isinstance(row[6], datetime) else datetime.fromisoformat(row[6]) if row[6] else None,
                removed_at=row[7] if isinstance(row[7], datetime) else datetime.fromisoformat(row[7]) if row[7] else None,
                removal_reason=row[8],
                estimated_wait_time=row[9]
            )
    
    def get_active_queue_entry(self, patient_id: int, specialization_id: int) -> Optional[QueueEntry]:
        """
        Get active queue entry for a patient in a specific specialization.
        
        Args:
            patient_id: Patient identifier
            specialization_id: Specialization identifier
        
        Returns:
            QueueEntry object or None if not found
        """
        query = """
            SELECT queue_entry_id, patient_id, specialization_id, status, 
                   position, joined_at, served_at, removed_at, removal_reason, 
                   estimated_wait_time
            FROM queue_entries
            WHERE patient_id = %s 
              AND specialization_id = %s
              AND removed_at IS NULL 
              AND served_at IS NULL
            ORDER BY joined_at DESC
            LIMIT 1
        """
        
        result = self.db.execute_query(query, (patient_id, specialization_id))
        if not result:
            return None
        
        row = result[0]
        # Handle both tuple and dict results (SQLite vs MySQL)
        if isinstance(row, dict):
            return QueueEntry(
                queue_entry_id=row.get('queue_entry_id'),
                patient_id=row.get('patient_id', 0),
                specialization_id=row.get('specialization_id', 0),
                status=row.get('status', 0),
                position=row.get('position'),
                joined_at=row.get('joined_at') if isinstance(row.get('joined_at'), datetime) else datetime.fromisoformat(row.get('joined_at')) if row.get('joined_at') else None,
                served_at=row.get('served_at') if isinstance(row.get('served_at'), datetime) else datetime.fromisoformat(row.get('served_at')) if row.get('served_at') else None,
                removed_at=row.get('removed_at') if isinstance(row.get('removed_at'), datetime) else datetime.fromisoformat(row.get('removed_at')) if row.get('removed_at') else None,
                removal_reason=row.get('removal_reason'),
                estimated_wait_time=row.get('estimated_wait_time')
            )
        else:
            return QueueEntry(
                queue_entry_id=row[0],
                patient_id=row[1],
                specialization_id=row[2],
                status=row[3],
                position=row[4],
                joined_at=row[5] if isinstance(row[5], datetime) else datetime.fromisoformat(row[5]) if row[5] else None,
                served_at=row[6] if isinstance(row[6], datetime) else datetime.fromisoformat(row[6]) if row[6] else None,
                removed_at=row[7] if isinstance(row[7], datetime) else datetime.fromisoformat(row[7]) if row[7] else None,
                removal_reason=row[8],
                estimated_wait_time=row[9]
            )
    
    def update_patient_priority(self, queue_entry_id: int, new_status: int) -> bool:
        """
        Update patient priority and reorder queue.
        
        Args:
            queue_entry_id: Queue entry identifier
            new_status: New priority status (0, 1, or 2)
        
        Returns:
            bool: True if successful, False if not found
        """
        # Validate status
        if new_status not in [0, 1, 2]:
            raise ValueError("Status must be 0 (Normal), 1 (Urgent), or 2 (Super-Urgent)")
        
        # Get queue entry
        entry = self.get_queue_entry(queue_entry_id)
        if not entry:
            return False
        
        # Update status
        query = "UPDATE queue_entries SET status = %s WHERE queue_entry_id = %s"
        self.db.execute_update(query, (new_status, queue_entry_id))
        
        # Reorder queue positions
        if entry.specialization_id:
            self._reorder_queue_positions(entry.specialization_id)
        
        return True
    
    def get_queue_statistics(self, specialization_id: Optional[int] = None, 
                            date_range: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Get queue statistics.
        
        Args:
            specialization_id: Optional specialization ID to filter by
            date_range: Optional tuple of (start_date, end_date)
        
        Returns:
            Dictionary containing statistics
        """
        # Build query
        where_clauses = ["removed_at IS NULL AND served_at IS NULL"]
        params = []
        
        if specialization_id:
            where_clauses.append("specialization_id = %s")
            params.append(specialization_id)
        
        if date_range:
            where_clauses.append("joined_at >= %s AND joined_at <= %s")
            params.extend(date_range)
        
        where_clause = " AND ".join(where_clauses)
        
        # Get total active queue size
        query = f"SELECT COUNT(*) FROM queue_entries WHERE {where_clause}"
        result = self.db.execute_query(query, tuple(params) if params else None)
        if result:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(result[0], dict):
                total_active = result[0].get('COUNT(*)', 0)
            else:
                total_active = result[0][0]
        else:
            total_active = 0
        
        # Get status distribution
        status_query = f"""
            SELECT status, COUNT(*) 
            FROM queue_entries 
            WHERE {where_clause}
            GROUP BY status
        """
        status_result = self.db.execute_query(status_query, tuple(params) if params else None)
        status_dist = {0: 0, 1: 0, 2: 0}
        for row in status_result:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                status = row.get('status', 0)
                count = row.get('COUNT(*)', 0)
            else:
                status = row[0]
                count = row[1]
            status_dist[status] = count
        
        # Get average wait time (for served patients)
        # Calculate in Python for cross-database compatibility
        served_query = """
            SELECT joined_at, served_at
            FROM queue_entries
            WHERE served_at IS NOT NULL
        """
        served_params = []
        if specialization_id:
            served_query += " AND specialization_id = %s"
            served_params.append(specialization_id)
        
        served_results = self.db.execute_query(served_query, tuple(served_params) if served_params else None)
        
        wait_times = []
        for row in served_results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                joined = row.get('joined_at') if isinstance(row.get('joined_at'), datetime) else datetime.fromisoformat(row.get('joined_at')) if row.get('joined_at') else None
                served = row.get('served_at') if isinstance(row.get('served_at'), datetime) else datetime.fromisoformat(row.get('served_at')) if row.get('served_at') else None
            else:
                joined = row[0] if isinstance(row[0], datetime) else datetime.fromisoformat(row[0]) if row[0] else None
                served = row[1] if isinstance(row[1], datetime) else datetime.fromisoformat(row[1]) if row[1] else None
            if joined and served:
                delta = served - joined
                wait_times.append(int(delta.total_seconds() / 60))
        
        avg_wait_time = int(sum(wait_times) / len(wait_times)) if wait_times else 0
        
        # Get longest wait time (for active patients)
        active_query = f"""
            SELECT joined_at
            FROM queue_entries
            WHERE {where_clause}
        """
        active_results = self.db.execute_query(active_query, tuple(params) if params else None)
        
        longest_wait = 0
        now = datetime.now()
        for row in active_results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                joined = row.get('joined_at') if isinstance(row.get('joined_at'), datetime) else datetime.fromisoformat(row.get('joined_at')) if row.get('joined_at') else None
            else:
                joined = row[0] if isinstance(row[0], datetime) else datetime.fromisoformat(row[0]) if row[0] else None
            if joined:
                delta = now - joined
                wait_minutes = int(delta.total_seconds() / 60)
                longest_wait = max(longest_wait, wait_minutes)
        
        return {
            'total_active': total_active,
            'normal_count': status_dist[0],
            'urgent_count': status_dist[1],
            'super_urgent_count': status_dist[2],
            'average_wait_time': avg_wait_time,
            'longest_wait_time': longest_wait
        }
    
    def _calculate_estimated_wait_time(self, specialization_id: int, 
                                       status: int, position: int) -> int:
        """
        Calculate estimated wait time based on queue position and average service time.
        
        Args:
            specialization_id: Specialization identifier
            status: Priority status
            position: Position in queue
        
        Returns:
            Estimated wait time in minutes
        """
        # Get queue to count patients ahead
        queue = self.get_queue(specialization_id, active_only=True)
        
        # Count patients with higher or equal priority ahead
        patients_ahead = 0
        for entry in queue:
            if entry.status > status or (entry.status == status and entry.position < position):
                patients_ahead += 1
        
        # Estimate: patients ahead * average service time
        # Higher priority patients get faster service
        multiplier = 1.0 if status == 0 else (0.7 if status == 1 else 0.5)
        estimated = int(patients_ahead * self.AVERAGE_SERVICE_TIME * multiplier)
        
        return max(estimated, 0)
    
    def _reorder_queue_positions(self, specialization_id: int):
        """
        Reorder queue positions based on priority sorting.
        
        Args:
            specialization_id: Specialization identifier
        """
        queue = self.get_queue(specialization_id, active_only=True)
        
        # Update positions
        for idx, entry in enumerate(queue, start=1):
            if entry.position != idx:
                self._update_position(entry.queue_entry_id, idx)
    
    def _update_position(self, queue_entry_id: int, position: int):
        """
        Update position for a queue entry.
        
        Args:
            queue_entry_id: Queue entry identifier
            position: New position
        """
        query = "UPDATE queue_entries SET position = %s WHERE queue_entry_id = %s"
        self.db.execute_update(query, (position, queue_entry_id))
