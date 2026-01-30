"""
Patient Model

Represents a patient in the hospital management system.
"""

from datetime import date, datetime
from typing import Optional, Dict, Any


class Patient:
    """
    Represents a patient in the hospital management system.
    
    Attributes:
        patient_id (int): Unique patient identifier
        full_name (str): Patient's full name
        date_of_birth (date): Date of birth
        gender (Optional[str]): Gender ('Male', 'Female', 'Other')
        phone_number (Optional[str]): Contact phone number
        email (Optional[str]): Email address
        address (Optional[str]): Physical address
        emergency_contact_name (Optional[str]): Emergency contact name
        emergency_contact_relationship (Optional[str]): Relationship to patient
        emergency_contact_phone (Optional[str]): Emergency contact phone
        blood_type (Optional[str]): Blood type
        allergies (Optional[str]): Known allergies
        medical_history (Optional[str]): Medical history notes
        status (int): Priority status (0=Normal, 1=Urgent, 2=Super-Urgent)
        registration_date (datetime): Registration timestamp
    """
    
    def __init__(self, 
                 patient_id: Optional[int] = None,
                 full_name: str = "",
                 date_of_birth: Optional[date] = None,
                 gender: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 email: Optional[str] = None,
                 address: Optional[str] = None,
                 emergency_contact_name: Optional[str] = None,
                 emergency_contact_relationship: Optional[str] = None,
                 emergency_contact_phone: Optional[str] = None,
                 blood_type: Optional[str] = None,
                 allergies: Optional[str] = None,
                 medical_history: Optional[str] = None,
                 status: int = 0,
                 registration_date: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """
        Initialize Patient instance.
        
        Args:
            patient_id: Unique patient identifier (None for new patients)
            full_name: Patient's full name
            date_of_birth: Date of birth
            gender: Gender ('Male', 'Female', 'Other')
            phone_number: Contact phone number
            email: Email address
            address: Physical address
            emergency_contact_name: Emergency contact name
            emergency_contact_relationship: Relationship to patient
            emergency_contact_phone: Emergency contact phone
            blood_type: Blood type
            allergies: Known allergies
            medical_history: Medical history notes
            status: Priority status (0=Normal, 1=Urgent, 2=Super-Urgent)
            registration_date: Registration timestamp
        """
        self.patient_id = patient_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_relationship = emergency_contact_relationship
        self.emergency_contact_phone = emergency_contact_phone
        self.blood_type = blood_type
        self.allergies = allergies
        self.medical_history = medical_history
        self.status = status
        self.registration_date = registration_date
        self.created_at = created_at
        self.updated_at = updated_at
    
    @property
    def age(self) -> Optional[int]:
        """
        Calculate patient's age from date of birth.
        
        Returns:
            Age in years, or None if date_of_birth is not set
        """
        if not self.date_of_birth:
            return None
        
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < 
            (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def status_text(self) -> str:
        """
        Get human-readable status text.
        
        Returns:
            Status as text: 'Normal', 'Urgent', or 'Super-Urgent'
        """
        status_map = {
            0: 'Normal',
            1: 'Urgent',
            2: 'Super-Urgent'
        }
        return status_map.get(self.status, 'Unknown')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert patient to dictionary.
        
        Returns:
            Dictionary representation of patient
        """
        return {
            'patient_id': self.patient_id,
            'full_name': self.full_name,
            'date_of_birth': str(self.date_of_birth) if self.date_of_birth else None,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_relationship': self.emergency_contact_relationship,
            'emergency_contact_phone': self.emergency_contact_phone,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'medical_history': self.medical_history,
            'status': self.status,
            'status_text': self.status_text,
            'age': self.age,
            'registration_date': str(self.registration_date) if self.registration_date else None,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        """
        Create Patient instance from dictionary.
        
        Args:
            data: Dictionary containing patient data
        
        Returns:
            Patient instance
        """
        # Convert date strings to date objects
        date_of_birth = None
        if data.get('date_of_birth'):
            if isinstance(data['date_of_birth'], str):
                date_of_birth = date.fromisoformat(data['date_of_birth'])
            elif isinstance(data['date_of_birth'], date):
                date_of_birth = data['date_of_birth']
        
        # Convert datetime strings to datetime objects
        registration_date = None
        if data.get('registration_date'):
            if isinstance(data['registration_date'], str):
                registration_date = datetime.fromisoformat(data['registration_date'].replace('Z', '+00:00'))
            elif isinstance(data['registration_date'], datetime):
                registration_date = data['registration_date']
        
        return cls(
            patient_id=data.get('patient_id'),
            full_name=data.get('full_name', ''),
            date_of_birth=date_of_birth,
            gender=data.get('gender'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            address=data.get('address'),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_relationship=data.get('emergency_contact_relationship'),
            emergency_contact_phone=data.get('emergency_contact_phone'),
            blood_type=data.get('blood_type'),
            allergies=data.get('allergies'),
            medical_history=data.get('medical_history'),
            status=data.get('status', 0),
            registration_date=registration_date,
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def __str__(self) -> str:
        """String representation of patient."""
        return f"Patient(id={self.patient_id}, name={self.full_name}, status={self.status_text})"
    
    def __repr__(self) -> str:
        """Developer representation of patient."""
        return f"Patient(patient_id={self.patient_id}, full_name='{self.full_name}', status={self.status})"
