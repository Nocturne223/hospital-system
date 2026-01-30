"""
Doctor Service - Business logic for doctor management
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from models.doctor import Doctor


class DoctorService:
    """
    Service class for doctor management operations.
    
    This class encapsulates all business logic related to doctor management,
    including validation, data processing, and database operations.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize DoctorService with database manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_doctor(self, doctor_data: Dict[str, Any]) -> int:
        """
        Create a new doctor record.
        
        Args:
            doctor_data: Dictionary containing doctor information.
                Required keys:
                    - full_name (str): Doctor's full name
                    - license_number (str): Medical license number (unique)
                Optional keys:
                    - title (str): Title/Designation
                    - phone_number (str): Contact phone number
                    - email (str): Email address
                    - office_address (str): Office address
                    - medical_degree (str): Medical degree
                    - years_of_experience (int): Years of experience
                    - certifications (str): Certifications
                    - status (str): Status ('Active', 'Inactive', 'On Leave')
                    - bio (str): Biography
                    - hire_date (str or date): Hire date in YYYY-MM-DD format
                    - specialization_ids (list): List of specialization IDs to assign
        
        Returns:
            int: The ID of the newly created doctor record.
        
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Validation
        if not doctor_data.get('full_name') or not doctor_data['full_name'].strip():
            raise ValueError("Full name is required")
        
        if not doctor_data.get('license_number') or not doctor_data['license_number'].strip():
            raise ValueError("License number is required")
        
        # Check for duplicate license number
        existing = self.get_doctor_by_license(doctor_data['license_number'].strip())
        if existing:
            raise ValueError(f"Doctor with license number '{doctor_data['license_number'].strip()}' already exists")
        
        # Validate status
        status = doctor_data.get('status', 'Active')
        if status not in ['Active', 'Inactive', 'On Leave']:
            raise ValueError("Status must be 'Active', 'Inactive', or 'On Leave'")
        
        # Get values with defaults
        full_name = doctor_data['full_name'].strip()
        license_number = doctor_data['license_number'].strip()
        title = doctor_data.get('title')
        phone_number = doctor_data.get('phone_number')
        email = doctor_data.get('email')
        office_address = doctor_data.get('office_address')
        medical_degree = doctor_data.get('medical_degree')
        years_of_experience = doctor_data.get('years_of_experience')
        certifications = doctor_data.get('certifications')
        bio = doctor_data.get('bio')
        hire_date = doctor_data.get('hire_date')
        
        # Convert hire_date to date object if string
        if hire_date and isinstance(hire_date, str):
            try:
                hire_date = date.fromisoformat(hire_date)
            except ValueError:
                raise ValueError("Invalid hire date format. Use YYYY-MM-DD")
        
        # Build INSERT query
        query = """
            INSERT INTO doctors 
            (full_name, title, license_number, phone_number, email, office_address,
             medical_degree, years_of_experience, certifications, status, bio, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (full_name, title, license_number, phone_number, email, office_address,
                 medical_degree, years_of_experience, certifications, status, bio, hire_date)
        
        self.db.execute_update(query, params)
        doctor_id = self.db.get_last_insert_id()
        
        # Assign specializations if provided
        specialization_ids = doctor_data.get('specialization_ids', [])
        if specialization_ids:
            for spec_id in specialization_ids:
                try:
                    self.assign_specialization(doctor_id, spec_id)
                except Exception as e:
                    # Log error but don't fail doctor creation
                    print(f"Warning: Could not assign specialization {spec_id}: {e}")
        
        return doctor_id
    
    def get_doctor(self, doctor_id: int) -> Optional[Doctor]:
        """
        Retrieve doctor by ID.
        
        Args:
            doctor_id: Unique doctor identifier
        
        Returns:
            Doctor object or None if not found
        """
        query = """
            SELECT doctor_id, full_name, title, license_number, phone_number, email,
                   office_address, medical_degree, years_of_experience, certifications,
                   status, bio, hire_date, created_at, updated_at
            FROM doctors
            WHERE doctor_id = %s
        """
        
        result = self.db.execute_query(query, (doctor_id,))
        if not result:
            return None
        
        row = result[0]
        # Handle both tuple and dict results (SQLite vs MySQL)
        if isinstance(row, dict):
            return Doctor(
                doctor_id=row.get('doctor_id'),
                full_name=row.get('full_name', ''),
                title=row.get('title'),
                license_number=row.get('license_number', ''),
                phone_number=row.get('phone_number'),
                email=row.get('email'),
                office_address=row.get('office_address'),
                medical_degree=row.get('medical_degree'),
                years_of_experience=row.get('years_of_experience'),
                certifications=row.get('certifications'),
                status=row.get('status', 'Active'),
                bio=row.get('bio'),
                hire_date=row.get('hire_date') if isinstance(row.get('hire_date'), date) else date.fromisoformat(row.get('hire_date')) if row.get('hire_date') else None,
                created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None
            )
        else:
            return Doctor(
                doctor_id=row[0],
                full_name=row[1],
                title=row[2],
                license_number=row[3],
                phone_number=row[4],
                email=row[5],
                office_address=row[6],
                medical_degree=row[7],
                years_of_experience=row[8],
                certifications=row[9],
                status=row[10],
                bio=row[11],
                hire_date=row[12] if isinstance(row[12], date) else date.fromisoformat(row[12]) if row[12] else None,
                created_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                updated_at=row[14] if isinstance(row[14], datetime) else datetime.fromisoformat(row[14]) if row[14] else None
            )
    
    def get_doctor_by_license(self, license_number: str) -> Optional[Doctor]:
        """
        Retrieve doctor by license number.
        
        Args:
            license_number: Medical license number
        
        Returns:
            Doctor object or None if not found
        """
        query = """
            SELECT doctor_id, full_name, title, license_number, phone_number, email,
                   office_address, medical_degree, years_of_experience, certifications,
                   status, bio, hire_date, created_at, updated_at
            FROM doctors
            WHERE license_number = %s
        """
        
        result = self.db.execute_query(query, (license_number,))
        if not result:
            return None
        
        row = result[0]
        # Handle both tuple and dict results (SQLite vs MySQL)
        if isinstance(row, dict):
            return Doctor(
                doctor_id=row.get('doctor_id'),
                full_name=row.get('full_name', ''),
                title=row.get('title'),
                license_number=row.get('license_number', ''),
                phone_number=row.get('phone_number'),
                email=row.get('email'),
                office_address=row.get('office_address'),
                medical_degree=row.get('medical_degree'),
                years_of_experience=row.get('years_of_experience'),
                certifications=row.get('certifications'),
                status=row.get('status', 'Active'),
                bio=row.get('bio'),
                hire_date=row.get('hire_date') if isinstance(row.get('hire_date'), date) else date.fromisoformat(row.get('hire_date')) if row.get('hire_date') else None,
                created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None
            )
        else:
            return Doctor(
                doctor_id=row[0],
                full_name=row[1],
                title=row[2],
                license_number=row[3],
                phone_number=row[4],
                email=row[5],
                office_address=row[6],
                medical_degree=row[7],
                years_of_experience=row[8],
                certifications=row[9],
                status=row[10],
                bio=row[11],
                hire_date=row[12] if isinstance(row[12], date) else date.fromisoformat(row[12]) if row[12] else None,
                created_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                updated_at=row[14] if isinstance(row[14], datetime) else datetime.fromisoformat(row[14]) if row[14] else None
            )
    
    def get_all_doctors(self, active_only: bool = False) -> List[Doctor]:
        """
        Retrieve all doctors.
        
        Args:
            active_only: If True, only return active doctors
        
        Returns:
            List of Doctor objects
        """
        if active_only:
            query = """
                SELECT doctor_id, full_name, title, license_number, phone_number, email,
                       office_address, medical_degree, years_of_experience, certifications,
                       status, bio, hire_date, created_at, updated_at
                FROM doctors
                WHERE status = 'Active'
                ORDER BY full_name ASC
            """
        else:
            query = """
                SELECT doctor_id, full_name, title, license_number, phone_number, email,
                       office_address, medical_degree, years_of_experience, certifications,
                       status, bio, hire_date, created_at, updated_at
                FROM doctors
                ORDER BY full_name ASC
            """
        
        results = self.db.execute_query(query)
        
        doctors = []
        for row in results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                doctor = Doctor(
                    doctor_id=row.get('doctor_id'),
                    full_name=row.get('full_name', ''),
                    title=row.get('title'),
                    license_number=row.get('license_number', ''),
                    phone_number=row.get('phone_number'),
                    email=row.get('email'),
                    office_address=row.get('office_address'),
                    medical_degree=row.get('medical_degree'),
                    years_of_experience=row.get('years_of_experience'),
                    certifications=row.get('certifications'),
                    status=row.get('status', 'Active'),
                    bio=row.get('bio'),
                    hire_date=row.get('hire_date') if isinstance(row.get('hire_date'), date) else date.fromisoformat(row.get('hire_date')) if row.get('hire_date') else None,
                    created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                    updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None
                )
            else:
                doctor = Doctor(
                    doctor_id=row[0],
                    full_name=row[1],
                    title=row[2],
                    license_number=row[3],
                    phone_number=row[4],
                    email=row[5],
                    office_address=row[6],
                    medical_degree=row[7],
                    years_of_experience=row[8],
                    certifications=row[9],
                    status=row[10],
                    bio=row[11],
                    hire_date=row[12] if isinstance(row[12], date) else date.fromisoformat(row[12]) if row[12] else None,
                    created_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                    updated_at=row[14] if isinstance(row[14], datetime) else datetime.fromisoformat(row[14]) if row[14] else None
                )
            doctors.append(doctor)
        
        return doctors
    
    def search_doctors(self, query: str) -> List[Doctor]:
        """
        Search doctors by name, license number, or email.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching Doctor objects
        """
        search_query = """
            SELECT doctor_id, full_name, title, license_number, phone_number, email,
                   office_address, medical_degree, years_of_experience, certifications,
                   status, bio, hire_date, created_at, updated_at
            FROM doctors
            WHERE full_name LIKE %s 
               OR license_number LIKE %s 
               OR email LIKE %s
            ORDER BY full_name ASC
        """
        
        search_term = f"%{query}%"
        results = self.db.execute_query(search_query, (search_term, search_term, search_term))
        
        doctors = []
        for row in results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                doctor = Doctor(
                    doctor_id=row.get('doctor_id'),
                    full_name=row.get('full_name', ''),
                    title=row.get('title'),
                    license_number=row.get('license_number', ''),
                    phone_number=row.get('phone_number'),
                    email=row.get('email'),
                    office_address=row.get('office_address'),
                    medical_degree=row.get('medical_degree'),
                    years_of_experience=row.get('years_of_experience'),
                    certifications=row.get('certifications'),
                    status=row.get('status', 'Active'),
                    bio=row.get('bio'),
                    hire_date=row.get('hire_date') if isinstance(row.get('hire_date'), date) else date.fromisoformat(row.get('hire_date')) if row.get('hire_date') else None,
                    created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                    updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None
                )
            else:
                doctor = Doctor(
                    doctor_id=row[0],
                    full_name=row[1],
                    title=row[2],
                    license_number=row[3],
                    phone_number=row[4],
                    email=row[5],
                    office_address=row[6],
                    medical_degree=row[7],
                    years_of_experience=row[8],
                    certifications=row[9],
                    status=row[10],
                    bio=row[11],
                    hire_date=row[12] if isinstance(row[12], date) else date.fromisoformat(row[12]) if row[12] else None,
                    created_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                    updated_at=row[14] if isinstance(row[14], datetime) else datetime.fromisoformat(row[14]) if row[14] else None
                )
            doctors.append(doctor)
        
        return doctors
    
    def update_doctor(self, doctor_id: int, doctor_data: Dict[str, Any]) -> bool:
        """
        Update doctor information.
        
        Args:
            doctor_id: Doctor ID to update
            doctor_data: Dictionary containing fields to update
        
        Returns:
            True if update successful, False if doctor not found
        """
        # Check if doctor exists
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            return False
        
        # Build update query dynamically
        updates = []
        params = []
        
        if 'full_name' in doctor_data:
            updates.append("full_name = %s")
            params.append(doctor_data['full_name'].strip())
        
        if 'title' in doctor_data:
            updates.append("title = %s")
            params.append(doctor_data['title'])
        
        if 'license_number' in doctor_data:
            # Check for duplicate license number (excluding current doctor)
            existing = self.get_doctor_by_license(doctor_data['license_number'].strip())
            if existing and existing.doctor_id != doctor_id:
                raise ValueError(f"License number '{doctor_data['license_number'].strip()}' is already in use")
            updates.append("license_number = %s")
            params.append(doctor_data['license_number'].strip())
        
        if 'phone_number' in doctor_data:
            updates.append("phone_number = %s")
            params.append(doctor_data['phone_number'])
        
        if 'email' in doctor_data:
            updates.append("email = %s")
            params.append(doctor_data['email'])
        
        if 'office_address' in doctor_data:
            updates.append("office_address = %s")
            params.append(doctor_data['office_address'])
        
        if 'medical_degree' in doctor_data:
            updates.append("medical_degree = %s")
            params.append(doctor_data['medical_degree'])
        
        if 'years_of_experience' in doctor_data:
            updates.append("years_of_experience = %s")
            params.append(doctor_data['years_of_experience'])
        
        if 'certifications' in doctor_data:
            updates.append("certifications = %s")
            params.append(doctor_data['certifications'])
        
        if 'status' in doctor_data:
            if doctor_data['status'] not in ['Active', 'Inactive', 'On Leave']:
                raise ValueError("Status must be 'Active', 'Inactive', or 'On Leave'")
            updates.append("status = %s")
            params.append(doctor_data['status'])
        
        if 'bio' in doctor_data:
            updates.append("bio = %s")
            params.append(doctor_data['bio'])
        
        if 'hire_date' in doctor_data:
            hire_date = doctor_data['hire_date']
            if isinstance(hire_date, str):
                try:
                    hire_date = date.fromisoformat(hire_date)
                except ValueError:
                    raise ValueError("Invalid hire date format. Use YYYY-MM-DD")
            updates.append("hire_date = %s")
            params.append(hire_date)
        
        if not updates:
            return True  # No changes to make
        
        # Add updated_at timestamp
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        # Add doctor_id to params
        params.append(doctor_id)
        
        query = f"UPDATE doctors SET {', '.join(updates)} WHERE doctor_id = %s"
        self.db.execute_update(query, tuple(params))
        
        return True
    
    def delete_doctor(self, doctor_id: int, force: bool = False) -> bool:
        """
        Delete or deactivate a doctor.
        
        By default, this performs a soft delete (sets status = 'Inactive').
        Set force=True for hard delete (not recommended).
        
        Args:
            doctor_id: Doctor ID to delete
            force: If True, perform hard delete (default: False)
        
        Returns:
            True if deletion successful, False if doctor not found
        """
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            return False
        
        if force:
            # Hard delete (not recommended - will cascade delete related records)
            query = "DELETE FROM doctors WHERE doctor_id = %s"
            self.db.execute_update(query, (doctor_id,))
        else:
            # Soft delete
            query = "UPDATE doctors SET status = 'Inactive', updated_at = CURRENT_TIMESTAMP WHERE doctor_id = %s"
            self.db.execute_update(query, (doctor_id,))
        
        return True
    
    def assign_specialization(self, doctor_id: int, specialization_id: int) -> bool:
        """
        Assign a doctor to a specialization.
        
        Args:
            doctor_id: Doctor identifier
            specialization_id: Specialization identifier
        
        Returns:
            True if assignment successful, False if already assigned
        """
        # Check if assignment already exists
        query = """
            SELECT doctor_id FROM doctor_specializations
            WHERE doctor_id = %s AND specialization_id = %s
        """
        result = self.db.execute_query(query, (doctor_id, specialization_id))
        if result:
            return False  # Already assigned
        
        # Create assignment
        query = """
            INSERT INTO doctor_specializations (doctor_id, specialization_id)
            VALUES (%s, %s)
        """
        self.db.execute_update(query, (doctor_id, specialization_id))
        return True
    
    def remove_specialization(self, doctor_id: int, specialization_id: int) -> bool:
        """
        Remove a doctor from a specialization.
        
        Args:
            doctor_id: Doctor identifier
            specialization_id: Specialization identifier
        
        Returns:
            True if removal successful, False if not found
        """
        query = """
            DELETE FROM doctor_specializations
            WHERE doctor_id = %s AND specialization_id = %s
        """
        self.db.execute_update(query, (doctor_id, specialization_id))
        return True
    
    def get_doctor_specializations(self, doctor_id: int) -> List[int]:
        """
        Get all specialization IDs assigned to a doctor.
        
        Args:
            doctor_id: Doctor identifier
        
        Returns:
            List of specialization IDs
        """
        query = """
            SELECT specialization_id FROM doctor_specializations
            WHERE doctor_id = %s
        """
        results = self.db.execute_query(query, (doctor_id,))
        
        specialization_ids = []
        for row in results:
            if isinstance(row, dict):
                specialization_ids.append(row.get('specialization_id'))
            else:
                specialization_ids.append(row[0])
        
        return specialization_ids
    
    def get_doctors_by_specialization(self, specialization_id: int) -> List[Doctor]:
        """
        Get all doctors assigned to a specialization.
        
        Args:
            specialization_id: Specialization identifier
        
        Returns:
            List of Doctor objects
        """
        query = """
            SELECT d.doctor_id, d.full_name, d.title, d.license_number, d.phone_number, d.email,
                   d.office_address, d.medical_degree, d.years_of_experience, d.certifications,
                   d.status, d.bio, d.hire_date, d.created_at, d.updated_at
            FROM doctors d
            INNER JOIN doctor_specializations ds ON d.doctor_id = ds.doctor_id
            WHERE ds.specialization_id = %s AND d.status = 'Active'
            ORDER BY d.full_name ASC
        """
        
        results = self.db.execute_query(query, (specialization_id,))
        
        doctors = []
        for row in results:
            # Handle both tuple and dict results (SQLite vs MySQL)
            if isinstance(row, dict):
                doctor = Doctor(
                    doctor_id=row.get('doctor_id'),
                    full_name=row.get('full_name', ''),
                    title=row.get('title'),
                    license_number=row.get('license_number', ''),
                    phone_number=row.get('phone_number'),
                    email=row.get('email'),
                    office_address=row.get('office_address'),
                    medical_degree=row.get('medical_degree'),
                    years_of_experience=row.get('years_of_experience'),
                    certifications=row.get('certifications'),
                    status=row.get('status', 'Active'),
                    bio=row.get('bio'),
                    hire_date=row.get('hire_date') if isinstance(row.get('hire_date'), date) else date.fromisoformat(row.get('hire_date')) if row.get('hire_date') else None,
                    created_at=row.get('created_at') if isinstance(row.get('created_at'), datetime) else datetime.fromisoformat(row.get('created_at')) if row.get('created_at') else None,
                    updated_at=row.get('updated_at') if isinstance(row.get('updated_at'), datetime) else datetime.fromisoformat(row.get('updated_at')) if row.get('updated_at') else None
                )
            else:
                doctor = Doctor(
                    doctor_id=row[0],
                    full_name=row[1],
                    title=row[2],
                    license_number=row[3],
                    phone_number=row[4],
                    email=row[5],
                    office_address=row[6],
                    medical_degree=row[7],
                    years_of_experience=row[8],
                    certifications=row[9],
                    status=row[10],
                    bio=row[11],
                    hire_date=row[12] if isinstance(row[12], date) else date.fromisoformat(row[12]) if row[12] else None,
                    created_at=row[13] if isinstance(row[13], datetime) else datetime.fromisoformat(row[13]) if row[13] else None,
                    updated_at=row[14] if isinstance(row[14], datetime) else datetime.fromisoformat(row[14]) if row[14] else None
                )
            doctors.append(doctor)
        
        return doctors
    
    def get_doctor_statistics(self, doctor_id: int) -> Dict[str, Any]:
        """
        Get doctor statistics.
        
        Args:
            doctor_id: Doctor identifier
        
        Returns:
            Dictionary containing statistics
        """
        doctor = self.get_doctor(doctor_id)
        if not doctor:
            return {}
        
        # Get specialization count
        specializations = self.get_doctor_specializations(doctor_id)
        
        # Note: More statistics can be added when appointments/queue integration is complete
        return {
            'doctor_id': doctor_id,
            'specialization_count': len(specializations),
            'status': doctor.status,
            'years_of_experience': doctor.years_of_experience
        }
