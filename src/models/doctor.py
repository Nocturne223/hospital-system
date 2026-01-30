"""
Doctor Model

Represents a doctor in the hospital management system.
"""

from datetime import date, datetime
from typing import Optional, Dict, Any, List


class Doctor:
    """
    Represents a doctor in the hospital management system.
    
    Attributes:
        doctor_id (int): Unique doctor identifier
        full_name (str): Doctor's full name
        title (Optional[str]): Title/Designation (Dr., Prof., etc.)
        license_number (str): Medical license number (unique)
        phone_number (Optional[str]): Contact phone number
        email (Optional[str]): Email address
        office_address (Optional[str]): Office address
        medical_degree (Optional[str]): Medical degree
        years_of_experience (Optional[int]): Years of experience
        certifications (Optional[str]): Certifications
        status (str): Status ('Active', 'Inactive', 'On Leave')
        bio (Optional[str]): Biography/description
        hire_date (Optional[date]): Hire date
        created_at (Optional[datetime]): Creation timestamp
        updated_at (Optional[datetime]): Last update timestamp
    """
    
    def __init__(self,
                 doctor_id: Optional[int] = None,
                 full_name: str = "",
                 title: Optional[str] = None,
                 license_number: str = "",
                 phone_number: Optional[str] = None,
                 email: Optional[str] = None,
                 office_address: Optional[str] = None,
                 medical_degree: Optional[str] = None,
                 years_of_experience: Optional[int] = None,
                 certifications: Optional[str] = None,
                 status: str = "Active",
                 bio: Optional[str] = None,
                 hire_date: Optional[date] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.doctor_id = doctor_id
        self.full_name = full_name
        self.title = title
        self.license_number = license_number
        self.phone_number = phone_number
        self.email = email
        self.office_address = office_address
        self.medical_degree = medical_degree
        self.years_of_experience = years_of_experience
        self.certifications = certifications
        self.status = status
        self.bio = bio
        self.hire_date = hire_date
        self.created_at = created_at
        self.updated_at = updated_at
    
    @property
    def display_name(self) -> str:
        """Get display name with title"""
        if self.title:
            return f"{self.title} {self.full_name}"
        return self.full_name
    
    @property
    def is_active(self) -> bool:
        """Check if doctor is active"""
        return self.status == "Active"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert doctor to dictionary"""
        return {
            'doctor_id': self.doctor_id,
            'full_name': self.full_name,
            'title': self.title,
            'display_name': self.display_name,
            'license_number': self.license_number,
            'phone_number': self.phone_number,
            'email': self.email,
            'office_address': self.office_address,
            'medical_degree': self.medical_degree,
            'years_of_experience': self.years_of_experience,
            'certifications': self.certifications,
            'status': self.status,
            'is_active': self.is_active,
            'bio': self.bio,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Doctor':
        """Create Doctor from dictionary"""
        return Doctor(
            doctor_id=data.get('doctor_id'),
            full_name=data.get('full_name', ''),
            title=data.get('title'),
            license_number=data.get('license_number', ''),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            office_address=data.get('office_address'),
            medical_degree=data.get('medical_degree'),
            years_of_experience=data.get('years_of_experience'),
            certifications=data.get('certifications'),
            status=data.get('status', 'Active'),
            bio=data.get('bio'),
            hire_date=date.fromisoformat(data['hire_date']) if data.get('hire_date') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    def __repr__(self) -> str:
        return f"Doctor(id={self.doctor_id}, name={self.display_name}, license={self.license_number}, status={self.status})"
