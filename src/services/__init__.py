"""
Services package for Hospital Management System.
"""

from .patient_service import PatientService
from .specialization_service import SpecializationService

__all__ = ['PatientService', 'SpecializationService']
