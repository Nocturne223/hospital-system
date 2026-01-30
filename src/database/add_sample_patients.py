"""
Add Sample Patients to Database
This script adds sample patient data for testing purposes.
"""

import sys
import os

# Get project root directory (two levels up from this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')

# Add src to path
sys.path.insert(0, src_dir)

from database import DatabaseManager
from services.patient_service import PatientService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def add_sample_patients():
    """Add sample patients to the database"""
    print("=" * 60)
    print("Adding Sample Patients to Database")
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
    
    service = PatientService(db)
    
    # Sample patients data
    sample_patients = [
        {
            'full_name': 'John Doe',
            'date_of_birth': '1985-03-15',
            'gender': 'Male',
            'phone_number': '555-0101',
            'email': 'john.doe@email.com',
            'address': '123 Main Street, City, State',
            'emergency_contact_name': 'Jane Doe',
            'emergency_contact_relationship': 'Spouse',
            'emergency_contact_phone': '555-0102',
            'blood_type': 'O Positive',
            'allergies': 'Penicillin',
            'medical_history': 'Hypertension, managed with medication',
            'status': 0  # Normal
        },
        {
            'full_name': 'Jane Smith',
            'date_of_birth': '1990-07-22',
            'gender': 'Female',
            'phone_number': '555-0201',
            'email': 'jane.smith@email.com',
            'address': '456 Oak Avenue, City, State',
            'emergency_contact_name': 'Bob Smith',
            'emergency_contact_relationship': 'Husband',
            'emergency_contact_phone': '555-0202',
            'blood_type': 'A Positive',
            'allergies': 'Latex, Shellfish',
            'medical_history': 'Diabetes Type 2',
            'status': 1  # Urgent
        },
        {
            'full_name': 'Bob Johnson',
            'date_of_birth': '1978-11-05',
            'gender': 'Male',
            'phone_number': '555-0301',
            'email': 'bob.johnson@email.com',
            'address': '789 Pine Road, City, State',
            'emergency_contact_name': 'Mary Johnson',
            'emergency_contact_relationship': 'Wife',
            'emergency_contact_phone': '555-0302',
            'blood_type': 'B Negative',
            'allergies': None,
            'medical_history': 'Previous heart surgery (2020)',
            'status': 0  # Normal
        },
        {
            'full_name': 'Alice Williams',
            'date_of_birth': '1995-01-30',
            'gender': 'Female',
            'phone_number': '555-0401',
            'email': 'alice.williams@email.com',
            'address': '321 Elm Street, City, State',
            'emergency_contact_name': 'Tom Williams',
            'emergency_contact_relationship': 'Father',
            'emergency_contact_phone': '555-0402',
            'blood_type': 'AB Positive',
            'allergies': 'Peanuts, Dust',
            'medical_history': 'Asthma',
            'status': 2  # Super-Urgent
        },
        {
            'full_name': 'Michael Brown',
            'date_of_birth': '1988-05-12',
            'gender': 'Male',
            'phone_number': '555-0501',
            'email': 'michael.brown@email.com',
            'address': '654 Maple Drive, City, State',
            'emergency_contact_name': 'Sarah Brown',
            'emergency_contact_relationship': 'Sister',
            'emergency_contact_phone': '555-0502',
            'blood_type': 'O Negative',
            'allergies': None,
            'medical_history': 'Healthy, routine checkup',
            'status': 0  # Normal
        },
        {
            'full_name': 'Emily Davis',
            'date_of_birth': '1992-09-18',
            'gender': 'Female',
            'phone_number': '555-0601',
            'email': 'emily.davis@email.com',
            'address': '987 Cedar Lane, City, State',
            'emergency_contact_name': 'David Davis',
            'emergency_contact_relationship': 'Brother',
            'emergency_contact_phone': '555-0602',
            'blood_type': 'A Negative',
            'allergies': 'Iodine',
            'medical_history': 'Migraine headaches',
            'status': 1  # Urgent
        },
        {
            'full_name': 'Robert Wilson',
            'date_of_birth': '1982-12-25',
            'gender': 'Male',
            'phone_number': '555-0701',
            'email': 'robert.wilson@email.com',
            'address': '147 Birch Court, City, State',
            'emergency_contact_name': 'Lisa Wilson',
            'emergency_contact_relationship': 'Wife',
            'emergency_contact_phone': '555-0702',
            'blood_type': 'B Positive',
            'allergies': None,
            'medical_history': 'High cholesterol',
            'status': 0  # Normal
        },
        {
            'full_name': 'Sarah Martinez',
            'date_of_birth': '1998-04-08',
            'gender': 'Female',
            'phone_number': '555-0801',
            'email': 'sarah.martinez@email.com',
            'address': '258 Spruce Way, City, State',
            'emergency_contact_name': 'Carlos Martinez',
            'emergency_contact_relationship': 'Father',
            'emergency_contact_phone': '555-0802',
            'blood_type': 'O Positive',
            'allergies': 'Aspirin',
            'medical_history': 'Anemia',
            'status': 1  # Urgent
        }
    ]
    
    created_patients = []
    
    try:
        print(f"\nAdding {len(sample_patients)} sample patients...\n")
        
        for i, patient_data in enumerate(sample_patients, 1):
            try:
                patient_id = service.create_patient(patient_data)
                created_patients.append(patient_id)
                print(f"[OK] {i}. Created: {patient_data['full_name']} (ID: {patient_id})")
            except Exception as e:
                print(f"[ERROR] {i}. Failed to create {patient_data['full_name']}: {e}")
        
        print("\n" + "=" * 60)
        print(f"[SUCCESS] Added {len(created_patients)} patients successfully!")
        print("=" * 60)
        
        # Show summary
        print("\nPatient Summary:")
        all_patients = service.get_all_patients()
        print(f"  Total patients in database: {len(all_patients)}")
        
        # Count by status
        normal = len(service.get_patients_by_status(0))
        urgent = len(service.get_patients_by_status(1))
        super_urgent = len(service.get_patients_by_status(2))
        
        print(f"  Normal: {normal}")
        print(f"  Urgent: {urgent}")
        print(f"  Super-Urgent: {super_urgent}")
        
        print("\nYou can now:")
        print("  1. View patients in phpMyAdmin or Navicat")
        print("  2. Test PatientService with: python tests/test_patient_service.py")
        print("  3. Use PatientService in your application")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to add sample patients: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    add_sample_patients()
