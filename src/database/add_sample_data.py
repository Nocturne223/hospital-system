"""
Add Sample Data to Database
This script adds some sample data so you can see the database in action.
"""

import sys
import os

# Add src directory to path
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from database import DatabaseManager


def add_sample_data():
    """Add sample data to the database."""
    print("=" * 60)
    print("Adding Sample Data to Database")
    print("=" * 60)
    
    db = DatabaseManager(db_path='data/hospital_system.db')
    
    try:
        # Add sample specializations
        print("\n1. Adding specializations...")
        specializations = [
            ("Cardiology", "Heart and cardiovascular system", 10),
            ("Pediatrics", "Children's health", 15),
            ("Orthopedics", "Bones and joints", 8),
            ("Neurology", "Brain and nervous system", 12),
        ]
        
        for name, desc, capacity in specializations:
            db.execute_update(
                "INSERT INTO specializations (name, description, max_capacity) VALUES (?, ?, ?)",
                (name, desc, capacity)
            )
        print(f"   [OK] Added {len(specializations)} specializations")
        
        # Add sample patients
        print("\n2. Adding patients...")
        patients = [
            ("John Doe", "1985-03-15", "Male", "555-0101", "john.doe@email.com", 0),
            ("Jane Smith", "1990-07-22", "Female", "555-0102", "jane.smith@email.com", 1),
            ("Bob Johnson", "1978-11-05", "Male", "555-0103", "bob.j@email.com", 0),
            ("Alice Williams", "1995-01-30", "Female", "555-0104", "alice.w@email.com", 2),
        ]
        
        for name, dob, gender, phone, email, status in patients:
            db.execute_update(
                """INSERT INTO patients 
                   (full_name, date_of_birth, gender, phone_number, email, status) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (name, dob, gender, phone, email, status)
            )
        print(f"   [OK] Added {len(patients)} patients")
        
        # Add sample doctors
        print("\n3. Adding doctors...")
        doctors = [
            ("Dr. Sarah Chen", "MD", "LIC001", "555-0201", "s.chen@hospital.com", "Cardiology", 10),
            ("Dr. Michael Brown", "MD", "LIC002", "555-0202", "m.brown@hospital.com", "Pediatrics", 15),
            ("Dr. Emily Davis", "MD", "LIC003", "555-0203", "e.davis@hospital.com", "Orthopedics", 8),
        ]
        
        for name, title, license_num, phone, email, degree, experience in doctors:
            db.execute_update(
                """INSERT INTO doctors 
                   (full_name, title, license_number, phone_number, email, medical_degree, years_of_experience) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (name, title, license_num, phone, email, degree, experience)
            )
        print(f"   [OK] Added {len(doctors)} doctors")
        
        # Assign doctors to specializations
        print("\n4. Assigning doctors to specializations...")
        # Get IDs (assuming they're inserted in order)
        db.execute_update(
            "INSERT INTO doctor_specializations (doctor_id, specialization_id) VALUES (1, 1)",
            ()
        )
        db.execute_update(
            "INSERT INTO doctor_specializations (doctor_id, specialization_id) VALUES (2, 2)",
            ()
        )
        db.execute_update(
            "INSERT INTO doctor_specializations (doctor_id, specialization_id) VALUES (3, 3)",
            ()
        )
        print("   [OK] Assigned 3 doctor-specialization relationships")
        
        # Add sample queue entries
        print("\n5. Adding queue entries...")
        queue_entries = [
            (1, 1, 0),  # Patient 1, Cardiology, Normal
            (2, 1, 1),  # Patient 2, Cardiology, Urgent
            (3, 2, 0),  # Patient 3, Pediatrics, Normal
            (4, 3, 2),  # Patient 4, Orthopedics, Super-Urgent
        ]
        
        for patient_id, spec_id, status in queue_entries:
            db.execute_update(
                "INSERT INTO queue_entries (patient_id, specialization_id, status) VALUES (?, ?, ?)",
                (patient_id, spec_id, status)
            )
        print(f"   [OK] Added {len(queue_entries)} queue entries")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Sample data added successfully!")
        print("=" * 60)
        print("\nYou can now view the database using:")
        print("  python src/database/view_db.py")
        print("  python src/database/view_db.py --table patients")
        print("  python src/database/view_db.py --table specializations")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to add sample data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    add_sample_data()
