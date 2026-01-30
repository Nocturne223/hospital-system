# Feature 1: Enhanced Patient Management

## Overview
Transform the basic patient management from the POC into a comprehensive patient management system with full CRUD operations, search capabilities, and detailed patient profiles.

## Current State (POC)
- Basic Patient class with only `name` and `status` attributes
- No data persistence
- Limited patient information

## Target State
- Comprehensive patient profiles with multiple attributes
- Full CRUD operations (Create, Read, Update, Delete)
- Search and filtering capabilities
- Patient history tracking
- Data persistence in database

## Requirements

### Functional Requirements

#### 1.1 Patient Registration
- **Patient Information Fields**:
  - Patient ID (auto-generated, unique)
  - Full Name (required)
  - Date of Birth (required)
  - Gender (Male/Female/Other)
  - Contact Information:
    - Phone Number
    - Email Address
    - Address
  - Emergency Contact:
    - Name
    - Relationship
    - Phone Number
  - Medical Information:
    - Blood Type
    - Allergies
    - Medical History (text field)
  - Status (Normal/Urgent/Super-Urgent)
  - Registration Date (auto-generated)

- **Validation Rules**:
  - Name: Required, minimum 2 characters
  - Date of Birth: Valid date, not in future
  - Phone: Valid format
  - Email: Valid email format
  - Patient ID: Auto-generated, unique

#### 1.2 Patient Profile Management
- View complete patient profile
- Edit patient information
- Update patient status
- Add medical notes/history
- View patient visit history

#### 1.3 Patient Search & Filtering
- Search by:
  - Patient ID
  - Name (partial match)
  - Phone number
  - Email
- Filter by:
  - Status (Normal/Urgent/Super-Urgent)
  - Gender
  - Age range
  - Registration date range
- Sort by:
  - Name (A-Z, Z-A)
  - Registration date (newest/oldest)
  - Status priority

#### 1.4 Patient History
- Track all patient visits
- View appointment history
- View queue history
- View medical notes timeline

## Technical Implementation

### Database Schema

```sql
CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
    phone_number TEXT,
    email TEXT,
    address TEXT,
    emergency_contact_name TEXT,
    emergency_contact_relationship TEXT,
    emergency_contact_phone TEXT,
    blood_type TEXT,
    allergies TEXT,
    medical_history TEXT,
    status INTEGER DEFAULT 0 CHECK(status IN (0, 1, 2)),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_name ON patients(full_name);
CREATE INDEX idx_patient_phone ON patients(phone_number);
CREATE INDEX idx_patient_status ON patients(status);
```

### Class Structure

```python
class Patient:
    def __init__(self, patient_id, full_name, date_of_birth, ...):
        self.patient_id = patient_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        # ... other attributes
    
    @property
    def age(self):
        # Calculate age from date_of_birth
        pass
    
    def to_dict(self):
        # Convert to dictionary for serialization
        pass
```

### Service Layer

```python
class PatientService:
    def create_patient(self, patient_data):
        # Validate and create new patient
        pass
    
    def get_patient(self, patient_id):
        # Retrieve patient by ID
        pass
    
    def update_patient(self, patient_id, patient_data):
        # Update patient information
        pass
    
    def delete_patient(self, patient_id):
        # Soft delete or hard delete patient
        pass
    
    def search_patients(self, search_term):
        # Search patients by various criteria
        pass
    
    def filter_patients(self, filters):
        # Filter patients by criteria
        pass
```

### UI Components

1. **Patient Registration Form**
   - Input fields for all patient information
   - Validation feedback
   - Save/Cancel buttons

2. **Patient List View**
   - Table/grid display
   - Search bar
   - Filter options
   - Sort controls
   - Action buttons (View/Edit/Delete)

3. **Patient Profile View**
   - Display all patient information
   - Edit mode toggle
   - History timeline
   - Status indicator

4. **Patient Search Dialog**
   - Quick search interface
   - Advanced search options

## Implementation Steps

1. **Database Setup**
   - Create patients table
   - Create indexes
   - Set up relationships

2. **Model Implementation**
   - Create Patient model class
   - Add validation methods
   - Add helper methods (age calculation, etc.)

3. **Service Layer**
   - Implement PatientService
   - Add CRUD operations
   - Implement search and filter logic

4. **UI Components**
   - Design patient registration form
   - Create patient list view
   - Build patient profile view
   - Implement search interface

5. **Integration**
   - Connect UI to services
   - Add error handling
   - Implement user feedback

6. **Testing**
   - Unit tests for Patient model
   - Unit tests for PatientService
   - UI tests for forms
   - Integration tests

## Acceptance Criteria

- [ ] Can create new patient with all required fields
- [ ] Can view patient profile with all information
- [ ] Can edit patient information
- [ ] Can delete patient (with confirmation)
- [ ] Can search patients by name, ID, phone, email
- [ ] Can filter patients by status, gender, age
- [ ] Can sort patient list
- [ ] All validations work correctly
- [ ] Data persists to database
- [ ] UI is intuitive and responsive

## Dependencies

- Database setup (Feature 8: Data Management)
- UI framework setup (Feature 6: User Interface)

## Estimated Effort

- Database design: 2 hours
- Model implementation: 4 hours
- Service layer: 6 hours
- UI components: 12 hours
- Testing: 4 hours
- **Total: 28 hours**

## Notes

- Consider soft delete for patients to maintain history
- Implement pagination for large patient lists
- Add export functionality for patient data
- Consider privacy/security for patient information
