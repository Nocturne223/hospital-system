"""
Add Comprehensive Data for Reports & Analytics
This script adds varied data across all tables to generate meaningful reports.
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
from services.patient_service import PatientService
from services.specialization_service import SpecializationService
from services.queue_service import QueueService
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def add_comprehensive_data():
    """Add comprehensive data for reports and analytics"""
    print("=" * 60)
    print("Adding Comprehensive Data for Reports & Analytics")
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
    
    patient_service = PatientService(db)
    specialization_service = SpecializationService(db)
    queue_service = QueueService(db)
    doctor_service = DoctorService(db)
    appointment_service = AppointmentService(db)
    
    # Get existing data
    all_patients = patient_service.get_all_patients()
    doctors = doctor_service.get_all_doctors(active_only=True)
    specializations = specialization_service.get_all_specializations(active_only=True)
    
    print(f"\nFound {len(all_patients)} patients, {len(doctors)} doctors, {len(specializations)} specializations")
    
    if not all_patients or not doctors or not specializations:
        print("[ERROR] Missing required data. Please ensure patients, doctors, and specializations exist.")
        return
    
    # Add more patients with varied registration dates (past 90 days)
    print("\n" + "=" * 60)
    print("Adding Patients with Varied Registration Dates")
    print("=" * 60)
    
    new_patients = []
    today = date.today()
    
    # Patient names for variety
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Edward', 'Fiona', 'George', 'Hannah', 
                   'Ivan', 'Julia', 'Kevin', 'Laura', 'Marcus', 'Nina', 'Oscar', 'Patricia',
                   'Quinn', 'Rachel', 'Samuel', 'Tina', 'Victor', 'Wendy', 'Xavier', 'Yvonne', 'Zachary']
    last_names = ['Anderson', 'Brown', 'Clark', 'Davis', 'Evans', 'Foster', 'Green', 'Harris',
                  'Jackson', 'King', 'Lee', 'Martinez', 'Nelson', 'Owens', 'Parker', 'Quinn',
                  'Roberts', 'Smith', 'Taylor', 'Underwood', 'Vargas', 'White', 'Young', 'Zimmerman']
    
    genders = ['Male', 'Female', 'Other']
    statuses = [0, 1, 2]  # Normal, Urgent, Super-Urgent
    
    for i in range(30):
        # Random registration date in past 90 days
        days_ago = random.randint(0, 90)
        registration_date = today - timedelta(days=days_ago)
        
        # Create patient
        patient_data = {
            'full_name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'date_of_birth': (today - timedelta(days=random.randint(18*365, 80*365))).isoformat(),
            'gender': random.choice(genders),
            'phone_number': f"555-{random.randint(1000, 9999)}",
            'email': f"patient{i+100}@example.com",
            'address': f"{random.randint(100, 9999)} Main St, City, State",
            'status': random.choice(statuses),
            'registration_date': registration_date.isoformat()
        }
        
        try:
            patient_id = patient_service.create_patient(patient_data)
            new_patients.append(patient_id)
            print(f"[OK] {i+1}. Created patient: {patient_data['full_name']} (ID: {patient_id}, Registered: {registration_date})")
        except Exception as e:
            print(f"[ERROR] {i+1}. Failed to create patient: {e}")
    
    all_patients = patient_service.get_all_patients()
    print(f"\nTotal patients now: {len(all_patients)}")
    
    # Add appointments with varied dates (past 60 days to future 30 days)
    print("\n" + "=" * 60)
    print("Adding Appointments with Varied Dates and Statuses")
    print("=" * 60)
    
    appointment_types = ['Regular', 'Follow-up', 'Emergency']
    statuses_list = ['Scheduled', 'Confirmed', 'Completed', 'Cancelled', 'No-Show']
    
    time_slots = []
    current_time = time(9, 0)
    while current_time < time(17, 0):
        time_slots.append(current_time)
        current_dt = datetime.combine(date.today(), current_time)
        next_dt = current_dt + timedelta(minutes=30)
        current_time = next_dt.time()
    
    created_appointments = 0
    target_appointments = 30
    
    for i in range(target_appointments * 2):  # Try more to account for conflicts
        if created_appointments >= target_appointments:
            break
        
        patient = random.choice(all_patients)
        doctor = random.choice(doctors)
        specialization = random.choice(specializations)
        
        # Random date (past 60 days to future 30 days)
        days_offset = random.randint(-60, 30)
        appointment_date = today + timedelta(days=days_offset)
        
        # Skip if in the past and trying to create future appointment
        if appointment_date < today:
            # For past appointments, use completed/cancelled/no-show status
            status = random.choice(['Completed', 'Cancelled', 'No-Show'])
        elif appointment_date == today:
            status = random.choice(['Scheduled', 'Confirmed'])
        else:
            status = random.choice(['Scheduled', 'Confirmed'])
        
        appointment_time = random.choice(time_slots)
        duration = random.choice([15, 30, 45, 60])
        appointment_type = random.choice(appointment_types)
        
        reasons = [
            "Routine checkup", "Follow-up consultation", "Annual physical",
            "Pain management", "Medication review", "Test results discussion",
            "Preventive care", "Chronic condition management", "Emergency consultation"
        ]
        reason = random.choice(reasons)
        
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
                'status': status
            }
            
            # Check for conflicts only for future appointments
            if appointment_date >= today:
                conflicts = appointment_service.check_conflicts(
                    doctor.doctor_id,
                    appointment_date,
                    appointment_time,
                    duration
                )
                if conflicts:
                    continue
            
            appointment_id = appointment_service.create_appointment(appointment_data)
            created_appointments += 1
            print(f"[OK] {created_appointments}. Created: {appointment_date.strftime('%Y-%m-%d')} {appointment_time.strftime('%H:%M')} - {patient.full_name} with {doctor.display_name} (Status: {status})")
        except Exception as e:
            if "future" not in str(e).lower():  # Skip "must be in future" errors for past dates
                print(f"[ERROR] Failed to create appointment: {e}")
    
    print(f"\nCreated {created_appointments} new appointments")
    
    # Add queue entries with varied dates (past 30 days)
    print("\n" + "=" * 60)
    print("Adding Queue Entries with Varied Dates")
    print("=" * 60)
    
    created_queue_entries = 0
    target_queue = 30
    
    for i in range(target_queue * 2):  # Try more to account for capacity
        if created_queue_entries >= target_queue:
            break
        
        patient = random.choice(all_patients)
        specialization = random.choice(specializations)
        
        # Random date in past 30 days
        days_ago = random.randint(0, 30)
        join_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        status = random.choice([0, 1, 2])  # Normal, Urgent, Super-Urgent
        
        # Some entries should be served/removed
        if random.random() > 0.5:  # 50% chance of being served
            served_at = join_date + timedelta(minutes=random.randint(15, 120))
            try:
                # Add to queue first
                queue_entry_id = queue_service.add_patient_to_queue(
                    patient.patient_id,
                    specialization.specialization_id,
                    status
                )
                
                # Mark as served
                queue_service.serve_patient(queue_entry_id)
                created_queue_entries += 1
                print(f"[OK] {created_queue_entries}. Added served queue entry: {patient.full_name} -> {specialization.name} (Served)")
            except Exception as e:
                # Skip if patient already in queue or capacity full
                pass
        else:
            try:
                queue_entry_id = queue_service.add_patient_to_queue(
                    patient.patient_id,
                    specialization.specialization_id,
                    status
                )
                created_queue_entries += 1
                print(f"[OK] {created_queue_entries}. Added active queue entry: {patient.full_name} -> {specialization.name}")
            except Exception as e:
                # Skip if patient already in queue or capacity full
                pass
    
    print(f"\nCreated {created_queue_entries} new queue entries")
    
    # Summary
    print("\n" + "=" * 60)
    print("Data Addition Summary")
    print("=" * 60)
    
    all_patients = patient_service.get_all_patients()
    all_appointments = appointment_service.get_all_appointments()
    all_specializations = specialization_service.get_all_specializations(active_only=True)
    total_queue = 0
    for spec in all_specializations:
        queue = queue_service.get_queue(spec.specialization_id)
        total_queue += len([qe for qe in queue if qe.is_active])
    
    print(f"Total Patients: {len(all_patients)}")
    print(f"Total Appointments: {len(all_appointments)}")
    print(f"Active Queue Entries: {total_queue}")
    print(f"Total Doctors: {len(doctors)}")
    print(f"Total Specializations: {len(all_specializations)}")
    
    print("\nReports & Analytics should now have rich data to display!")
    print("You can now:")
    print("  1. View comprehensive reports in the Reports & Analytics page")
    print("  2. See trends across different time periods")
    print("  3. Analyze patient registration patterns")
    print("  4. Review appointment completion rates")
    print("  5. Monitor queue utilization")


if __name__ == "__main__":
    add_comprehensive_data()
