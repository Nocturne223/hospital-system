"""
Models package for Hospital Management System.
"""

from .patient import Patient
from .specialization import Specialization
from .queue_entry import QueueEntry

__all__ = ['Patient', 'Specialization', 'QueueEntry']
