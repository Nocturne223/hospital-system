"""
Appointment Model

Represents an appointment in the hospital management system.
"""

from datetime import date, datetime, time, timedelta
from typing import Optional, Dict, Any


class Appointment:
    """
    Represents an appointment in the hospital management system.
    
    Attributes:
        appointment_id (int): Unique appointment identifier
        patient_id (int): Patient identifier
        doctor_id (int): Doctor identifier
        specialization_id (int): Specialization identifier
        appointment_date (date): Appointment date
        appointment_time (time): Appointment time
        duration (int): Duration in minutes (default: 30)
        appointment_type (str): Type ('Regular', 'Follow-up', 'Emergency')
        reason (Optional[str]): Appointment reason
        notes (Optional[str]): Additional notes
        status (str): Status ('Scheduled', 'Confirmed', 'Cancelled', 'Completed', 'No-Show')
        created_at (Optional[datetime]): Creation timestamp
        updated_at (Optional[datetime]): Last update timestamp
        cancelled_at (Optional[datetime]): Cancellation timestamp
        cancellation_reason (Optional[str]): Cancellation reason
    """
    
    def __init__(self,
                 appointment_id: Optional[int] = None,
                 patient_id: int = 0,
                 doctor_id: int = 0,
                 specialization_id: int = 0,
                 appointment_date: Optional[date] = None,
                 appointment_time: Optional[time] = None,
                 duration: int = 30,
                 appointment_type: str = "Regular",
                 reason: Optional[str] = None,
                 notes: Optional[str] = None,
                 status: str = "Scheduled",
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 cancelled_at: Optional[datetime] = None,
                 cancellation_reason: Optional[str] = None):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.specialization_id = specialization_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.duration = duration
        self.appointment_type = appointment_type
        self.reason = reason
        self.notes = notes
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason
    
    @property
    def appointment_datetime(self) -> Optional[datetime]:
        """Get appointment as datetime object"""
        if self.appointment_date and self.appointment_time:
            return datetime.combine(self.appointment_date, self.appointment_time)
        return None
    
    @property
    def end_time(self) -> Optional[time]:
        """Calculate end time based on duration"""
        if self.appointment_time:
            start_dt = datetime.combine(date.today(), self.appointment_time)
            end_dt = start_dt + timedelta(minutes=self.duration)
            return end_dt.time()
        return None
    
    @property
    def end_datetime(self) -> Optional[datetime]:
        """Calculate end datetime"""
        if self.appointment_datetime:
            return self.appointment_datetime + timedelta(minutes=self.duration)
        return None
    
    @property
    def is_upcoming(self) -> bool:
        """Check if appointment is in the future"""
        if self.appointment_datetime:
            return self.appointment_datetime > datetime.now()
        return False
    
    @property
    def is_past(self) -> bool:
        """Check if appointment is in the past"""
        if self.appointment_datetime:
            return self.appointment_datetime < datetime.now()
        return False
    
    @property
    def is_today(self) -> bool:
        """Check if appointment is today"""
        if self.appointment_date:
            return self.appointment_date == date.today()
        return False
    
    @property
    def is_active(self) -> bool:
        """Check if appointment is active (not cancelled)"""
        return self.status not in ['Cancelled', 'Completed', 'No-Show']
    
    @property
    def status_color(self) -> str:
        """Get color code for status (for UI)"""
        color_map = {
            'Scheduled': 'blue',
            'Confirmed': 'green',
            'Cancelled': 'red',
            'Completed': 'gray',
            'No-Show': 'orange'
        }
        return color_map.get(self.status, 'gray')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert appointment to dictionary"""
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'specialization_id': self.specialization_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.isoformat() if self.appointment_time else None,
            'appointment_datetime': self.appointment_datetime.isoformat() if self.appointment_datetime else None,
            'duration': self.duration,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'appointment_type': self.appointment_type,
            'reason': self.reason,
            'notes': self.notes,
            'status': self.status,
            'status_color': self.status_color,
            'is_upcoming': self.is_upcoming,
            'is_past': self.is_past,
            'is_today': self.is_today,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'cancellation_reason': self.cancellation_reason
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Appointment':
        """Create Appointment from dictionary"""
        return Appointment(
            appointment_id=data.get('appointment_id'),
            patient_id=data.get('patient_id', 0),
            doctor_id=data.get('doctor_id', 0),
            specialization_id=data.get('specialization_id', 0),
            appointment_date=date.fromisoformat(data['appointment_date']) if data.get('appointment_date') else None,
            appointment_time=time.fromisoformat(data['appointment_time']) if data.get('appointment_time') else None,
            duration=data.get('duration', 30),
            appointment_type=data.get('appointment_type', 'Regular'),
            reason=data.get('reason'),
            notes=data.get('notes'),
            status=data.get('status', 'Scheduled'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            cancelled_at=datetime.fromisoformat(data['cancelled_at']) if data.get('cancelled_at') else None,
            cancellation_reason=data.get('cancellation_reason')
        )
    
    def __repr__(self) -> str:
        return f"Appointment(id={self.appointment_id}, patient={self.patient_id}, doctor={self.doctor_id}, date={self.appointment_date}, time={self.appointment_time}, status={self.status})"
