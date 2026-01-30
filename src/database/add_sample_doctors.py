"""
Add Sample Doctors to Database
This script adds sample doctor data for testing purposes.
"""

import sys
import os
from datetime import date

# Get project root directory (two levels up from this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')

# Add src to path
sys.path.insert(0, src_dir)

from database import DatabaseManager
from services.doctor_service import DoctorService
from services.specialization_service import SpecializationService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def add_sample_doctors():
    """Add sample doctors to the database"""
    print("=" * 60)
    print("Adding Sample Doctors to Database")
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
    
    doctor_service = DoctorService(db)
    specialization_service = SpecializationService(db)
    
    # Get all specializations for assignment
    all_specializations = specialization_service.get_all_specializations(active_only=True)
    spec_ids = [s.specialization_id for s in all_specializations]
    
    # Sample doctors data
    sample_doctors = [
        {
            'full_name': 'Sarah Chen',
            'title': 'Dr.',
            'license_number': 'LIC001',
            'phone_number': '555-0201',
            'email': 'sarah.chen@hospital.com',
            'office_address': 'Room 101, Building A',
            'medical_degree': 'MD, Internal Medicine',
            'years_of_experience': 10,
            'certifications': 'Board Certified in Internal Medicine',
            'status': 'Active',
            'bio': 'Experienced internist specializing in preventive care and chronic disease management.',
            'hire_date': '2014-01-15',
            'specialization_ids': [spec_ids[0] if len(spec_ids) > 0 else None]  # Cardiology
        },
        {
            'full_name': 'Michael Brown',
            'title': 'Dr.',
            'license_number': 'LIC002',
            'phone_number': '555-0202',
            'email': 'michael.brown@hospital.com',
            'office_address': 'Room 205, Building B',
            'medical_degree': 'MD, Pediatrics',
            'years_of_experience': 15,
            'certifications': 'Board Certified in Pediatrics, Pediatric Emergency Medicine',
            'status': 'Active',
            'bio': 'Pediatrician with extensive experience in child healthcare and development.',
            'hire_date': '2009-03-20',
            'specialization_ids': [spec_ids[1] if len(spec_ids) > 1 else None]  # Pediatrics
        },
        {
            'full_name': 'Emily Davis',
            'title': 'Dr.',
            'license_number': 'LIC003',
            'phone_number': '555-0203',
            'email': 'emily.davis@hospital.com',
            'office_address': 'Room 310, Building A',
            'medical_degree': 'MD, Orthopedic Surgery',
            'years_of_experience': 8,
            'certifications': 'Board Certified in Orthopedic Surgery',
            'status': 'Active',
            'bio': 'Orthopedic surgeon specializing in joint replacement and sports medicine.',
            'hire_date': '2016-06-10',
            'specialization_ids': [spec_ids[2] if len(spec_ids) > 2 else None]  # Orthopedics
        },
        {
            'full_name': 'Robert Wilson',
            'title': 'Prof.',
            'license_number': 'LIC004',
            'phone_number': '555-0204',
            'email': 'robert.wilson@hospital.com',
            'office_address': 'Room 401, Building C',
            'medical_degree': 'MD, PhD, Neurology',
            'years_of_experience': 20,
            'certifications': 'Board Certified in Neurology, Neurocritical Care',
            'status': 'Active',
            'bio': 'Renowned neurologist with expertise in stroke treatment and neurological disorders.',
            'hire_date': '2004-02-01',
            'specialization_ids': [spec_ids[3] if len(spec_ids) > 3 else None]  # Neurology
        },
        {
            'full_name': 'Jennifer Martinez',
            'title': 'Dr.',
            'license_number': 'LIC005',
            'phone_number': '555-0205',
            'email': 'jennifer.martinez@hospital.com',
            'office_address': 'Room 502, Building B',
            'medical_degree': 'MD, Dermatology',
            'years_of_experience': 12,
            'certifications': 'Board Certified in Dermatology',
            'status': 'Active',
            'bio': 'Dermatologist specializing in skin cancer detection and cosmetic dermatology.',
            'hire_date': '2012-05-15',
            'specialization_ids': [spec_ids[4] if len(spec_ids) > 4 else None]  # Dermatology
        },
        {
            'full_name': 'David Thompson',
            'title': 'Dr.',
            'license_number': 'LIC006',
            'phone_number': '555-0206',
            'email': 'david.thompson@hospital.com',
            'office_address': 'Room 203, Building A',
            'medical_degree': 'MD, Emergency Medicine',
            'years_of_experience': 7,
            'certifications': 'Board Certified in Emergency Medicine',
            'status': 'Active',
            'bio': 'Emergency medicine physician with expertise in trauma and critical care.',
            'hire_date': '2017-08-01',
            'specialization_ids': [spec_ids[5] if len(spec_ids) > 5 else None]  # Emergency Medicine
        },
        {
            'full_name': 'Lisa Anderson',
            'title': 'Dr.',
            'license_number': 'LIC007',
            'phone_number': '555-0207',
            'email': 'lisa.anderson@hospital.com',
            'office_address': 'Room 304, Building B',
            'medical_degree': 'MD, Internal Medicine',
            'years_of_experience': 9,
            'certifications': 'Board Certified in Internal Medicine',
            'status': 'Active',
            'bio': 'Internist focusing on preventive medicine and patient education.',
            'hire_date': '2015-04-12',
            'specialization_ids': [spec_ids[6] if len(spec_ids) > 6 else None]  # Internal Medicine
        },
        {
            'full_name': 'James Taylor',
            'title': 'Dr.',
            'license_number': 'LIC008',
            'phone_number': '555-0208',
            'email': 'james.taylor@hospital.com',
            'office_address': 'Room 405, Building C',
            'medical_degree': 'MD, Oncology',
            'years_of_experience': 18,
            'certifications': 'Board Certified in Medical Oncology, Hematology',
            'status': 'Active',
            'bio': 'Oncologist specializing in cancer treatment and research.',
            'hire_date': '2006-09-20',
            'specialization_ids': [spec_ids[7] if len(spec_ids) > 7 else None]  # Oncology
        },
        {
            'full_name': 'Maria Garcia',
            'title': 'Dr.',
            'license_number': 'LIC009',
            'phone_number': '555-0209',
            'email': 'maria.garcia@hospital.com',
            'office_address': 'Room 201, Building A',
            'medical_degree': 'MD, Cardiology',
            'years_of_experience': 14,
            'certifications': 'Board Certified in Cardiology, Interventional Cardiology',
            'status': 'Active',
            'bio': 'Cardiologist with expertise in interventional procedures and heart disease management.',
            'hire_date': '2010-11-05',
            'specialization_ids': [spec_ids[0] if len(spec_ids) > 0 else None]  # Cardiology (second doctor)
        },
        {
            'full_name': 'Christopher Lee',
            'title': 'Dr.',
            'license_number': 'LIC010',
            'phone_number': '555-0210',
            'email': 'christopher.lee@hospital.com',
            'office_address': 'Room 302, Building B',
            'medical_degree': 'MD, Pediatrics',
            'years_of_experience': 6,
            'certifications': 'Board Certified in Pediatrics',
            'status': 'Active',
            'bio': 'Pediatrician with focus on adolescent medicine and preventive care.',
            'hire_date': '2018-01-08',
            'specialization_ids': [spec_ids[1] if len(spec_ids) > 1 else None]  # Pediatrics (second doctor)
        },
        {
            'full_name': 'Patricia White',
            'title': 'Dr.',
            'license_number': 'LIC011',
            'phone_number': '555-0211',
            'email': 'patricia.white@hospital.com',
            'office_address': 'Room 103, Building A',
            'medical_degree': 'MD, Cardiology',
            'years_of_experience': 11,
            'certifications': 'Board Certified in Cardiology',
            'status': 'Active',
            'bio': 'Cardiologist specializing in heart failure and cardiac rehabilitation.',
            'hire_date': '2013-07-22',
            'specialization_ids': [spec_ids[0] if len(spec_ids) > 0 else None]  # Cardiology
        },
        {
            'full_name': 'Daniel Kim',
            'title': 'Dr.',
            'license_number': 'LIC012',
            'phone_number': '555-0212',
            'email': 'daniel.kim@hospital.com',
            'office_address': 'Room 206, Building B',
            'medical_degree': 'MD, Orthopedic Surgery',
            'years_of_experience': 9,
            'certifications': 'Board Certified in Orthopedic Surgery, Sports Medicine',
            'status': 'Active',
            'bio': 'Orthopedic surgeon with expertise in sports injuries and arthroscopic surgery.',
            'hire_date': '2015-03-15',
            'specialization_ids': [spec_ids[2] if len(spec_ids) > 2 else None]  # Orthopedics
        },
        {
            'full_name': 'Amanda Johnson',
            'title': 'Dr.',
            'license_number': 'LIC013',
            'phone_number': '555-0213',
            'email': 'amanda.johnson@hospital.com',
            'office_address': 'Room 402, Building C',
            'medical_degree': 'MD, Neurology',
            'years_of_experience': 13,
            'certifications': 'Board Certified in Neurology, Epilepsy',
            'status': 'Active',
            'bio': 'Neurologist specializing in epilepsy and movement disorders.',
            'hire_date': '2011-09-10',
            'specialization_ids': [spec_ids[3] if len(spec_ids) > 3 else None]  # Neurology
        },
        {
            'full_name': 'Kevin Rodriguez',
            'title': 'Dr.',
            'license_number': 'LIC014',
            'phone_number': '555-0214',
            'email': 'kevin.rodriguez@hospital.com',
            'office_address': 'Room 503, Building B',
            'medical_degree': 'MD, Dermatology',
            'years_of_experience': 5,
            'certifications': 'Board Certified in Dermatology',
            'status': 'Active',
            'bio': 'Dermatologist focusing on general dermatology and skin conditions.',
            'hire_date': '2019-02-14',
            'specialization_ids': [spec_ids[4] if len(spec_ids) > 4 else None]  # Dermatology
        },
        {
            'full_name': 'Nicole Williams',
            'title': 'Dr.',
            'license_number': 'LIC015',
            'phone_number': '555-0215',
            'email': 'nicole.williams@hospital.com',
            'office_address': 'Room 204, Building A',
            'medical_degree': 'MD, Emergency Medicine',
            'years_of_experience': 8,
            'certifications': 'Board Certified in Emergency Medicine, Toxicology',
            'status': 'Active',
            'bio': 'Emergency medicine physician with expertise in toxicology and critical care.',
            'hire_date': '2016-05-20',
            'specialization_ids': [spec_ids[5] if len(spec_ids) > 5 else None]  # Emergency Medicine
        },
        {
            'full_name': 'Thomas Moore',
            'title': 'Dr.',
            'license_number': 'LIC016',
            'phone_number': '555-0216',
            'email': 'thomas.moore@hospital.com',
            'office_address': 'Room 305, Building B',
            'medical_degree': 'MD, Internal Medicine',
            'years_of_experience': 16,
            'certifications': 'Board Certified in Internal Medicine, Geriatrics',
            'status': 'Active',
            'bio': 'Internist specializing in geriatric medicine and chronic disease management.',
            'hire_date': '2008-11-30',
            'specialization_ids': [spec_ids[6] if len(spec_ids) > 6 else None]  # Internal Medicine
        },
        {
            'full_name': 'Rachel Green',
            'title': 'Dr.',
            'license_number': 'LIC017',
            'phone_number': '555-0217',
            'email': 'rachel.green@hospital.com',
            'office_address': 'Room 406, Building C',
            'medical_degree': 'MD, Oncology',
            'years_of_experience': 12,
            'certifications': 'Board Certified in Medical Oncology',
            'status': 'Active',
            'bio': 'Oncologist specializing in breast cancer and hematologic malignancies.',
            'hire_date': '2012-04-18',
            'specialization_ids': [spec_ids[7] if len(spec_ids) > 7 else None]  # Oncology
        },
        {
            'full_name': 'Andrew Harris',
            'title': 'Dr.',
            'license_number': 'LIC018',
            'phone_number': '555-0218',
            'email': 'andrew.harris@hospital.com',
            'office_address': 'Room 104, Building A',
            'medical_degree': 'MD, Cardiology',
            'years_of_experience': 7,
            'certifications': 'Board Certified in Cardiology',
            'status': 'Active',
            'bio': 'Cardiologist with focus on preventive cardiology and cardiac imaging.',
            'hire_date': '2017-10-05',
            'specialization_ids': [spec_ids[0] if len(spec_ids) > 0 else None]  # Cardiology
        },
        {
            'full_name': 'Stephanie Clark',
            'title': 'Dr.',
            'license_number': 'LIC019',
            'phone_number': '555-0219',
            'email': 'stephanie.clark@hospital.com',
            'office_address': 'Room 207, Building B',
            'medical_degree': 'MD, Pediatrics',
            'years_of_experience': 10,
            'certifications': 'Board Certified in Pediatrics, Neonatology',
            'status': 'Active',
            'bio': 'Pediatrician with specialization in neonatology and newborn care.',
            'hire_date': '2014-06-12',
            'specialization_ids': [spec_ids[1] if len(spec_ids) > 1 else None]  # Pediatrics
        },
        {
            'full_name': 'Ryan Lewis',
            'title': 'Dr.',
            'license_number': 'LIC020',
            'phone_number': '555-0220',
            'email': 'ryan.lewis@hospital.com',
            'office_address': 'Room 311, Building A',
            'medical_degree': 'MD, Orthopedic Surgery',
            'years_of_experience': 6,
            'certifications': 'Board Certified in Orthopedic Surgery',
            'status': 'Active',
            'bio': 'Orthopedic surgeon specializing in spine surgery and trauma.',
            'hire_date': '2018-03-25',
            'specialization_ids': [spec_ids[2] if len(spec_ids) > 2 else None]  # Orthopedics
        },
        {
            'full_name': 'Michelle Walker',
            'title': 'Dr.',
            'license_number': 'LIC021',
            'phone_number': '555-0221',
            'email': 'michelle.walker@hospital.com',
            'office_address': 'Room 403, Building C',
            'medical_degree': 'MD, Neurology',
            'years_of_experience': 15,
            'certifications': 'Board Certified in Neurology, Stroke Medicine',
            'status': 'Active',
            'bio': 'Neurologist with expertise in stroke treatment and neurocritical care.',
            'hire_date': '2009-08-14',
            'specialization_ids': [spec_ids[3] if len(spec_ids) > 3 else None]  # Neurology
        },
        {
            'full_name': 'Brian Hall',
            'title': 'Dr.',
            'license_number': 'LIC022',
            'phone_number': '555-0222',
            'email': 'brian.hall@hospital.com',
            'office_address': 'Room 504, Building B',
            'medical_degree': 'MD, Dermatology',
            'years_of_experience': 4,
            'certifications': 'Board Certified in Dermatology',
            'status': 'Active',
            'bio': 'Dermatologist specializing in medical dermatology and skin cancer screening.',
            'hire_date': '2020-01-10',
            'specialization_ids': [spec_ids[4] if len(spec_ids) > 4 else None]  # Dermatology
        },
        {
            'full_name': 'Lauren Allen',
            'title': 'Dr.',
            'license_number': 'LIC023',
            'phone_number': '555-0223',
            'email': 'lauren.allen@hospital.com',
            'office_address': 'Room 208, Building A',
            'medical_degree': 'MD, Emergency Medicine',
            'years_of_experience': 5,
            'certifications': 'Board Certified in Emergency Medicine',
            'status': 'Active',
            'bio': 'Emergency medicine physician with focus on pediatric emergency care.',
            'hire_date': '2019-07-08',
            'specialization_ids': [spec_ids[5] if len(spec_ids) > 5 else None]  # Emergency Medicine
        },
        {
            'full_name': 'Jonathan Young',
            'title': 'Dr.',
            'license_number': 'LIC024',
            'phone_number': '555-0224',
            'email': 'jonathan.young@hospital.com',
            'office_address': 'Room 306, Building B',
            'medical_degree': 'MD, Internal Medicine',
            'years_of_experience': 11,
            'certifications': 'Board Certified in Internal Medicine, Endocrinology',
            'status': 'Active',
            'bio': 'Internist specializing in endocrinology and diabetes management.',
            'hire_date': '2013-12-03',
            'specialization_ids': [spec_ids[6] if len(spec_ids) > 6 else None]  # Internal Medicine
        },
        {
            'full_name': 'Samantha King',
            'title': 'Dr.',
            'license_number': 'LIC025',
            'phone_number': '555-0225',
            'email': 'samantha.king@hospital.com',
            'office_address': 'Room 407, Building C',
            'medical_degree': 'MD, Oncology',
            'years_of_experience': 9,
            'certifications': 'Board Certified in Medical Oncology, Radiation Oncology',
            'status': 'Active',
            'bio': 'Oncologist with expertise in radiation therapy and cancer treatment.',
            'hire_date': '2015-09-28',
            'specialization_ids': [spec_ids[7] if len(spec_ids) > 7 else None]  # Oncology
        },
        {
            'full_name': 'Matthew Wright',
            'title': 'Dr.',
            'license_number': 'LIC026',
            'phone_number': '555-0226',
            'email': 'matthew.wright@hospital.com',
            'office_address': 'Room 105, Building A',
            'medical_degree': 'MD, Cardiology',
            'years_of_experience': 19,
            'certifications': 'Board Certified in Cardiology, Cardiac Electrophysiology',
            'status': 'Active',
            'bio': 'Cardiologist specializing in cardiac electrophysiology and arrhythmia management.',
            'hire_date': '2005-05-15',
            'specialization_ids': [spec_ids[0] if len(spec_ids) > 0 else None]  # Cardiology
        },
        {
            'full_name': 'Jessica Lopez',
            'title': 'Dr.',
            'license_number': 'LIC027',
            'phone_number': '555-0227',
            'email': 'jessica.lopez@hospital.com',
            'office_address': 'Room 209, Building B',
            'medical_degree': 'MD, Pediatrics',
            'years_of_experience': 8,
            'certifications': 'Board Certified in Pediatrics, Pediatric Cardiology',
            'status': 'Active',
            'bio': 'Pediatrician with specialization in pediatric cardiology and congenital heart disease.',
            'hire_date': '2016-11-20',
            'specialization_ids': [spec_ids[1] if len(spec_ids) > 1 else None]  # Pediatrics
        },
        {
            'full_name': 'Brandon Hill',
            'title': 'Dr.',
            'license_number': 'LIC028',
            'phone_number': '555-0228',
            'email': 'brandon.hill@hospital.com',
            'office_address': 'Room 312, Building A',
            'medical_degree': 'MD, Orthopedic Surgery',
            'years_of_experience': 13,
            'certifications': 'Board Certified in Orthopedic Surgery, Hand Surgery',
            'status': 'Active',
            'bio': 'Orthopedic surgeon specializing in hand and upper extremity surgery.',
            'hire_date': '2011-04-07',
            'specialization_ids': [spec_ids[2] if len(spec_ids) > 2 else None]  # Orthopedics
        },
        {
            'full_name': 'Ashley Scott',
            'title': 'Dr.',
            'license_number': 'LIC029',
            'phone_number': '555-0229',
            'email': 'ashley.scott@hospital.com',
            'office_address': 'Room 404, Building C',
            'medical_degree': 'MD, Neurology',
            'years_of_experience': 10,
            'certifications': 'Board Certified in Neurology, Multiple Sclerosis',
            'status': 'Active',
            'bio': 'Neurologist specializing in multiple sclerosis and autoimmune neurological disorders.',
            'hire_date': '2014-02-18',
            'specialization_ids': [spec_ids[3] if len(spec_ids) > 3 else None]  # Neurology
        },
        {
            'full_name': 'Justin Adams',
            'title': 'Dr.',
            'license_number': 'LIC030',
            'phone_number': '555-0230',
            'email': 'justin.adams@hospital.com',
            'office_address': 'Room 505, Building B',
            'medical_degree': 'MD, Dermatology',
            'years_of_experience': 7,
            'certifications': 'Board Certified in Dermatology, Mohs Surgery',
            'status': 'Active',
            'bio': 'Dermatologist specializing in Mohs micrographic surgery for skin cancer.',
            'hire_date': '2017-06-30',
            'specialization_ids': [spec_ids[4] if len(spec_ids) > 4 else None]  # Dermatology
        }
    ]
    
    created_doctors = []
    
    try:
        print(f"\nAdding {len(sample_doctors)} sample doctors...\n")
        
        for i, doctor_data in enumerate(sample_doctors, 1):
            try:
                # Filter out None specialization IDs
                if doctor_data.get('specialization_ids'):
                    doctor_data['specialization_ids'] = [sid for sid in doctor_data['specialization_ids'] if sid is not None]
                else:
                    doctor_data['specialization_ids'] = []
                
                doctor_id = doctor_service.create_doctor(doctor_data)
                created_doctors.append(doctor_id)
                print(f"[OK] {i}. Created: {doctor_data['title']} {doctor_data['full_name']} (ID: {doctor_id}, License: {doctor_data['license_number']})")
            except Exception as e:
                print(f"[ERROR] {i}. Failed to create {doctor_data['full_name']}: {e}")
        
        print("\n" + "=" * 60)
        print(f"[SUCCESS] Added {len(created_doctors)} doctors successfully!")
        print("=" * 60)
        
        # Show summary
        print("\nDoctor Summary:")
        all_doctors = doctor_service.get_all_doctors()
        print(f"  Total doctors in database: {len(all_doctors)}")
        
        # Count by status
        active = len([d for d in all_doctors if d.status == 'Active'])
        inactive = len([d for d in all_doctors if d.status == 'Inactive'])
        on_leave = len([d for d in all_doctors if d.status == 'On Leave'])
        
        print(f"  Active: {active}")
        print(f"  Inactive: {inactive}")
        print(f"  On Leave: {on_leave}")
        
        print("\nYou can now:")
        print("  1. View doctors in phpMyAdmin or Navicat")
        print("  2. Test DoctorService in your application")
        print("  3. Use DoctorService in your application")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to add sample doctors: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    add_sample_doctors()
