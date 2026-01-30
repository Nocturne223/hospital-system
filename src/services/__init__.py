"""
Services package for Hospital Management System.
"""

from .patient_service import PatientService
from .specialization_service import SpecializationService
from .queue_service import QueueService

__all__ = ['PatientService', 'SpecializationService', 'QueueService']
