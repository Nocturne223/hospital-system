"""
Models package for Hospital Management System.
"""

from .patient import Patient
from .specialization import Specialization
from .queue_entry import QueueEntry
from .doctor import Doctor
from .appointment import Appointment

__all__ = ['Patient', 'Specialization', 'QueueEntry', 'Doctor', 'Appointment']
