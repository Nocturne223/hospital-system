"""
Specialization Model

Represents a medical specialization in the hospital management system.
"""

from datetime import datetime
from typing import Optional, Dict, Any


class Specialization:
    """
    Represents a medical specialization in the hospital management system.
    
    Attributes:
        specialization_id (int): Unique specialization identifier
        name (str): Specialization name (e.g., "Cardiology", "Pediatrics")
        description (Optional[str]): Description of the specialization
        max_capacity (int): Maximum number of patients in queue (default: 10)
        is_active (bool): Whether the specialization is active
        created_at (Optional[datetime]): Creation timestamp
        updated_at (Optional[datetime]): Last update timestamp
    """
    
    def __init__(self,
                 specialization_id: Optional[int] = None,
                 name: str = "",
                 description: Optional[str] = None,
                 max_capacity: int = 10,
                 is_active: bool = True,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """
        Initialize a Specialization instance.
        
        Args:
            specialization_id: Unique identifier
            name: Specialization name
            description: Optional description
            max_capacity: Maximum queue capacity
            is_active: Active status
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.specialization_id = specialization_id
        self.name = name
        self.description = description
        self.max_capacity = max_capacity
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self) -> str:
        """String representation of the specialization."""
        status = "Active" if self.is_active else "Inactive"
        return f"<Specialization(id={self.specialization_id}, name='{self.name}', status={status})>"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return self.name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert specialization to dictionary.
        
        Returns:
            Dictionary representation of the specialization
        """
        return {
            'specialization_id': self.specialization_id,
            'name': self.name,
            'description': self.description,
            'max_capacity': self.max_capacity,
            'is_active': self.is_active,
            'is_active_text': 'Active' if self.is_active else 'Inactive',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Specialization':
        """
        Create Specialization instance from dictionary.
        
        Args:
            data: Dictionary containing specialization data
            
        Returns:
            Specialization instance
        """
        # Parse datetime strings if present
        created_at = None
        updated_at = None
        
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            else:
                created_at = data['created_at']
        
        if data.get('updated_at'):
            if isinstance(data['updated_at'], str):
                updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            else:
                updated_at = data['updated_at']
        
        # Handle is_active (can be int 0/1 or bool)
        is_active = data.get('is_active', True)
        if isinstance(is_active, int):
            is_active = bool(is_active)
        
        return cls(
            specialization_id=data.get('specialization_id'),
            name=data.get('name', ''),
            description=data.get('description'),
            max_capacity=data.get('max_capacity', 10),
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate specialization data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.name or not self.name.strip():
            return False, "Specialization name is required"
        
        if self.max_capacity <= 0:
            return False, "Maximum capacity must be greater than 0"
        
        if self.max_capacity > 1000:
            return False, "Maximum capacity cannot exceed 1000"
        
        return True, None
