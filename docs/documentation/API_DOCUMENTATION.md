# Hospital Management System - API Documentation

## Overview

This document describes the Service Layer API for the Hospital Management System. The API provides business logic methods for all system operations.

**Note**: This is a desktop application with service layer APIs, not a REST API.

---

## Table of Contents

1. [DatabaseManager API](#databasemanager-api)
2. [PatientService API](#patientservice-api)
3. [QueueService API](#queueservice-api)
4. [DoctorService API](#doctorservice-api)
5. [AppointmentService API](#appointmentservice-api)
6. [SpecializationService API](#specializationservice-api)
7. [Error Handling](#error-handling)

---

## DatabaseManager API

### Class: `DatabaseManager`

Manages database connections and operations.

#### Constructor

```python
DatabaseManager(db_path: str = 'data/hospital_system.db')
```

**Parameters:**
- `db_path` (str): Path to SQLite database file

**Returns:** DatabaseManager instance

**Example:**
```python
from src.database import DatabaseManager

db = DatabaseManager('data/hospital_system.db')
```

#### Methods

##### `execute_query(query: str, params: tuple = ()) -> List[sqlite3.Row]`

Execute a SELECT query and return results.

**Parameters:**
- `query` (str): SQL SELECT query
- `params` (tuple): Query parameters

**Returns:** List of Row objects (dictionary-like)

**Example:**
```python
results = db.execute_query(
    "SELECT * FROM patients WHERE status = ?",
    (1,)
)
for row in results:
    print(row['full_name'])
```

##### `execute_update(query: str, params: tuple = ()) -> int`

Execute INSERT, UPDATE, or DELETE query.

**Parameters:**
- `query` (str): SQL query
- `params` (tuple): Query parameters

**Returns:** Number of rows affected

**Example:**
```python
rows_affected = db.execute_update(
    "INSERT INTO patients (full_name, date_of_birth) VALUES (?, ?)",
    ("John Doe", "1990-01-01")
)
```

##### `get_connection() -> contextmanager`

Get database connection with context manager.

**Returns:** Connection context manager

**Example:**
```python
with db.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    results = cursor.fetchall()
```

##### `backup_database(backup_path: Optional[str] = None) -> str`

Create database backup.

**Parameters:**
- `backup_path` (str, optional): Custom backup path

**Returns:** Path to backup file

**Example:**
```python
backup_path = db.backup_database()
```

---

## PatientService API

### Class: `PatientService`

Business logic for patient management.

#### Constructor

```python
PatientService(db_manager: DatabaseManager)
```

**Parameters:**
- `db_manager` (DatabaseManager): Database manager instance

#### Methods

##### `create_patient(patient_data: dict) -> int`

Create a new patient.

**Parameters:**
- `patient_data` (dict): Patient information
  ```python
  {
      'full_name': str,
      'date_of_birth': str,  # YYYY-MM-DD
      'gender': str,  # 'Male', 'Female', 'Other'
      'phone_number': str,
      'email': str,
      'address': str,
      'emergency_contact_name': str,
      'emergency_contact_relationship': str,
      'emergency_contact_phone': str,
      'blood_type': str,
      'allergies': str,
      'medical_history': str,
      'status': int  # 0=Normal, 1=Urgent, 2=Super-Urgent
  }
  ```

**Returns:** Patient ID (int)

**Raises:** ValueError if validation fails

**Example:**
```python
from src.services.patient_service import PatientService

service = PatientService(DatabaseManager())
patient_id = service.create_patient({
    'full_name': 'John Doe',
    'date_of_birth': '1990-01-01',
    'gender': 'Male',
    'status': 0
})
```

##### `get_patient(patient_id: int) -> Optional[dict]`

Get patient by ID.

**Parameters:**
- `patient_id` (int): Patient ID

**Returns:** Patient data dictionary or None

**Example:**
```python
patient = service.get_patient(1)
if patient:
    print(patient['full_name'])
```

##### `update_patient(patient_id: int, patient_data: dict) -> bool`

Update patient information.

**Parameters:**
- `patient_id` (int): Patient ID
- `patient_data` (dict): Updated patient data

**Returns:** True if successful

**Example:**
```python
success = service.update_patient(1, {
    'phone_number': '555-9999',
    'status': 1
})
```

##### `delete_patient(patient_id: int) -> bool`

Delete a patient.

**Parameters:**
- `patient_id` (int): Patient ID

**Returns:** True if successful

**Warning:** This deletes all related records (queue entries, appointments)

##### `search_patients(search_term: str) -> List[dict]`

Search patients by name, phone, or email.

**Parameters:**
- `search_term` (str): Search keyword

**Returns:** List of matching patients

**Example:**
```python
results = service.search_patients("John")
```

##### `filter_patients(filters: dict) -> List[dict]`

Filter patients by criteria.

**Parameters:**
- `filters` (dict): Filter criteria
  ```python
  {
      'status': int,
      'gender': str,
      'min_age': int,
      'max_age': int
  }
  ```

**Returns:** List of filtered patients

---

## QueueService API

### Class: `QueueService`

Business logic for queue management.

#### Methods

##### `add_to_queue(patient_id: int, specialization_id: int) -> int`

Add patient to queue.

**Parameters:**
- `patient_id` (int): Patient ID
- `specialization_id` (int): Specialization ID

**Returns:** Queue entry ID

**Raises:** ValueError if queue is full

**Example:**
```python
from src.services.queue_service import QueueService

queue_service = QueueService(DatabaseManager())
entry_id = queue_service.add_to_queue(patient_id=1, specialization_id=1)
```

##### `get_next_patient(specialization_id: int) -> Optional[dict]`

Get next patient from queue (highest priority).

**Parameters:**
- `specialization_id` (int): Specialization ID

**Returns:** Patient data dictionary or None

**Example:**
```python
next_patient = queue_service.get_next_patient(specialization_id=1)
if next_patient:
    print(f"Next: {next_patient['full_name']}")
```

##### `get_queue(specialization_id: int) -> List[dict]`

Get all patients in queue for specialization.

**Parameters:**
- `specialization_id` (int): Specialization ID

**Returns:** List of queue entries with patient data

**Example:**
```python
queue = queue_service.get_queue(specialization_id=1)
for entry in queue:
    print(f"{entry['position']}: {entry['patient_name']} - {entry['status']}")
```

##### `remove_from_queue(queue_entry_id: int, reason: str = None) -> bool`

Remove patient from queue.

**Parameters:**
- `queue_entry_id` (int): Queue entry ID
- `reason` (str, optional): Removal reason

**Returns:** True if successful

##### `get_queue_status(specialization_id: int) -> dict`

Get queue status and statistics.

**Parameters:**
- `specialization_id` (int): Specialization ID

**Returns:** Status dictionary
```python
{
    'current_count': int,
    'max_capacity': int,
    'available_slots': int,
    'urgent_count': int,
    'normal_count': int
}
```

---

## DoctorService API

### Class: `DoctorService`

Business logic for doctor management.

#### Methods

##### `create_doctor(doctor_data: dict) -> int`

Create a new doctor.

**Parameters:**
- `doctor_data` (dict): Doctor information
  ```python
  {
      'full_name': str,
      'title': str,
      'license_number': str,  # Must be unique
      'phone_number': str,
      'email': str,
      'office_address': str,
      'medical_degree': str,
      'years_of_experience': int,
      'certifications': str,
      'status': str,  # 'Active', 'Inactive', 'On Leave'
      'bio': str,
      'hire_date': str  # YYYY-MM-DD
  }
  ```

**Returns:** Doctor ID

##### `assign_to_specialization(doctor_id: int, specialization_id: int) -> bool`

Assign doctor to specialization.

**Parameters:**
- `doctor_id` (int): Doctor ID
- `specialization_id` (int): Specialization ID

**Returns:** True if successful

##### `get_doctors_by_specialization(specialization_id: int) -> List[dict]`

Get all doctors assigned to a specialization.

**Parameters:**
- `specialization_id` (int): Specialization ID

**Returns:** List of doctor dictionaries

---

## AppointmentService API

### Class: `AppointmentService`

Business logic for appointment management.

#### Methods

##### `schedule_appointment(appointment_data: dict) -> int`

Schedule a new appointment.

**Parameters:**
- `appointment_data` (dict): Appointment information
  ```python
  {
      'patient_id': int,
      'doctor_id': int,
      'specialization_id': int,
      'appointment_date': str,  # YYYY-MM-DD
      'appointment_time': str,  # HH:MM
      'duration': int,  # minutes
      'appointment_type': str,  # 'Regular', 'Follow-up', 'Emergency'
      'reason': str,
      'notes': str
  }
  ```

**Returns:** Appointment ID

**Raises:** ValueError if conflict detected

##### `get_appointments_by_date(date: str) -> List[dict]`

Get appointments for a specific date.

**Parameters:**
- `date` (str): Date in YYYY-MM-DD format

**Returns:** List of appointment dictionaries

##### `cancel_appointment(appointment_id: int, reason: str) -> bool`

Cancel an appointment.

**Parameters:**
- `appointment_id` (int): Appointment ID
- `reason` (str): Cancellation reason

**Returns:** True if successful

---

## SpecializationService API

### Class: `SpecializationService`

Business logic for specialization management.

#### Methods

##### `create_specialization(specialization_data: dict) -> int`

Create a new specialization.

**Parameters:**
- `specialization_data` (dict):
  ```python
  {
      'name': str,  # Must be unique
      'description': str,
      'max_capacity': int
  }
  ```

**Returns:** Specialization ID

##### `get_all_specializations() -> List[dict]`

Get all specializations.

**Returns:** List of specialization dictionaries

##### `update_capacity(specialization_id: int, max_capacity: int) -> bool`

Update maximum queue capacity.

**Parameters:**
- `specialization_id` (int): Specialization ID
- `max_capacity` (int): New maximum capacity

**Returns:** True if successful

---

## Error Handling

### Exception Types

#### `DatabaseError`
Raised for database operation failures.

```python
try:
    db.execute_update("INSERT INTO patients ...")
except DatabaseError as e:
    print(f"Database error: {e}")
```

#### `ValidationError`
Raised when input validation fails.

```python
try:
    service.create_patient(invalid_data)
except ValidationError as e:
    print(f"Validation error: {e}")
```

#### `BusinessRuleError`
Raised when business rules are violated.

```python
try:
    queue_service.add_to_queue(patient_id, specialization_id)
except BusinessRuleError as e:
    print(f"Business rule violation: {e}")
```

### Error Response Format

All service methods that can fail return appropriate exceptions with descriptive messages.

---

## Usage Examples

### Complete Patient Registration Flow

```python
from src.database import DatabaseManager
from src.services.patient_service import PatientService

# Initialize
db = DatabaseManager()
patient_service = PatientService(db)

# Create patient
patient_data = {
    'full_name': 'Jane Smith',
    'date_of_birth': '1990-05-15',
    'gender': 'Female',
    'phone_number': '555-1234',
    'email': 'jane@email.com',
    'status': 0
}

try:
    patient_id = patient_service.create_patient(patient_data)
    print(f"Patient created with ID: {patient_id}")
except ValidationError as e:
    print(f"Error: {e}")
```

### Queue Management Flow

```python
from src.services.queue_service import QueueService

queue_service = QueueService(db)

# Add to queue
entry_id = queue_service.add_to_queue(patient_id=1, specialization_id=1)

# Get queue status
status = queue_service.get_queue_status(specialization_id=1)
print(f"Queue: {status['current_count']}/{status['max_capacity']}")

# Get next patient
next_patient = queue_service.get_next_patient(specialization_id=1)
if next_patient:
    print(f"Next: {next_patient['full_name']}")
```

---

## API Versioning

**Current Version**: 1.0  
**Last Updated**: January 30, 2026

---

**Note**: This API documentation covers the service layer. For database schema details, see [Architecture Documentation](ARCHITECTURE.md).
