"""
Report Service - Business logic for reporting and analytics
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from services.patient_service import PatientService
from services.specialization_service import SpecializationService
from services.queue_service import QueueService
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService


class ReportService:
    """
    Service class for generating reports and analytics.
    
    This class aggregates data from all services to provide comprehensive
    reporting and analytics capabilities.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
        patient_service (PatientService): Patient service instance
        specialization_service (SpecializationService): Specialization service instance
        queue_service (QueueService): Queue service instance
        doctor_service (DoctorService): Doctor service instance
        appointment_service (AppointmentService): Appointment service instance
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize ReportService with database manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
        self.patient_service = PatientService(db_manager)
        self.specialization_service = SpecializationService(db_manager)
        self.queue_service = QueueService(db_manager)
        self.doctor_service = DoctorService(db_manager)
        self.appointment_service = AppointmentService(db_manager)
    
    def get_patient_statistics(self, date_range: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Get comprehensive patient statistics.
        
        Args:
            date_range: Optional tuple of (start_date, end_date)
        
        Returns:
            Dictionary containing patient statistics
        """
        all_patients = self.patient_service.get_all_patients()
        
        # Filter by date range if provided
        if date_range:
            start_date, end_date = date_range
            filtered_patients = []
            for p in all_patients:
                if p.registration_date:
                    reg_date = p.registration_date
                    if isinstance(reg_date, datetime):
                        reg_date = reg_date.date()
                    elif not isinstance(reg_date, date):
                        continue
                    if start_date <= reg_date <= end_date:
                        filtered_patients.append(p)
            all_patients = filtered_patients
        
        total = len(all_patients)
        
        # Status distribution
        status_dist = {0: 0, 1: 0, 2: 0}
        for p in all_patients:
            status_dist[p.status] = status_dist.get(p.status, 0) + 1
        
        # Gender distribution
        gender_dist = {'Male': 0, 'Female': 0, 'Other': 0, 'Unknown': 0}
        for p in all_patients:
            gender = p.gender or 'Unknown'
            if gender in gender_dist:
                gender_dist[gender] += 1
            else:
                gender_dist['Other'] += 1
        
        # Age groups
        age_groups = {
            '0-18': 0,
            '19-30': 0,
            '31-50': 0,
            '51-70': 0,
            '71+': 0
        }
        for p in all_patients:
            age = p.age
            if age <= 18:
                age_groups['0-18'] += 1
            elif age <= 30:
                age_groups['19-30'] += 1
            elif age <= 50:
                age_groups['31-50'] += 1
            elif age <= 70:
                age_groups['51-70'] += 1
            else:
                age_groups['71+'] += 1
        
        # New patients (today, this week, this month)
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        def get_patient_date(reg_date):
            """Helper to convert registration_date to date object"""
            if reg_date is None:
                return None
            if isinstance(reg_date, datetime):
                return reg_date.date()
            if isinstance(reg_date, date):
                return reg_date
            return None
        
        new_today = len([p for p in all_patients if get_patient_date(p.registration_date) == today])
        new_this_week = len([p for p in all_patients if get_patient_date(p.registration_date) and get_patient_date(p.registration_date) >= week_ago])
        new_this_month = len([p for p in all_patients if get_patient_date(p.registration_date) and get_patient_date(p.registration_date) >= month_ago])
        
        return {
            'total': total,
            'status_distribution': status_dist,
            'gender_distribution': gender_dist,
            'age_groups': age_groups,
            'new_today': new_today,
            'new_this_week': new_this_week,
            'new_this_month': new_this_month
        }
    
    def get_queue_statistics(self, specialization_id: Optional[int] = None, 
                            date_range: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Get comprehensive queue statistics.
        
        Args:
            specialization_id: Optional specialization ID to filter by
            date_range: Optional tuple of (start_date, end_date)
        
        Returns:
            Dictionary containing queue statistics
        """
        # Get queue statistics from queue service
        queue_stats = self.queue_service.get_queue_statistics(specialization_id, date_range)
        
        # Get all queue entries
        if specialization_id:
            queue_entries = self.queue_service.get_queue(specialization_id)
        else:
            # Get queue entries for all specializations
            all_specializations = self.specialization_service.get_all_specializations(active_only=True)
            queue_entries = []
            for spec in all_specializations:
                queue_entries.extend(self.queue_service.get_queue(spec.specialization_id))
        
        # Filter by date range if provided
        if date_range:
            start_date, end_date = date_range
            filtered_entries = []
            for qe in queue_entries:
                if qe.joined_at:
                    join_date = qe.joined_at
                    if isinstance(join_date, datetime):
                        join_date = join_date.date()
                    elif not isinstance(join_date, date):
                        continue
                    if start_date <= join_date <= end_date:
                        filtered_entries.append(qe)
            queue_entries = filtered_entries
        
        # Priority distribution
        priority_dist = {0: 0, 1: 0, 2: 0}
        for qe in queue_entries:
            if qe.is_active:
                priority_dist[qe.status] = priority_dist.get(qe.status, 0) + 1
        
        # Average wait time (for served entries)
        served_entries = [qe for qe in queue_entries if qe.served_at]
        avg_wait_times = []
        for qe in served_entries:
            if qe.time_in_queue:
                avg_wait_times.append(qe.time_in_queue.total_seconds() / 60)  # in minutes
        
        avg_wait_time = sum(avg_wait_times) / len(avg_wait_times) if avg_wait_times else 0
        
        # Specialization breakdown
        spec_breakdown = {}
        for qe in queue_entries:
            if qe.is_active:
                spec_id = qe.specialization_id
                if spec_id not in spec_breakdown:
                    spec_breakdown[spec_id] = 0
                spec_breakdown[spec_id] += 1
        
        return {
            'total_active': queue_stats.get('total_active', 0),
            'priority_distribution': priority_dist,
            'average_wait_time_minutes': round(avg_wait_time, 2),
            'specialization_breakdown': spec_breakdown,
            'served_count': len(served_entries),
            'active_count': len([qe for qe in queue_entries if qe.is_active])
        }
    
    def get_appointment_statistics(self, date_range: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Get comprehensive appointment statistics.
        
        Args:
            date_range: Optional tuple of (start_date, end_date)
        
        Returns:
            Dictionary containing appointment statistics
        """
        # Build filters
        filters = {}
        if date_range:
            filters['start_date'] = date_range[0]
            filters['end_date'] = date_range[1]
        
        appointments = self.appointment_service.get_all_appointments(filters if filters else None)
        
        total = len(appointments)
        
        # Status distribution
        status_dist = {
            'Scheduled': 0,
            'Confirmed': 0,
            'Completed': 0,
            'Cancelled': 0,
            'No-Show': 0
        }
        for apt in appointments:
            status_dist[apt.status] = status_dist.get(apt.status, 0) + 1
        
        # Type distribution
        type_dist = {
            'Regular': 0,
            'Follow-up': 0,
            'Emergency': 0
        }
        for apt in appointments:
            type_dist[apt.appointment_type] = type_dist.get(apt.appointment_type, 0) + 1
        
        # Doctor distribution
        doctor_dist = {}
        for apt in appointments:
            doctor_id = apt.doctor_id
            if doctor_id not in doctor_dist:
                doctor_dist[doctor_id] = 0
            doctor_dist[doctor_id] += 1
        
        # Specialization distribution
        spec_dist = {}
        for apt in appointments:
            spec_id = apt.specialization_id
            if spec_id not in spec_dist:
                spec_dist[spec_id] = 0
            spec_dist[spec_id] += 1
        
        # Calculate rates
        completed_count = status_dist['Completed']
        cancelled_count = status_dist['Cancelled']
        no_show_count = status_dist['No-Show']
        total_ended = completed_count + cancelled_count + no_show_count
        
        completion_rate = (completed_count / total_ended * 100) if total_ended > 0 else 0
        cancellation_rate = (cancelled_count / total_ended * 100) if total_ended > 0 else 0
        no_show_rate = (no_show_count / total_ended * 100) if total_ended > 0 else 0
        
        return {
            'total': total,
            'status_distribution': status_dist,
            'type_distribution': type_dist,
            'doctor_distribution': doctor_dist,
            'specialization_distribution': spec_dist,
            'completion_rate': round(completion_rate, 2),
            'cancellation_rate': round(cancellation_rate, 2),
            'no_show_rate': round(no_show_rate, 2)
        }
    
    def get_doctor_statistics(self, doctor_id: Optional[int] = None, 
                             date_range: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Get comprehensive doctor statistics.
        
        Args:
            doctor_id: Optional doctor ID to filter by
            date_range: Optional tuple of (start_date, end_date)
        
        Returns:
            Dictionary containing doctor statistics
        """
        if doctor_id:
            doctors = [self.doctor_service.get_doctor(doctor_id)]
            doctors = [d for d in doctors if d]
        else:
            doctors = self.doctor_service.get_all_doctors(active_only=True)
        
        # Get appointments for each doctor
        doctor_stats = []
        for doctor in doctors:
            filters = {'doctor_id': doctor.doctor_id}
            if date_range:
                filters['start_date'] = date_range[0]
                filters['end_date'] = date_range[1]
            
            appointments = self.appointment_service.get_all_appointments(filters)
            
            total_appointments = len(appointments)
            completed = len([a for a in appointments if a.status == 'Completed'])
            cancelled = len([a for a in appointments if a.status == 'Cancelled'])
            
            # Get specializations
            specializations = self.doctor_service.get_doctor_specializations(doctor.doctor_id)
            
            doctor_stats.append({
                'doctor_id': doctor.doctor_id,
                'doctor_name': doctor.display_name,
                'total_appointments': total_appointments,
                'completed_appointments': completed,
                'cancelled_appointments': cancelled,
                'specialization_count': len(specializations),
                'status': doctor.status
            })
        
        return {
            'doctors': doctor_stats,
            'total_doctors': len(doctors),
            'active_doctors': len([d for d in doctors if d.status == 'Active'])
        }
    
    def get_specialization_statistics(self, specialization_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get comprehensive specialization statistics.
        
        Args:
            specialization_id: Optional specialization ID to filter by
        
        Returns:
            Dictionary containing specialization statistics
        """
        if specialization_id:
            specializations = [self.specialization_service.get_specialization(specialization_id)]
            specializations = [s for s in specializations if s]
        else:
            specializations = self.specialization_service.get_all_specializations(active_only=True)
        
        spec_stats = []
        for spec in specializations:
            # Get queue statistics
            queue_stats = self.queue_service.get_queue_statistics(spec.specialization_id)
            
            # Get appointments
            filters = {'specialization_id': spec.specialization_id}
            appointments = self.appointment_service.get_all_appointments(filters)
            
            # Get assigned doctors
            doctors = self.doctor_service.get_doctors_by_specialization(spec.specialization_id)
            
            spec_stats.append({
                'specialization_id': spec.specialization_id,
                'specialization_name': spec.name,
                'current_queue_size': queue_stats.get('total_active', 0),
                'max_capacity': spec.max_capacity,
                'utilization_percentage': round((queue_stats.get('total_active', 0) / spec.max_capacity * 100) if spec.max_capacity > 0 else 0, 2),
                'total_appointments': len(appointments),
                'assigned_doctors': len(doctors),
                'is_active': spec.is_active
            })
        
        return {
            'specializations': spec_stats,
            'total_specializations': len(specializations),
            'active_specializations': len([s for s in specializations if s.is_active])
        }
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for dashboard.
        
        Returns:
            Dictionary containing dashboard summary
        """
        # Get basic counts
        patients = self.patient_service.get_all_patients()
        doctors = self.doctor_service.get_all_doctors(active_only=True)
        specializations = self.specialization_service.get_all_specializations(active_only=True)
        appointments = self.appointment_service.get_all_appointments()
        
        # Get queue entries
        all_specializations = self.specialization_service.get_all_specializations(active_only=True)
        total_queue = 0
        for spec in all_specializations:
            queue = self.queue_service.get_queue(spec.specialization_id)
            total_queue += len([qe for qe in queue if qe.is_active])
        
        # Today's statistics
        today = date.today()
        new_patients_today = len([p for p in patients if p.registration_date == today])
        appointments_today = len([a for a in appointments if a.is_today])
        upcoming_appointments = len([a for a in appointments if a.is_upcoming])
        
        return {
            'total_patients': len(patients),
            'total_doctors': len(doctors),
            'total_specializations': len(specializations),
            'total_appointments': len(appointments),
            'active_queue': total_queue,
            'new_patients_today': new_patients_today,
            'appointments_today': appointments_today,
            'upcoming_appointments': upcoming_appointments
        }
