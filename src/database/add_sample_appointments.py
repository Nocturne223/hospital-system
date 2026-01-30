"""
Add Sample Appointments to Database
This script adds sample appointment data for testing purposes.
"""

import sys
import os
from datetime import date, datetime, time, timedelta
import random

# Get project root directory (two levels up from this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')

# Add src to path
sys.path.insert(0, src_dir)

# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from database import DatabaseManager
from services.appointment_service import AppointmentService
from services.patient_service import PatientService
from services.doctor_service import DoctorService
from services.specialization_service import SpecializationService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def add_sample_appointments():
    """Add sample appointments to the database"""
    print("=" * 60)
    print("Adding Sample Appointments to Database")
    print("=" * 60)
    
    # Initialize
    if USE_MYSQL:
        db = DatabaseManager(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )
    else:
        db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])
    
    appointment_service = AppointmentService(db)
    patient_service = PatientService(db)
    doctor_service = DoctorService(db)
    specialization_service = SpecializationService(db)
    
    # Get all patients, doctors, and specializations
    all_patients = patient_service.get_all_patients()
    # Filter active patients (status 1 = Active)
    patients = [p for p in all_patients if p.status == 1]
    doctors = doctor_service.get_all_doctors(active_only=True)
    specializations = specialization_service.get_all_specializations(active_only=True)
    
    if not patients:
        print("[ERROR] No active patients found. Please add patients first.")
        return
    
    if not doctors:
        print("[ERROR] No active doctors found. Please add doctors first.")
        return
    
    if not specializations:
        print("[ERROR] No active specializations found. Please add specializations first.")
        return
    
    print(f"\nFound {len(patients)} patients, {len(doctors)} doctors, {len(specializations)} specializations")
    
    # Generate sample appointments
    # Create appointments for the next 30 days
    today = date.today()
    appointment_types = ['Regular', 'Follow-up', 'Emergency']
    statuses = ['Scheduled', 'Confirmed', 'Completed', 'Cancelled']
    
    # Time slots (9 AM to 5 PM, every 30 minutes)
    time_slots = []
    current_time = time(9, 0)
    while current_time < time(17, 0):
        time_slots.append(current_time)
        current_dt = datetime.combine(date.today(), current_time)
        next_dt = current_dt + timedelta(minutes=30)
        current_time = next_dt.time()
    
    sample_appointments = []
    created_count = 0
    failed_count = 0
    
    # Create at least 30 appointments
    target_count = 30
    max_attempts = 100  # Prevent infinite loop
    
    print(f"\nGenerating {target_count} sample appointments...\n")
    
    attempt = 0
    while created_count < target_count and attempt < max_attempts:
        attempt += 1
        
        # Random patient, doctor, specialization
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        specialization = random.choice(specializations)
        
        # Random date (today to 30 days from now)
        days_ahead = random.randint(0, 30)
        appointment_date = today + timedelta(days=days_ahead)
        
        # Random time slot
        appointment_time = random.choice(time_slots)
        
        # Random duration (15, 30, 45, or 60 minutes)
        duration = random.choice([15, 30, 45, 60])
        
        # Random type and status
        appointment_type = random.choice(appointment_types)
        
        # Status depends on date
        if appointment_date < today:
            status = random.choice(['Completed', 'Cancelled', 'No-Show'])
        elif appointment_date == today:
            status = random.choice(['Scheduled', 'Confirmed'])
        else:
            status = random.choice(['Scheduled', 'Confirmed'])
        
        # Reason
        reasons = [
            "Routine checkup",
            "Follow-up consultation",
            "Annual physical examination",
            "Pain management",
            "Medication review",
            "Test results discussion",
            "Preventive care",
            "Chronic condition management",
            "Emergency consultation",
            "Second opinion",
            "Treatment plan review",
            "Symptom evaluation"
        ]
        reason = random.choice(reasons)
        
        # Notes (optional)
        notes = None
        if random.random() > 0.7:  # 30% chance of having notes
            notes_options = [
                "Patient requested morning appointment",
                "Patient has mobility issues",
                "Requires interpreter",
                "First-time visit",
                "Returning patient",
                "Insurance verification needed"
            ]
            notes = random.choice(notes_options)
        
        try:
            appointment_data = {
                'patient_id': patient.patient_id,
                'doctor_id': doctor.doctor_id,
                'specialization_id': specialization.specialization_id,
                'appointment_date': appointment_date.isoformat(),
                'appointment_time': appointment_time.strftime('%H:%M:%S'),
                'duration': duration,
                'appointment_type': appointment_type,
                'reason': reason,
                'notes': notes,
                'status': status
            }
            
            # Check for conflicts
            conflicts = appointment_service.check_conflicts(
                doctor.doctor_id,
                appointment_date,
                appointment_time,
                duration
            )
            
            if conflicts:
                # Skip this appointment if there's a conflict
                continue
            
            # Create appointment
            appointment_id = appointment_service.create_appointment(appointment_data)
            created_count += 1
            
            print(f"[OK] {created_count}. Created: {appointment_date.strftime('%Y-%m-%d')} {appointment_time.strftime('%H:%M')} - {patient.full_name} with {doctor.display_name} (ID: {appointment_id})")
        
        except Exception as e:
            failed_count += 1
            if failed_count <= 5:  # Only show first 5 errors
                print(f"[ERROR] Failed to create appointment: {e}")
    
    print("\n" + "=" * 60)
    print(f"[SUCCESS] Added {created_count} appointments successfully!")
    if failed_count > 0:
        print(f"[WARNING] {failed_count} appointments failed to create (likely due to conflicts)")
    print("=" * 60)
    
    # Show summary
    print("\nAppointment Summary:")
    all_appointments = appointment_service.get_all_appointments()
    print(f"  Total appointments in database: {len(all_appointments)}")
    
    # Count by status
    stats = appointment_service.get_appointment_statistics()
    print(f"  Scheduled: {stats['scheduled']}")
    print(f"  Confirmed: {stats['confirmed']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Cancelled: {stats['cancelled']}")
    print(f"  No-Show: {stats['no_show']}")
    print(f"  Upcoming: {stats['upcoming']}")
    print(f"  Today: {stats['today']}")
    
    print("\nYou can now:")
    print("  1. View appointments in phpMyAdmin or Navicat")
    print("  2. Test AppointmentService in your application")
    print("  3. Use AppointmentService in your Streamlit application")


if __name__ == "__main__":
    add_sample_appointments()
