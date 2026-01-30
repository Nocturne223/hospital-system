"""
Queue Entry Model

Represents a queue entry in the hospital management system.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class QueueEntry:
    """
    Represents a queue entry in the hospital management system.
    
    Attributes:
        queue_entry_id (int): Unique queue entry identifier
        patient_id (int): Patient identifier
        specialization_id (int): Specialization identifier
        status (int): Priority status (0=Normal, 1=Urgent, 2=Super-Urgent, 3=Served)
        position (Optional[int]): Position in queue
        joined_at (datetime): Timestamp when patient joined queue
        served_at (Optional[datetime]): Timestamp when patient was served
        removed_at (Optional[datetime]): Timestamp when patient was removed
        removal_reason (Optional[str]): Reason for removal
        estimated_wait_time (Optional[int]): Estimated wait time in minutes
    """
    
    def __init__(self,
                 queue_entry_id: Optional[int] = None,
                 patient_id: int = 0,
                 specialization_id: int = 0,
                 status: int = 0,
                 position: Optional[int] = None,
                 joined_at: Optional[datetime] = None,
                 served_at: Optional[datetime] = None,
                 removed_at: Optional[datetime] = None,
                 removal_reason: Optional[str] = None,
                 estimated_wait_time: Optional[int] = None):
        self.queue_entry_id = queue_entry_id
        self.patient_id = patient_id
        self.specialization_id = specialization_id
        self.status = status
        self.position = position
        self.joined_at = joined_at if joined_at else datetime.now()
        self.served_at = served_at
        self.removed_at = removed_at
        self.removal_reason = removal_reason
        self.estimated_wait_time = estimated_wait_time
    
    @property
    def status_text(self) -> str:
        """Get human-readable status text"""
        status_map = {
            0: "Normal",
            1: "Urgent",
            2: "Super-Urgent",
            3: "Served"
        }
        return status_map.get(self.status, "Unknown")
    
    @property
    def status_color(self) -> str:
        """Get color code for status (for UI)"""
        color_map = {
            0: "green",      # Normal
            1: "yellow",     # Urgent
            2: "red",        # Super-Urgent
            3: "blue"        # Served
        }
        return color_map.get(self.status, "gray")
    
    @property
    def wait_time_minutes(self) -> int:
        """Calculate actual wait time in minutes"""
        if self.served_at and self.joined_at:
            delta = self.served_at - self.joined_at
            return int(delta.total_seconds() / 60)
        elif self.joined_at:
            delta = datetime.now() - self.joined_at
            return int(delta.total_seconds() / 60)
        return 0
    
    @property
    def wait_time_formatted(self) -> str:
        """Get formatted wait time string"""
        minutes = self.wait_time_minutes
        if minutes < 60:
            return f"{minutes} min"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m"
    
    @property
    def is_active(self) -> bool:
        """Check if queue entry is active (not served or removed)"""
        return self.status != 3 and self.removed_at is None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert queue entry to dictionary"""
        return {
            'queue_entry_id': self.queue_entry_id,
            'patient_id': self.patient_id,
            'specialization_id': self.specialization_id,
            'status': self.status,
            'status_text': self.status_text,
            'status_color': self.status_color,
            'position': self.position,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'served_at': self.served_at.isoformat() if self.served_at else None,
            'removed_at': self.removed_at.isoformat() if self.removed_at else None,
            'removal_reason': self.removal_reason,
            'estimated_wait_time': self.estimated_wait_time,
            'wait_time_minutes': self.wait_time_minutes,
            'wait_time_formatted': self.wait_time_formatted,
            'is_active': self.is_active
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'QueueEntry':
        """Create QueueEntry from dictionary"""
        return QueueEntry(
            queue_entry_id=data.get('queue_entry_id'),
            patient_id=data.get('patient_id', 0),
            specialization_id=data.get('specialization_id', 0),
            status=data.get('status', 0),
            position=data.get('position'),
            joined_at=datetime.fromisoformat(data['joined_at']) if data.get('joined_at') else None,
            served_at=datetime.fromisoformat(data['served_at']) if data.get('served_at') else None,
            removed_at=datetime.fromisoformat(data['removed_at']) if data.get('removed_at') else None,
            removal_reason=data.get('removal_reason'),
            estimated_wait_time=data.get('estimated_wait_time')
        )
    
    def __repr__(self) -> str:
        return f"QueueEntry(id={self.queue_entry_id}, patient={self.patient_id}, spec={self.specialization_id}, status={self.status_text}, pos={self.position})"
