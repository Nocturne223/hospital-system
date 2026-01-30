"""
Interactive Test Script for Hospital Management System
Run this to interactively test the Patient Management system.
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import after path is set
try:
    from database import DatabaseManager  # type: ignore
    from services.patient_service import PatientService  # type: ignore
    from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG  # type: ignore
except ImportError:
    # Fallback: try with src prefix
    sys.path.insert(0, project_root)
    from src.database import DatabaseManager  # type: ignore
    from src.services.patient_service import PatientService  # type: ignore
    from src.config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG  # type: ignore


def print_menu():
    """Print main menu"""
    print("\n" + "=" * 60)
    print("Hospital Management System - Interactive Test")
    print("=" * 60)
    print("\nOptions:")
    print("  1. View all patients")
    print("  2. Search patients")
    print("  3. Get patient by ID")
    print("  4. Create new patient")
    print("  5. Update patient")
    print("  6. Delete patient")
    print("  7. Filter patients by status")
    print("  8. View patient statistics")
    print("  9. Exit")
    print("=" * 60)


def view_all_patients(service):
    """View all patients"""
    print("\n--- All Patients ---")
    patients = service.get_all_patients()
    
    if not patients:
        print("No patients found.")
        return
    
    print(f"\nTotal: {len(patients)} patients\n")
    print(f"{'ID':<5} {'Name':<25} {'Age':<5} {'Status':<15} {'Phone':<15}")
    print("-" * 70)
    
    for p in patients:
        age_str = str(p.age) if p.age else "N/A"
        print(f"{p.patient_id:<5} {p.full_name:<25} {age_str:<5} {p.status_text:<15} {p.phone_number or 'N/A':<15}")


def search_patients(service):
    """Search patients"""
    print("\n--- Search Patients ---")
    search_term = input("Enter search term (name, phone, or email): ").strip()
    
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    results = service.search_patients(search_term)
    
    if not results:
        print(f"No patients found matching '{search_term}'")
        return
    
    print(f"\nFound {len(results)} patient(s):\n")
    for p in results:
        print(f"  ID: {p.patient_id}")
        print(f"  Name: {p.full_name}")
        print(f"  Age: {p.age} years" if p.age else "  Age: N/A")
        print(f"  Status: {p.status_text}")
        print(f"  Phone: {p.phone_number or 'N/A'}")
        print(f"  Email: {p.email or 'N/A'}")
        print()


def get_patient_by_id(service):
    """Get patient by ID"""
    print("\n--- Get Patient by ID ---")
    try:
        patient_id = int(input("Enter patient ID: "))
        patient = service.get_patient(patient_id)
        
        if not patient:
            print(f"Patient with ID {patient_id} not found.")
            return
        
        print("\nPatient Details:")
        print(f"  ID: {patient.patient_id}")
        print(f"  Name: {patient.full_name}")
        print(f"  Date of Birth: {patient.date_of_birth}")
        print(f"  Age: {patient.age} years" if patient.age else "  Age: N/A")
        print(f"  Gender: {patient.gender or 'N/A'}")
        print(f"  Phone: {patient.phone_number or 'N/A'}")
        print(f"  Email: {patient.email or 'N/A'}")
        print(f"  Address: {patient.address or 'N/A'}")
        print(f"  Status: {patient.status_text}")
        print(f"  Blood Type: {patient.blood_type or 'N/A'}")
        print(f"  Allergies: {patient.allergies or 'None'}")
        print(f"  Medical History: {patient.medical_history or 'None'}")
        
    except ValueError:
        print("Invalid patient ID. Please enter a number.")
    except Exception as e:
        print(f"Error: {e}")


def create_patient(service):
    """Create new patient"""
    print("\n--- Create New Patient ---")
    print("Enter patient information (press Enter to skip optional fields):\n")
    
    try:
        patient_data = {}
        
        # Required fields
        patient_data['full_name'] = input("Full Name (required): ").strip()
        if not patient_data['full_name']:
            print("Full name is required!")
            return
        
        patient_data['date_of_birth'] = input("Date of Birth YYYY-MM-DD (required): ").strip()
        if not patient_data['date_of_birth']:
            print("Date of birth is required!")
            return
        
        # Optional fields
        gender = input("Gender (Male/Female/Other): ").strip()
        if gender:
            patient_data['gender'] = gender
        
        patient_data['phone_number'] = input("Phone Number: ").strip() or None
        patient_data['email'] = input("Email: ").strip() or None
        patient_data['address'] = input("Address: ").strip() or None
        
        status_input = input("Status (0=Normal, 1=Urgent, 2=Super-Urgent) [0]: ").strip()
        patient_data['status'] = int(status_input) if status_input else 0
        
        # Create patient
        patient_id = service.create_patient(patient_data)
        print(f"\n[SUCCESS] Patient created with ID: {patient_id}")
        
    except ValueError as e:
        print(f"\n[ERROR] Validation error: {e}")
    except Exception as e:
        print(f"\n[ERROR] Failed to create patient: {e}")


def update_patient(service):
    """Update patient"""
    print("\n--- Update Patient ---")
    try:
        patient_id = int(input("Enter patient ID to update: "))
        
        # Check if patient exists
        patient = service.get_patient(patient_id)
        if not patient:
            print(f"Patient with ID {patient_id} not found.")
            return
        
        print(f"\nCurrent patient: {patient.full_name}")
        print("Enter new values (press Enter to keep current value):\n")
        
        update_data = {}
        
        new_phone = input(f"Phone [{patient.phone_number or 'N/A'}]: ").strip()
        if new_phone:
            update_data['phone_number'] = new_phone
        
        new_email = input(f"Email [{patient.email or 'N/A'}]: ").strip()
        if new_email:
            update_data['email'] = new_email
        
        new_status = input(f"Status (0=Normal, 1=Urgent, 2=Super-Urgent) [{patient.status}]: ").strip()
        if new_status:
            update_data['status'] = int(new_status)
        
        if update_data:
            success = service.update_patient(patient_id, update_data)
            if success:
                print("\n[SUCCESS] Patient updated successfully!")
            else:
                print("\n[ERROR] Failed to update patient.")
        else:
            print("\nNo changes made.")
            
    except ValueError:
        print("Invalid input.")
    except Exception as e:
        print(f"\n[ERROR] {e}")


def delete_patient(service):
    """Delete patient"""
    print("\n--- Delete Patient ---")
    try:
        patient_id = int(input("Enter patient ID to delete: "))
        
        # Check if patient exists
        patient = service.get_patient(patient_id)
        if not patient:
            print(f"Patient with ID {patient_id} not found.")
            return
        
        print(f"\nWarning: This will delete patient: {patient.full_name}")
        print("This will also delete all related records (queue entries, appointments).")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            success = service.delete_patient(patient_id)
            if success:
                print("\n[SUCCESS] Patient deleted successfully!")
            else:
                print("\n[ERROR] Failed to delete patient.")
        else:
            print("Deletion cancelled.")
            
    except ValueError:
        print("Invalid patient ID.")
    except Exception as e:
        print(f"\n[ERROR] {e}")


def filter_by_status(service):
    """Filter patients by status"""
    print("\n--- Filter Patients by Status ---")
    print("Status options:")
    print("  0 = Normal")
    print("  1 = Urgent")
    print("  2 = Super-Urgent")
    
    try:
        status = int(input("\nEnter status (0/1/2): "))
        if status not in [0, 1, 2]:
            print("Invalid status. Must be 0, 1, or 2.")
            return
        
        patients = service.get_patients_by_status(status)
        status_text = ['Normal', 'Urgent', 'Super-Urgent'][status]
        
        print(f"\nFound {len(patients)} {status_text} patient(s):\n")
        for p in patients:
            print(f"  {p.patient_id}: {p.full_name} - {p.phone_number or 'N/A'}")
            
    except ValueError:
        print("Invalid status. Please enter 0, 1, or 2.")


def view_statistics(service):
    """View patient statistics"""
    print("\n--- Patient Statistics ---")
    
    all_patients = service.get_all_patients()
    total = len(all_patients)
    
    normal = len(service.get_patients_by_status(0))
    urgent = len(service.get_patients_by_status(1))
    super_urgent = len(service.get_patients_by_status(2))
    
    print(f"\nTotal Patients: {total}")
    print(f"  Normal: {normal}")
    print(f"  Urgent: {urgent}")
    print(f"  Super-Urgent: {super_urgent}")
    
    # Gender distribution
    male_count = sum(1 for p in all_patients if p.gender == 'Male')
    female_count = sum(1 for p in all_patients if p.gender == 'Female')
    other_count = sum(1 for p in all_patients if p.gender == 'Other')
    
    print(f"\nBy Gender:")
    print(f"  Male: {male_count}")
    print(f"  Female: {female_count}")
    print(f"  Other: {other_count}")
    
    # Age statistics
    ages = [p.age for p in all_patients if p.age is not None]
    if ages:
        print(f"\nAge Statistics:")
        print(f"  Average Age: {sum(ages) / len(ages):.1f} years")
        print(f"  Youngest: {min(ages)} years")
        print(f"  Oldest: {max(ages)} years")


def main():
    """Main interactive test function"""
    print("=" * 60)
    print("Hospital Management System - Interactive Test")
    print("=" * 60)
    print("\nInitializing database connection...")
    
    try:
        # Initialize database and service
        if USE_MYSQL:
            # MySQLDatabaseManager uses different parameters
            # Note: DatabaseManager is dynamically selected (MySQL or SQLite)
            # The type checker may show warnings, but code works correctly at runtime
            db = DatabaseManager(  # pyright: ignore[reportCallIssue]
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG['port'],
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password'],
                database=MYSQL_CONFIG['database']
            )
        else:
            db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])  # pyright: ignore[reportCallIssue]
        
        service = PatientService(db)
        print("[OK] Connected to database successfully!")
        
        # Main loop
        while True:
            print_menu()
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == '1':
                view_all_patients(service)
            elif choice == '2':
                search_patients(service)
            elif choice == '3':
                get_patient_by_id(service)
            elif choice == '4':
                create_patient(service)
            elif choice == '5':
                update_patient(service)
            elif choice == '6':
                delete_patient(service)
            elif choice == '7':
                filter_by_status(service)
            elif choice == '8':
                view_statistics(service)
            elif choice == '9':
                print("\nExiting... Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter 1-9.")
            
            input("\nPress Enter to continue...")
    
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize: {e}")
        print("\nTroubleshooting:")
        print("1. Check if MySQL is running in XAMPP")
        print("2. Verify database 'hospital_system' exists")
        print("3. Check credentials in src/config.py")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
