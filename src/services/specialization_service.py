"""
Specialization Service - Business logic for specialization management
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from models.specialization import Specialization


class SpecializationService:
    """
    Service class for specialization management operations.
    
    This class encapsulates all business logic related to specialization management,
    including validation, data processing, and database operations.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize SpecializationService with database manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_specialization(self, specialization_data: Dict[str, Any]) -> int:
        """
        Create a new specialization record.
        
        Args:
            specialization_data: Dictionary containing specialization information.
                Required keys:
                    - name (str): Specialization name
                Optional keys:
                    - description (str): Description
                    - max_capacity (int): Maximum queue capacity (default: 10)
                    - is_active (bool): Active status (default: True)
        
        Returns:
            int: The ID of the newly created specialization record.
        
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Validation
        if not specialization_data.get('name') or not specialization_data['name'].strip():
            raise ValueError("Specialization name is required")
        
        # Check for duplicate name
        existing = self.get_specialization_by_name(specialization_data['name'].strip())
        if existing:
            raise ValueError(f"Specialization with name '{specialization_data['name'].strip()}' already exists")
        
        # Get values with defaults
        name = specialization_data['name'].strip()
        description = specialization_data.get('description')
        max_capacity = specialization_data.get('max_capacity', 10)
        is_active = specialization_data.get('is_active', True)
        
        # Validate capacity
        if max_capacity <= 0:
            raise ValueError("Maximum capacity must be greater than 0")
        if max_capacity > 1000:
            raise ValueError("Maximum capacity cannot exceed 1000")
        
        # Convert boolean to int for database
        is_active_int = 1 if is_active else 0
        
        # Build INSERT query
        query = """
            INSERT INTO specializations 
            (name, description, max_capacity, is_active)
            VALUES (%s, %s, %s, %s)
        """
        
        params = (name, description, max_capacity, is_active_int)
        
        self.db.execute_update(query, params)
        return self.db.get_last_insert_id()
    
    def get_specialization(self, specialization_id: int) -> Optional[Specialization]:
        """
        Retrieve specialization by ID.
        
        Args:
            specialization_id: Unique specialization identifier
        
        Returns:
            Specialization object or None if not found
        """
        query = "SELECT * FROM specializations WHERE specialization_id = %s"
        results = self.db.execute_query(query, (specialization_id,))
        
        if not results:
            return None
        
        return Specialization.from_dict(dict(results[0]))
    
    def get_specialization_by_name(self, name: str) -> Optional[Specialization]:
        """
        Retrieve specialization by name.
        
        Args:
            name: Specialization name
        
        Returns:
            Specialization object or None if not found
        """
        query = "SELECT * FROM specializations WHERE name = %s"
        results = self.db.execute_query(query, (name,))
        
        if not results:
            return None
        
        return Specialization.from_dict(dict(results[0]))
    
    def get_all_specializations(self, active_only: bool = False) -> List[Specialization]:
        """
        Retrieve all specializations.
        
        Args:
            active_only: If True, only return active specializations
        
        Returns:
            List of Specialization objects
        """
        if active_only:
            query = "SELECT * FROM specializations WHERE is_active = 1 ORDER BY name"
        else:
            query = "SELECT * FROM specializations ORDER BY name"
        
        results = self.db.execute_query(query)
        return [Specialization.from_dict(dict(row)) for row in results]
    
    def update_specialization(self, specialization_id: int, specialization_data: Dict[str, Any]) -> bool:
        """
        Update specialization information.
        
        Args:
            specialization_id: Specialization ID to update
            specialization_data: Dictionary with fields to update
        
        Returns:
            True if update successful, False if specialization not found
        
        Raises:
            ValueError: If validation fails
        """
        # Check if specialization exists
        existing = self.get_specialization(specialization_id)
        if not existing:
            return False
        
        # Check for duplicate name if name is being changed
        if 'name' in specialization_data:
            new_name = specialization_data['name'].strip()
            if new_name != existing.name:
                duplicate = self.get_specialization_by_name(new_name)
                if duplicate:
                    raise ValueError(f"Specialization with name '{new_name}' already exists")
        
        # Validate capacity if provided
        if 'max_capacity' in specialization_data:
            max_capacity = specialization_data['max_capacity']
            if max_capacity <= 0:
                raise ValueError("Maximum capacity must be greater than 0")
            if max_capacity > 1000:
                raise ValueError("Maximum capacity cannot exceed 1000")
        
        # Build UPDATE query dynamically
        updates = []
        params = []
        
        if 'name' in specialization_data:
            updates.append("name = %s")
            params.append(specialization_data['name'].strip())
        
        if 'description' in specialization_data:
            updates.append("description = %s")
            params.append(specialization_data.get('description'))
        
        if 'max_capacity' in specialization_data:
            updates.append("max_capacity = %s")
            params.append(specialization_data['max_capacity'])
        
        if 'is_active' in specialization_data:
            is_active = specialization_data['is_active']
            is_active_int = 1 if is_active else 0
            updates.append("is_active = %s")
            params.append(is_active_int)
        
        if not updates:
            return True  # No changes to make
        
        # Add updated_at timestamp
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        # Add specialization_id to params
        params.append(specialization_id)
        
        query = f"UPDATE specializations SET {', '.join(updates)} WHERE specialization_id = %s"
        self.db.execute_update(query, tuple(params))
        
        return True
    
    def delete_specialization(self, specialization_id: int, force: bool = False) -> bool:
        """
        Delete or deactivate a specialization.
        
        By default, this performs a soft delete (sets is_active = 0).
        Set force=True for hard delete (not recommended).
        
        Args:
            specialization_id: Specialization ID to delete
            force: If True, perform hard delete (default: False)
        
        Returns:
            True if deletion successful, False if specialization not found
        
        Raises:
            ValueError: If specialization has active patients or assigned doctors
        """
        specialization = self.get_specialization(specialization_id)
        if not specialization:
            return False
        
        if force:
            # Check if specialization has patients in queue
            queue_query = "SELECT COUNT(*) FROM queue_entries WHERE specialization_id = %s"
            queue_count = self.db.execute_query(queue_query, (specialization_id,))[0][0]
            
            if queue_count > 0:
                raise ValueError("Cannot delete specialization with patients in queue")
            
            # Check if specialization has assigned doctors
            doctor_query = "SELECT COUNT(*) FROM doctor_specializations WHERE specialization_id = %s"
            doctor_count = self.db.execute_query(doctor_query, (specialization_id,))[0][0]
            
            if doctor_count > 0:
                raise ValueError("Cannot delete specialization with assigned doctors")
            
            # Hard delete
            query = "DELETE FROM specializations WHERE specialization_id = %s"
            self.db.execute_update(query, (specialization_id,))
        else:
            # Soft delete (deactivate)
            query = "UPDATE specializations SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE specialization_id = %s"
            self.db.execute_update(query, (specialization_id,))
        
        return True
    
    def search_specializations(self, search_term: str) -> List[Specialization]:
        """
        Search specializations by name or description.
        
        Args:
            search_term: Search keyword
        
        Returns:
            List of matching Specialization objects
        """
        search_pattern = f"%{search_term}%"
        query = """
            SELECT * FROM specializations 
            WHERE name LIKE %s OR description LIKE %s
            ORDER BY name
        """
        results = self.db.execute_query(query, (search_pattern, search_pattern))
        return [Specialization.from_dict(dict(row)) for row in results]
    
    def get_specialization_statistics(self, specialization_id: int) -> Dict[str, Any]:
        """
        Get statistics for a specialization.
        
        Args:
            specialization_id: Specialization ID
        
        Returns:
            Dictionary with statistics:
                - current_queue_size: Number of patients currently in queue
                - utilization_percentage: Queue utilization (0-100)
                - is_full: Whether queue is at capacity
                - assigned_doctors_count: Number of assigned doctors
        """
        specialization = self.get_specialization(specialization_id)
        if not specialization:
            return {}
        
        # Get current queue size
        queue_query = "SELECT COUNT(*) as count FROM queue_entries WHERE specialization_id = %s"
        queue_result = self.db.execute_query(queue_query, (specialization_id,))
        if queue_result and len(queue_result) > 0:
            # Result is a list of dict-like objects or tuples
            if isinstance(queue_result[0], dict):
                current_queue_size = queue_result[0].get('count', 0)
            else:
                # It's a tuple or row object
                current_queue_size = queue_result[0][0] if len(queue_result[0]) > 0 else 0
        else:
            current_queue_size = 0
        
        # Calculate utilization
        utilization_percentage = (current_queue_size / specialization.max_capacity * 100) if specialization.max_capacity > 0 else 0
        is_full = current_queue_size >= specialization.max_capacity
        
        # Get assigned doctors count
        doctor_query = "SELECT COUNT(*) as count FROM doctor_specializations WHERE specialization_id = %s"
        doctor_result = self.db.execute_query(doctor_query, (specialization_id,))
        if doctor_result and len(doctor_result) > 0:
            if isinstance(doctor_result[0], dict):
                assigned_doctors_count = doctor_result[0].get('count', 0)
            else:
                assigned_doctors_count = doctor_result[0][0] if len(doctor_result[0]) > 0 else 0
        else:
            assigned_doctors_count = 0
        
        return {
            'specialization_id': specialization_id,
            'name': specialization.name,
            'max_capacity': specialization.max_capacity,
            'current_queue_size': current_queue_size,
            'utilization_percentage': round(utilization_percentage, 2),
            'is_full': is_full,
            'assigned_doctors_count': assigned_doctors_count,
            'is_active': specialization.is_active
        }
    
    def assign_doctor(self, specialization_id: int, doctor_id: int) -> bool:
        """
        Assign a doctor to a specialization.
        
        Args:
            specialization_id: Specialization ID
            doctor_id: Doctor ID
        
        Returns:
            True if assignment successful, False if already assigned or invalid IDs
        """
        # Check if specialization exists
        specialization = self.get_specialization(specialization_id)
        if not specialization:
            return False
        
        # Check if already assigned
        check_query = "SELECT COUNT(*) FROM doctor_specializations WHERE specialization_id = %s AND doctor_id = %s"
        result = self.db.execute_query(check_query, (specialization_id, doctor_id))
        if result and result[0][0] > 0:
            return False  # Already assigned
        
        # Insert assignment
        query = "INSERT INTO doctor_specializations (specialization_id, doctor_id) VALUES (%s, %s)"
        try:
            self.db.execute_update(query, (specialization_id, doctor_id))
            return True
        except Exception:
            return False
    
    def remove_doctor(self, specialization_id: int, doctor_id: int) -> bool:
        """
        Remove a doctor from a specialization.
        
        Args:
            specialization_id: Specialization ID
            doctor_id: Doctor ID
        
        Returns:
            True if removal successful, False otherwise
        """
        query = "DELETE FROM doctor_specializations WHERE specialization_id = %s AND doctor_id = %s"
        self.db.execute_update(query, (specialization_id, doctor_id))
        return True
    
    def get_specialization_doctors(self, specialization_id: int) -> List[Dict[str, Any]]:
        """
        Get all doctors assigned to a specialization.
        
        Args:
            specialization_id: Specialization ID
        
        Returns:
            List of doctor dictionaries
        """
        query = """
            SELECT d.*, ds.assigned_date
            FROM doctors d
            INNER JOIN doctor_specializations ds ON d.doctor_id = ds.doctor_id
            WHERE ds.specialization_id = %s
            ORDER BY d.full_name
        """
        results = self.db.execute_query(query, (specialization_id,))
        return [dict(row) for row in results]
