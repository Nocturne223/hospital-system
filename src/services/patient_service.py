"""
Patient Service - Business logic for patient management
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from models.patient import Patient


class PatientService:
    """
    Service class for patient management operations.
    
    This class encapsulates all business logic related to patient management,
    including validation, data processing, and database operations.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize PatientService with database manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_patient(self, patient_data: Dict[str, Any]) -> int:
        """
        Create a new patient record.
        
        This method validates patient data, applies business rules, and saves
        the patient to the database.
        
        Args:
            patient_data: Dictionary containing patient information.
                Required keys:
                    - full_name (str): Patient's full name
                    - date_of_birth (str or date): Date of birth in YYYY-MM-DD format
                Optional keys:
                    - gender (str): 'Male', 'Female', or 'Other'
                    - phone_number (str): Contact phone number
                    - email (str): Email address
                    - address (str): Physical address
                    - emergency_contact_name (str): Emergency contact name
                    - emergency_contact_relationship (str): Relationship
                    - emergency_contact_phone (str): Emergency contact phone
                    - blood_type (str): Blood type
                    - allergies (str): Known allergies
                    - medical_history (str): Medical history notes
                    - status (int): Priority status (0=Normal, 1=Urgent, 2=Super-Urgent)
        
        Returns:
            int: The ID of the newly created patient record.
        
        Raises:
            ValueError: If required fields are missing or invalid.
            DatabaseError: If database operation fails.
        
        Example:
            >>> patient_data = {
            ...     'full_name': 'John Doe',
            ...     'date_of_birth': '1990-01-01',
            ...     'status': 0
            ... }
            >>> patient_id = service.create_patient(patient_data)
        """
        # Validation
        if not patient_data.get('full_name') or not patient_data['full_name'].strip():
            raise ValueError("Full name is required")
        
        if not patient_data.get('date_of_birth'):
            raise ValueError("Date of birth is required")
        
        # Convert date_of_birth to date object if string
        date_of_birth = patient_data['date_of_birth']
        if isinstance(date_of_birth, str):
            try:
                date_of_birth = date.fromisoformat(date_of_birth)
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        # Validate status
        status = patient_data.get('status', 0)
        if status not in [0, 1, 2]:
            raise ValueError("Status must be 0 (Normal), 1 (Urgent), or 2 (Super-Urgent)")
        
        # Validate gender if provided
        gender = patient_data.get('gender')
        if gender and gender not in ['Male', 'Female', 'Other']:
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'")
        
        # Build INSERT query
        query = """
            INSERT INTO patients 
            (full_name, date_of_birth, gender, phone_number, email, address,
             emergency_contact_name, emergency_contact_relationship, emergency_contact_phone,
             blood_type, allergies, medical_history, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            patient_data['full_name'].strip(),
            date_of_birth,
            gender,
            patient_data.get('phone_number'),
            patient_data.get('email'),
            patient_data.get('address'),
            patient_data.get('emergency_contact_name'),
            patient_data.get('emergency_contact_relationship'),
            patient_data.get('emergency_contact_phone'),
            patient_data.get('blood_type'),
            patient_data.get('allergies'),
            patient_data.get('medical_history'),
            status
        )
        
        self.db.execute_update(query, params)
        return self.db.get_last_insert_id()
    
    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """
        Retrieve patient by ID.
        
        Args:
            patient_id: Unique patient identifier
        
        Returns:
            Patient object or None if not found
        """
        query = "SELECT * FROM patients WHERE patient_id = %s"
        results = self.db.execute_query(query, (patient_id,))
        
        if not results:
            return None
        
        return Patient.from_dict(dict(results[0]))
    
    def update_patient(self, patient_id: int, patient_data: Dict[str, Any]) -> bool:
        """
        Update patient information.
        
        Args:
            patient_id: Patient ID to update
            patient_data: Dictionary with fields to update
        
        Returns:
            True if update successful, False if patient not found
        
        Raises:
            ValueError: If validation fails
        """
        # Check if patient exists
        existing = self.get_patient(patient_id)
        if not existing:
            return False
        
        # Validate status if provided
        if 'status' in patient_data:
            status = patient_data['status']
            if status not in [0, 1, 2]:
                raise ValueError("Status must be 0 (Normal), 1 (Urgent), or 2 (Super-Urgent)")
        
        # Validate gender if provided
        if 'gender' in patient_data:
            gender = patient_data['gender']
            if gender and gender not in ['Male', 'Female', 'Other']:
                raise ValueError("Gender must be 'Male', 'Female', or 'Other'")
        
        # Build UPDATE query dynamically
        update_fields = []
        params = []
        
        allowed_fields = [
            'full_name', 'date_of_birth', 'gender', 'phone_number', 'email',
            'address', 'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'blood_type', 'allergies', 'medical_history', 'status'
        ]
        
        for field in allowed_fields:
            if field in patient_data:
                update_fields.append(f"{field} = %s")
                value = patient_data[field]
                
                # Convert date_of_birth if string
                if field == 'date_of_birth' and isinstance(value, str):
                    value = date.fromisoformat(value)
                
                params.append(value)
        
        if not update_fields:
            return True  # Nothing to update
        
        # Add patient_id to params
        params.append(patient_id)
        
        query = f"UPDATE patients SET {', '.join(update_fields)} WHERE patient_id = %s"
        rows_affected = self.db.execute_update(query, tuple(params))
        
        return rows_affected > 0
    
    def delete_patient(self, patient_id: int) -> bool:
        """
        Delete a patient record.
        
        Warning: This will also delete all related records (queue entries, appointments)
        due to CASCADE foreign key constraints.
        
        Args:
            patient_id: Patient ID to delete
        
        Returns:
            True if deletion successful, False if patient not found
        """
        # Check if patient exists
        existing = self.get_patient(patient_id)
        if not existing:
            return False
        
        query = "DELETE FROM patients WHERE patient_id = %s"
        rows_affected = self.db.execute_update(query, (patient_id,))
        
        return rows_affected > 0
    
    def search_patients(self, search_term: str) -> List[Patient]:
        """
        Search patients by name, phone number, or email.
        
        Args:
            search_term: Search keyword
        
        Returns:
            List of matching Patient objects
        """
        if not search_term or not search_term.strip():
            return []
        
        search_pattern = f"%{search_term.strip()}%"
        
        query = """
            SELECT * FROM patients 
            WHERE full_name LIKE %s 
               OR phone_number LIKE %s 
               OR email LIKE %s
            ORDER BY full_name
        """
        
        results = self.db.execute_query(
            query, 
            (search_pattern, search_pattern, search_pattern)
        )
        
        return [Patient.from_dict(dict(row)) for row in results]
    
    def filter_patients(self, filters: Dict[str, Any]) -> List[Patient]:
        """
        Filter patients by criteria.
        
        Args:
            filters: Dictionary with filter criteria
                - status (int): Filter by status
                - gender (str): Filter by gender
                - min_age (int): Minimum age
                - max_age (int): Maximum age
        
        Returns:
            List of matching Patient objects
        """
        conditions = []
        params = []
        
        # Status filter
        if 'status' in filters:
            conditions.append("status = %s")
            params.append(filters['status'])
        
        # Gender filter
        if 'gender' in filters:
            conditions.append("gender = %s")
            params.append(filters['gender'])
        
        # Age filters (requires date calculation)
        if 'min_age' in filters or 'max_age' in filters:
            # Calculate date range for age
            today = date.today()
            if 'max_age' in filters:
                min_date = date(today.year - filters['max_age'] - 1, today.month, today.day)
                conditions.append("date_of_birth >= %s")
                params.append(min_date)
            if 'min_age' in filters:
                max_date = date(today.year - filters['min_age'], today.month, today.day)
                conditions.append("date_of_birth <= %s")
                params.append(max_date)
        
        # Build query
        query = "SELECT * FROM patients"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY full_name"
        
        results = self.db.execute_query(query, tuple(params))
        return [Patient.from_dict(dict(row)) for row in results]
    
    def get_all_patients(self, limit: Optional[int] = None) -> List[Patient]:
        """
        Get all patients.
        
        Args:
            limit: Optional limit on number of results
        
        Returns:
            List of Patient objects
        """
        query = "SELECT * FROM patients ORDER BY full_name"
        if limit:
            query += f" LIMIT {limit}"
        
        results = self.db.execute_query(query)
        return [Patient.from_dict(dict(row)) for row in results]
    
    def get_patients_by_status(self, status: int) -> List[Patient]:
        """
        Get all patients with a specific status.
        
        Args:
            status: Status value (0=Normal, 1=Urgent, 2=Super-Urgent)
        
        Returns:
            List of Patient objects
        """
        return self.filter_patients({'status': status})
