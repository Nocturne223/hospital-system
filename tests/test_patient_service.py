"""
Test PatientService - Test patient management operations
"""

import sys
import os
from datetime import date

# Add src to path
project_root = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

from database import DatabaseManager
from services.patient_service import PatientService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def test_patient_service():
    """Test PatientService operations"""
    print("=" * 60)
    print("Testing PatientService")
    print("=" * 60)
    
    # Initialize database and service
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
    
    # Test 1: Create Patient
    print("\n1. Testing create_patient()...")
    try:
        patient_data = {
            'full_name': 'John Doe',
            'date_of_birth': '1990-01-15',
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
            'status': 0
        }
        
        patient_id = service.create_patient(patient_data)
        print(f"   [OK] Created patient with ID: {patient_id}")
        
    except Exception as e:
        print(f"   [ERROR] Failed to create patient: {e}")
        return False
    
    # Test 2: Get Patient
    print("\n2. Testing get_patient()...")
    try:
        patient = service.get_patient(patient_id)
        if patient:
            print(f"   [OK] Retrieved patient: {patient.full_name}")
            print(f"       Age: {patient.age} years")
            print(f"       Status: {patient.status_text}")
        else:
            print("   [ERROR] Patient not found")
            return False
    except Exception as e:
        print(f"   [ERROR] Failed to get patient: {e}")
        return False
    
    # Test 3: Update Patient
    print("\n3. Testing update_patient()...")
    try:
        update_data = {
            'phone_number': '555-9999',
            'status': 1  # Change to Urgent
        }
        success = service.update_patient(patient_id, update_data)
        if success:
            updated_patient = service.get_patient(patient_id)
            print(f"   [OK] Updated patient")
            print(f"       New phone: {updated_patient.phone_number}")
            print(f"       New status: {updated_patient.status_text}")
        else:
            print("   [ERROR] Update failed")
            return False
    except Exception as e:
        print(f"   [ERROR] Failed to update patient: {e}")
        return False
    
    # Test 4: Search Patients
    print("\n4. Testing search_patients()...")
    try:
        results = service.search_patients("John")
        print(f"   [OK] Found {len(results)} patient(s) matching 'John'")
        for p in results:
            print(f"       - {p.full_name} (ID: {p.patient_id})")
    except Exception as e:
        print(f"   [ERROR] Search failed: {e}")
        return False
    
    # Test 5: Filter Patients
    print("\n5. Testing filter_patients()...")
    try:
        urgent_patients = service.filter_patients({'status': 1})
        print(f"   [OK] Found {len(urgent_patients)} urgent patient(s)")
    except Exception as e:
        print(f"   [ERROR] Filter failed: {e}")
        return False
    
    # Test 6: Get All Patients
    print("\n6. Testing get_all_patients()...")
    try:
        all_patients = service.get_all_patients()
        print(f"   [OK] Total patients in database: {len(all_patients)}")
    except Exception as e:
        print(f"   [ERROR] Get all failed: {e}")
        return False
    
    # Test 7: Validation Tests
    print("\n7. Testing validation...")
    try:
        # Test missing required field
        try:
            service.create_patient({'date_of_birth': '1990-01-01'})
            print("   [ERROR] Should have raised ValueError for missing name")
            return False
        except ValueError:
            print("   [OK] Correctly validates required fields")
        
        # Test invalid status
        try:
            service.create_patient({
                'full_name': 'Test',
                'date_of_birth': '1990-01-01',
                'status': 99  # Invalid
            })
            print("   [ERROR] Should have raised ValueError for invalid status")
            return False
        except ValueError:
            print("   [OK] Correctly validates status values")
            
    except Exception as e:
        print(f"   [ERROR] Validation test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All PatientService tests passed!")
    print("=" * 60)
    
    # Don't delete test patient - keep it for further testing
    print(f"\nNote: Test patient (ID: {patient_id}) kept in database for further testing")
    
    return True


if __name__ == "__main__":
    test_patient_service()
