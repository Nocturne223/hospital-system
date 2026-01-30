# Testing Guide - Hospital Management System

## Quick Start Testing

### Prerequisites Check

1. **MySQL Running**: Make sure XAMPP MySQL is started
2. **Database Ready**: Database `hospital_system` exists with tables
3. **Dependencies Installed**: `mysql-connector-python` installed

---

## Testing Methods

### Method 1: Run Test Suite (Recommended)

#### Test PatientService
```bash
python tests/test_patient_service.py
```

**What it tests**:
- ✅ Create patient
- ✅ Get patient
- ✅ Update patient
- ✅ Search patients
- ✅ Filter patients
- ✅ Validation

**Expected Output**:
```
[SUCCESS] All PatientService tests passed!
```

#### Test Database Connection
```bash
python test_mysql_connection.py
```

**What it tests**:
- ✅ Database connection
- ✅ Table creation
- ✅ Basic CRUD operations
- ✅ Foreign key constraints

---

### Method 2: Interactive Python Console

#### Quick Test in Python

1. **Open Python Console**:
```bash
python
```

2. **Run This Code**:
```python
import sys
sys.path.insert(0, 'src')

from database import DatabaseManager
from services.patient_service import PatientService
from config import USE_MYSQL, MYSQL_CONFIG

# Initialize
db = DatabaseManager(
    host=MYSQL_CONFIG['host'],
    user=MYSQL_CONFIG['user'],
    password=MYSQL_CONFIG['password'],
    database=MYSQL_CONFIG['database']
)

service = PatientService(db)

# Get all patients
patients = service.get_all_patients()
print(f"Total patients: {len(patients)}")

# View first patient
if patients:
    p = patients[0]
    print(f"\nFirst patient:")
    print(f"  Name: {p.full_name}")
    print(f"  Age: {p.age} years")
    print(f"  Status: {p.status_text}")
    print(f"  Phone: {p.phone_number}")

# Search
results = service.search_patients("John")
print(f"\nFound {len(results)} patients named 'John'")
```

---

### Method 3: Interactive Test Script

I'll create an interactive script you can run:

```bash
python interactive_test.py
```

---

### Method 4: View in Database Tools

#### phpMyAdmin
1. Open: http://localhost/phpmyadmin
2. Select: `hospital_system` database
3. Click: `patients` table
4. Browse: View all patient data

#### Navicat
1. Connect to MySQL
2. Open `hospital_system` database
3. Browse `patients` table
4. View/edit data directly

---

## Test Scenarios

### Scenario 1: Create a New Patient

```python
from src.database import DatabaseManager
from src.services.patient_service import PatientService
from src.config import USE_MYSQL, MYSQL_CONFIG

db = DatabaseManager(
    host=MYSQL_CONFIG['host'],
    user=MYSQL_CONFIG['user'],
    password=MYSQL_CONFIG['password'],
    database=MYSQL_CONFIG['database']
)
service = PatientService(db)

# Create patient
patient_data = {
    'full_name': 'Test Patient',
    'date_of_birth': '1995-06-20',
    'gender': 'Male',
    'phone_number': '555-1234',
    'email': 'test@email.com',
    'status': 0
}

patient_id = service.create_patient(patient_data)
print(f"Created patient with ID: {patient_id}")

# Verify
patient = service.get_patient(patient_id)
print(f"Patient: {patient.full_name}, Age: {patient.age}")
```

### Scenario 2: Search Patients

```python
# Search by name
results = service.search_patients("John")
for p in results:
    print(f"{p.full_name} - {p.phone_number} - {p.status_text}")

# Filter by status
urgent = service.get_patients_by_status(1)
print(f"Urgent patients: {len(urgent)}")
```

### Scenario 3: Update Patient

```python
# Update patient
update_data = {
    'phone_number': '555-9999',
    'status': 1  # Change to Urgent
}
service.update_patient(patient_id, update_data)

# Verify update
patient = service.get_patient(patient_id)
print(f"Updated phone: {patient.phone_number}")
print(f"Updated status: {patient.status_text}")
```

---

## Common Test Commands

### Quick Commands

```bash
# Test database connection
python test_mysql_connection.py

# Test PatientService
python tests/test_patient_service.py

# Add sample patients
python src/database/add_sample_patients.py

# View database
python src/database/view_db.py --table patients
```

---

## Troubleshooting Tests

### Issue: "ModuleNotFoundError"
**Solution**: Make sure you're in the project root directory

### Issue: "Can't connect to MySQL"
**Solution**: 
1. Check XAMPP MySQL is running
2. Verify credentials in `src/config.py`

### Issue: "Table doesn't exist"
**Solution**: 
1. Import schema: Run `test_mysql_connection.py` (it auto-creates tables)
2. Or import manually in phpMyAdmin

---

## Next Steps After Testing

1. ✅ Verify all tests pass
2. ✅ Check data in database
3. ✅ Test different scenarios
4. ⏳ Proceed to next feature (Specialization Management)

---

**Last Updated**: January 30, 2026
