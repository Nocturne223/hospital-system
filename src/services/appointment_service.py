"""
Appointment Service - Business logic for appointment management
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime, time, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from models.appointment import Appointment


def _parse_time(time_value) -> Optional[time]:
    """Helper function to parse time from various formats"""
    if time_value is None:
        return None
    if isinstance(time_value, time):
        return time_value
    if isinstance(time_value, timedelta):
        # MySQL TIME type is returned as timedelta
        total_seconds = int(time_value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(hours, minutes, seconds)
    if isinstance(time_value, str):
        # Handle 'HH:MM:SS' or 'HH:MM' format
        parts = time_value.split(':')
        if len(parts) >= 2:
            try:
                hour = int(parts[0])
                minute = int(parts[1])
                second = int(parts[2]) if len(parts) > 2 else 0
                return time(hour, minute, second)
            except ValueError:
                pass
    return None


class AppointmentService:
    """
    Service class for appointment management operations.
    
    This class encapsulates all business logic related to appointment management,
    including scheduling, conflict detection, and availability checking.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize AppointmentService with database manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_appointment(self, appointment_data: Dict[str, Any]) -> int:
        """
        Create a new appointment with validation.
        
        Args:
            appointment_data: Dictionary containing appointment information.
                Required keys:
                    - patient_id (int): Patient identifier
                    - doctor_id (int): Doctor identifier
                    - specialization_id (int): Specialization identifier
                    - appointment_date (str or date): Appointment date in YYYY-MM-DD format
                    - appointment_time (str or time): Appointment time in HH:MM:SS format
                Optional keys:
                    - duration (int): Duration in minutes (default: 30)
                    - appointment_type (str): Type ('Regular', 'Follow-up', 'Emergency')
                    - reason (str): Appointment reason
                    - notes (str): Additional notes
                    - status (str): Status (default: 'Scheduled')
        
        Returns:
            int: The ID of the newly created appointment
        
        Raises:
            ValueError: If validation fails or conflicts detected
        """
        # Validation
        if not appointment_data.get('patient_id'):
            raise ValueError("Patient ID is required")
        
        if not appointment_data.get('doctor_id'):
            raise ValueError("Doctor ID is required")
        
        if not appointment_data.get('specialization_id'):
            raise ValueError("Specialization ID is required")
        
        if not appointment_data.get('appointment_date'):
            raise ValueError("Appointment date is required")
        
        if not appointment_data.get('appointment_time'):
            raise ValueError("Appointment time is required")
        
        # Convert date and time
        appointment_date = appointment_data['appointment_date']
        if isinstance(appointment_date, str):
            try:
                appointment_date = date.fromisoformat(appointment_date)
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        appointment_time = appointment_data['appointment_time']
        if isinstance(appointment_time, str):
            try:
                # Handle both HH:MM:SS and HH:MM formats
                if len(appointment_time.split(':')) == 2:
                    appointment_time = time.fromisoformat(appointment_time + ':00')
                else:
                    appointment_time = time.fromisoformat(appointment_time)
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM or HH:MM:SS")
        
        # Validate appointment is in the future
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        if appointment_datetime < datetime.now():
            raise ValueError("Appointment date and time must be in the future")
        
        # Get duration
        duration = appointment_data.get('duration', 30)
        if duration <= 0:
            raise ValueError("Duration must be greater than 0")
        
        # Validate appointment type
        appointment_type = appointment_data.get('appointment_type', 'Regular')
        if appointment_type not in ['Regular', 'Follow-up', 'Emergency']:
            raise ValueError("Appointment type must be 'Regular', 'Follow-up', or 'Emergency'")
        
        # Validate status
        status = appointment_data.get('status', 'Scheduled')
        if status not in ['Scheduled', 'Confirmed', 'Cancelled', 'Completed', 'No-Show']:
            raise ValueError("Invalid status")
        
        # Check for conflicts
        conflicts = self.check_conflicts(
            appointment_data['doctor_id'],
            appointment_date,
            appointment_time,
            duration,
            exclude_appointment_id=None
        )
        if conflicts:
            raise ValueError(f"Appointment conflicts with existing appointment(s). Please choose a different time.")
        
        # Build INSERT query
        query = """
            INSERT INTO appointments 
            (patient_id, doctor_id, specialization_id, appointment_date, appointment_time,
             duration, appointment_type, reason, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            appointment_data['patient_id'],
            appointment_data['doctor_id'],
            appointment_data['specialization_id'],
            appointment_date,
            appointment_time,
            duration,
            appointment_type,
            appointment_data.get('reason'),
            appointment_data.get('notes'),
            status
        )
        
        self.db.execute_update(query, params)
        return self.db.get_last_insert_id()
    
    def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        """
        Retrieve appointment by ID.
        
        Args:
            appointment_id: Unique appointment identifier
        
        Returns:
            Appointment object or None if not found
        """
        query = """
            SELECT appointment_id, patient_id, doctor_id, specialization_id,
                   appointment_date, appointment_time, duration, appointment_type,
                   reason, notes, status, created_at, updated_at, cancelled_at, cancellation_reason
            FROM appointments
            WHERE appointment_id = %s
        """
        
        result = self.db.execute_query(query, (appointment_id,))
        if not result:
            return None
        
        row = result[0]
        # Handle both tuple and dict results (SQLite vs MySQL)
        if isinstance(row, dict):
            return Appointment(
                appointment_id=row.get('appointment_id'),
                patient_id=row.get('patient_id', 0),
                doctor_id=row.get('doctor_id', 0),
                specialization_id=row.get('specialization_id', 0),
                appointment_date=row.get('appointment_date') if isinstance(row.get('appointment_date'), date) else date.fromisoformat(row.get('appointment_date')) if row.get('appointment_date') else None,
                appointment_time=_parse_time(row.get('appointment_time')),
                duration=row.get('duration', 30),
                appointment_type=row.get('appointment_type', 'Regular'),
                reason=row.get('reason'),
                notes=row.get('notes'),
                status=row.get('status', 'Scheduled'),
                created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None,
                cancelled_at=row.get('cancelled_at') if isinstance(row.get('cancelled_at'), datetime) else datetime.fromisoformat(row.get('cancelled_at')) if row.get('cancelled_at') else None,
                cancellation_reason=row.get('cancellation_reason')
            )
        else:
            return Appointment(
                appointment_id=row[0],
                patient_id=row[1],
                doctor_id=row[2],
                specialization_id=row[3],
                appointment_date=row[4] if isinstance(row[4], date) else date.fromisoformat(row[4]) if row[4] else None,
                appointment_time=_parse_time(row[5]),
                duration=row[6],
                appointment_type=row[7],
                reason=row[8],
                notes=row[9],
                status=row[10],
                created_at=row[11] if isinstance(row[11], datetime) else datetime.fromisoformat(row[11]) if row[11] else None,
                updated_at=row[12] if isinstance(row[12], datetime) else datetime.fromisoformat(row[12]) if row[12] else None,
                cancelled_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                cancellation_reason=row[14]
            )
    
    def get_all_appointments(self, filters: Optional[Dict[str, Any]] = None) -> List[Appointment]:
        """
        Retrieve all appointments with optional filters.
        
        Args:
            filters: Optional dictionary with filter criteria:
                - patient_id (int): Filter by patient
                - doctor_id (int): Filter by doctor
                - specialization_id (int): Filter by specialization
                - status (str): Filter by status
                - start_date (date): Filter from date
                - end_date (date): Filter to date
                - upcoming_only (bool): Only future appointments
        
        Returns:
            List of Appointment objects
        """
        query = """
            SELECT appointment_id, patient_id, doctor_id, specialization_id,
                   appointment_date, appointment_time, duration, appointment_type,
                   reason, notes, status, created_at, updated_at, cancelled_at, cancellation_reason
            FROM appointments
            WHERE 1=1
        """
        
        params = []
        
        if filters:
            if filters.get('patient_id'):
                query += " AND patient_id = %s"
                params.append(filters['patient_id'])
            
            if filters.get('doctor_id'):
                query += " AND doctor_id = %s"
                params.append(filters['doctor_id'])
            
            if filters.get('specialization_id'):
                query += " AND specialization_id = %s"
                params.append(filters['specialization_id'])
            
            if filters.get('status'):
                query += " AND status = %s"
                params.append(filters['status'])
            
            if filters.get('start_date'):
                query += " AND appointment_date >= %s"
                params.append(filters['start_date'])
            
            if filters.get('end_date'):
                query += " AND appointment_date <= %s"
                params.append(filters['end_date'])
            
            if filters.get('upcoming_only'):
                # Cross-database compatible: use Python datetime comparison
                # We'll filter in Python after fetching
                pass
        
        query += " ORDER BY appointment_date ASC, appointment_time ASC"
        
        results = self.db.execute_query(query, tuple(params) if params else None)
        
        appointments = []
        now = datetime.now()
        for row in results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                appointment = Appointment(
                    appointment_id=row.get('appointment_id'),
                    patient_id=row.get('patient_id', 0),
                    doctor_id=row.get('doctor_id', 0),
                    specialization_id=row.get('specialization_id', 0),
                    appointment_date=row.get('appointment_date') if isinstance(row.get('appointment_date'), date) else date.fromisoformat(row.get('appointment_date')) if row.get('appointment_date') else None,
                    appointment_time=_parse_time(row.get('appointment_time')),
                    duration=row.get('duration', 30),
                    appointment_type=row.get('appointment_type', 'Regular'),
                    reason=row.get('reason'),
                    notes=row.get('notes'),
                    status=row.get('status', 'Scheduled'),
                    created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                    updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None,
                    cancelled_at=row.get('cancelled_at') if isinstance(row.get('cancelled_at'), datetime) else datetime.fromisoformat(row.get('cancelled_at')) if row.get('cancelled_at') else None,
                    cancellation_reason=row.get('cancellation_reason')
                )
            else:
                appointment = Appointment(
                    appointment_id=row[0],
                    patient_id=row[1],
                    doctor_id=row[2],
                    specialization_id=row[3],
                    appointment_date=row[4] if isinstance(row[4], date) else date.fromisoformat(row[4]) if row[4] else None,
                    appointment_time=_parse_time(row[5]),
                    duration=row[6],
                    appointment_type=row[7],
                    reason=row[8],
                    notes=row[9],
                    status=row[10],
                    created_at=row[11] if isinstance(row[11], datetime) else datetime.fromisoformat(row[11]) if row[11] else None,
                    updated_at=row[12] if isinstance(row[12], datetime) else datetime.fromisoformat(row[12]) if row[12] else None,
                    cancelled_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                    cancellation_reason=row[14]
                )
            
            # Filter for upcoming_only if requested
            if filters and filters.get('upcoming_only'):
                if not appointment.is_upcoming:
                    continue
            
            appointments.append(appointment)
        
        return appointments
    
    def update_appointment(self, appointment_id: int, appointment_data: Dict[str, Any]) -> bool:
        """
        Update appointment information.
        
        Args:
            appointment_id: Appointment ID to update
            appointment_data: Dictionary containing fields to update
        
        Returns:
            True if update successful, False if appointment not found
        """
        # Check if appointment exists
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            return False
        
        # Build update query dynamically
        updates = []
        params = []
        
        if 'patient_id' in appointment_data:
            updates.append("patient_id = %s")
            params.append(appointment_data['patient_id'])
        
        if 'doctor_id' in appointment_data:
            updates.append("doctor_id = %s")
            params.append(appointment_data['doctor_id'])
        
        if 'specialization_id' in appointment_data:
            updates.append("specialization_id = %s")
            params.append(appointment_data['specialization_id'])
        
        if 'appointment_date' in appointment_data:
            appointment_date = appointment_data['appointment_date']
            if isinstance(appointment_date, str):
                appointment_date = date.fromisoformat(appointment_date)
            updates.append("appointment_date = %s")
            params.append(appointment_date)
        
        if 'appointment_time' in appointment_data:
            appointment_time = appointment_data['appointment_time']
            if isinstance(appointment_time, str):
                if len(appointment_time.split(':')) == 2:
                    appointment_time = time.fromisoformat(appointment_time + ':00')
                else:
                    appointment_time = time.fromisoformat(appointment_time)
            updates.append("appointment_time = %s")
            params.append(appointment_time)
        
        if 'duration' in appointment_data:
            updates.append("duration = %s")
            params.append(appointment_data['duration'])
        
        if 'appointment_type' in appointment_data:
            if appointment_data['appointment_type'] not in ['Regular', 'Follow-up', 'Emergency']:
                raise ValueError("Appointment type must be 'Regular', 'Follow-up', or 'Emergency'")
            updates.append("appointment_type = %s")
            params.append(appointment_data['appointment_type'])
        
        if 'reason' in appointment_data:
            updates.append("reason = %s")
            params.append(appointment_data['reason'])
        
        if 'notes' in appointment_data:
            updates.append("notes = %s")
            params.append(appointment_data['notes'])
        
        if 'status' in appointment_data:
            if appointment_data['status'] not in ['Scheduled', 'Confirmed', 'Cancelled', 'Completed', 'No-Show']:
                raise ValueError("Invalid status")
            updates.append("status = %s")
            params.append(appointment_data['status'])
        
        if not updates:
            return True  # No changes to make
        
        # Check for conflicts if date/time changed
        if 'appointment_date' in appointment_data or 'appointment_time' in appointment_data:
            new_date = appointment_data.get('appointment_date', appointment.appointment_date)
            new_time = appointment_data.get('appointment_time', appointment.appointment_time)
            new_duration = appointment_data.get('duration', appointment.duration)
            
            if isinstance(new_date, str):
                new_date = date.fromisoformat(new_date)
            if isinstance(new_time, str):
                if len(new_time.split(':')) == 2:
                    new_time = time.fromisoformat(new_time + ':00')
                else:
                    new_time = time.fromisoformat(new_time)
            
            doctor_id = appointment_data.get('doctor_id', appointment.doctor_id)
            conflicts = self.check_conflicts(doctor_id, new_date, new_time, new_duration, exclude_appointment_id=appointment_id)
            if conflicts:
                raise ValueError(f"Appointment conflicts with existing appointment(s). Please choose a different time.")
        
        # Add updated_at timestamp
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        # Add appointment_id to params
        params.append(appointment_id)
        
        query = f"UPDATE appointments SET {', '.join(updates)} WHERE appointment_id = %s"
        self.db.execute_update(query, tuple(params))
        
        return True
    
    def cancel_appointment(self, appointment_id: int, reason: Optional[str] = None) -> bool:
        """
        Cancel an appointment.
        
        Args:
            appointment_id: Appointment ID to cancel
            reason: Optional cancellation reason
        
        Returns:
            True if cancellation successful, False if appointment not found
        """
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            return False
        
        query = """
            UPDATE appointments 
            SET status = 'Cancelled', 
                cancelled_at = CURRENT_TIMESTAMP,
                cancellation_reason = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE appointment_id = %s
        """
        
        self.db.execute_update(query, (reason, appointment_id))
        return True
    
    def check_conflicts(self, doctor_id: int, appointment_date: date, 
                       appointment_time: time, duration: int,
                       exclude_appointment_id: Optional[int] = None) -> List[Appointment]:
        """
        Check for scheduling conflicts.
        
        Args:
            doctor_id: Doctor identifier
            appointment_date: Appointment date
            appointment_time: Appointment start time
            duration: Appointment duration in minutes
            exclude_appointment_id: Optional appointment ID to exclude from conflict check
        
        Returns:
            List of conflicting Appointment objects
        """
        # Calculate end time
        start_datetime = datetime.combine(appointment_date, appointment_time)
        end_datetime = start_datetime + timedelta(minutes=duration)
        
        # Query for overlapping appointments
        # Get all appointments for the doctor on this date
        query = """
            SELECT appointment_id, patient_id, doctor_id, specialization_id,
                   appointment_date, appointment_time, duration, appointment_type,
                   reason, notes, status, created_at, updated_at, cancelled_at, cancellation_reason
            FROM appointments
            WHERE doctor_id = %s
              AND status NOT IN ('Cancelled', 'Completed', 'No-Show')
              AND appointment_date = %s
        """
        
        params = (doctor_id, appointment_date)
        
        if exclude_appointment_id:
            query += " AND appointment_id != %s"
            params = params + (exclude_appointment_id,)
        
        results = self.db.execute_query(query, params)
        
        conflicts = []
        for row in results:
            # Calculate if this appointment overlaps with the requested time
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                existing_time = row.get('appointment_time')
                existing_duration = row.get('duration', 30)
            else:
                existing_time = row[5]
                existing_duration = row[6]
            
            # Convert time to datetime for comparison
            if isinstance(existing_time, str):
                if len(existing_time.split(':')) == 2:
                    existing_time = time.fromisoformat(existing_time + ':00')
                else:
                    existing_time = time.fromisoformat(existing_time)
            
            existing_start = datetime.combine(appointment_date, existing_time)
            existing_end = existing_start + timedelta(minutes=existing_duration)
            
            # Check for overlap
            if not (end_datetime <= existing_start or start_datetime >= existing_end):
                # There's an overlap - add to conflicts
                if isinstance(row, dict):
                    appointment = Appointment(
                        appointment_id=row.get('appointment_id'),
                        patient_id=row.get('patient_id', 0),
                        doctor_id=row.get('doctor_id', 0),
                        specialization_id=row.get('specialization_id', 0),
                        appointment_date=row.get('appointment_date') if isinstance(row.get('appointment_date'), date) else date.fromisoformat(row.get('appointment_date')) if row.get('appointment_date') else None,
                        appointment_time=existing_time,
                        duration=existing_duration,
                        appointment_type=row.get('appointment_type', 'Regular'),
                        reason=row.get('reason'),
                        notes=row.get('notes'),
                        status=row.get('status', 'Scheduled'),
                        created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                        updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None,
                        cancelled_at=row.get('cancelled_at') if isinstance(row.get('cancelled_at'), datetime) else datetime.fromisoformat(row.get('cancelled_at')) if row.get('cancelled_at') else None,
                        cancellation_reason=row.get('cancellation_reason')
                    )
                else:
                    appointment = Appointment(
                        appointment_id=row[0],
                        patient_id=row[1],
                        doctor_id=row[2],
                        specialization_id=row[3],
                        appointment_date=row[4] if isinstance(row[4], date) else date.fromisoformat(row[4]) if row[4] else None,
                        appointment_time=existing_time,
                        duration=existing_duration,
                        appointment_type=row[7],
                        reason=row[8],
                        notes=row[9],
                        status=row[10],
                        created_at=row[11] if isinstance(row[11], datetime) else datetime.fromisoformat(row[11]) if row[11] else None,
                        updated_at=row[12] if isinstance(row[12], datetime) else datetime.fromisoformat(row[12]) if row[12] else None,
                        cancelled_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                        cancellation_reason=row[14]
                    )
                conflicts.append(appointment)
        
        return conflicts
    
    def check_availability(self, doctor_id: int, appointment_date: date, 
                          appointment_time: time, duration: int) -> bool:
        """
        Check if a time slot is available for a doctor.
        
        Args:
            doctor_id: Doctor identifier
            appointment_date: Appointment date
            appointment_time: Appointment start time
            duration: Appointment duration in minutes
        
        Returns:
            True if available, False if conflicts exist
        """
        conflicts = self.check_conflicts(doctor_id, appointment_date, appointment_time, duration)
        return len(conflicts) == 0
    
    def get_doctor_calendar(self, doctor_id: int, start_date: date, 
                           end_date: date) -> List[Appointment]:
        """
        Get doctor's appointments for a date range.
        
        Args:
            doctor_id: Doctor identifier
            start_date: Start date
            end_date: End date
        
        Returns:
            List of Appointment objects
        """
        filters = {
            'doctor_id': doctor_id,
            'start_date': start_date,
            'end_date': end_date
        }
        return self.get_all_appointments(filters)
    
    def get_available_slots(self, doctor_id: int, appointment_date: date, 
                           slot_duration: int = 30) -> List[time]:
        """
        Get available time slots for a doctor on a specific date.
        
        Args:
            doctor_id: Doctor identifier
            appointment_date: Date to check
            slot_duration: Duration of each slot in minutes (default: 30)
        
        Returns:
            List of available time slots
        """
        # Default working hours: 9:00 AM to 5:00 PM
        start_time = time(9, 0)
        end_time = time(17, 0)
        
        # Get existing appointments for the day
        filters = {
            'doctor_id': doctor_id,
            'start_date': appointment_date,
            'end_date': appointment_date
        }
        existing_appointments = self.get_all_appointments(filters)
        
        # Generate all possible slots
        available_slots = []
        current_time = start_time
        
        while current_time < end_time:
            # Check if this slot conflicts with existing appointments
            conflicts = self.check_conflicts(doctor_id, appointment_date, current_time, slot_duration)
            if not conflicts:
                available_slots.append(current_time)
            
            # Move to next slot
            current_dt = datetime.combine(date.today(), current_time)
            next_dt = current_dt + timedelta(minutes=slot_duration)
            current_time = next_dt.time()
        
        return available_slots
    
    def get_appointment_statistics(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get appointment statistics.
        
        Args:
            filters: Optional filter criteria (same as get_all_appointments)
        
        Returns:
            Dictionary containing statistics
        """
        appointments = self.get_all_appointments(filters)
        
        total = len(appointments)
        scheduled = len([a for a in appointments if a.status == 'Scheduled'])
        confirmed = len([a for a in appointments if a.status == 'Confirmed'])
        cancelled = len([a for a in appointments if a.status == 'Cancelled'])
        completed = len([a for a in appointments if a.status == 'Completed'])
        no_show = len([a for a in appointments if a.status == 'No-Show'])
        upcoming = len([a for a in appointments if a.is_upcoming])
        today = len([a for a in appointments if a.is_today])
        
        return {
            'total': total,
            'scheduled': scheduled,
            'confirmed': confirmed,
            'cancelled': cancelled,
            'completed': completed,
            'no_show': no_show,
            'upcoming': upcoming,
            'today': today
        }
