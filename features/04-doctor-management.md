# Feature 4: Doctor Management

## Overview
Implement comprehensive doctor management system to handle doctor registration, profiles, specialization assignments, and availability management.

## Current State (POC)
- No doctor management in POC
- No doctor-specialization relationship

## Target State
- Complete doctor registration and profiles
- Doctor-specialization assignments
- Doctor availability management
- Doctor workload tracking
- Doctor performance metrics

## Requirements

### Functional Requirements

#### 4.1 Doctor Registration
- **Doctor Information Fields**:
  - Doctor ID (auto-generated, unique)
  - Full Name (required)
  - Title/Designation (Dr., Prof., etc.)
  - Specialization(s) (multiple selection)
  - License Number (required, unique)
  - Contact Information:
    - Phone Number
    - Email Address
    - Office Address
  - Qualifications:
    - Medical Degree
    - Years of Experience
    - Certifications
  - Status (Active/Inactive/On Leave)
  - Hire Date
  - Bio/Description

#### 4.2 Doctor Profile Management
- View complete doctor profile
- Edit doctor information
- Update specializations
- Update availability
- View doctor statistics

#### 4.3 Specialization Assignment
- Assign doctor to one or more specializations
- Remove doctor from specializations
- View all doctors in a specialization
- View all specializations for a doctor

#### 4.4 Availability Management
- Set working hours per day
- Set available days of week
- Mark unavailable dates (holidays, leave)
- View current availability status
- Set break times

#### 4.5 Doctor Statistics
- Patients served (today/week/month)
- Average consultation time
- Queue assignments
- Specialization workload
- Performance metrics

## Technical Implementation

### Database Schema

```sql
CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    title TEXT,
    license_number TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    email TEXT,
    office_address TEXT,
    medical_degree TEXT,
    years_of_experience INTEGER,
    certifications TEXT,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'On Leave')),
    bio TEXT,
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctor_availability (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    day_of_week INTEGER CHECK(day_of_week BETWEEN 0 AND 6), -- 0=Monday, 6=Sunday
    start_time TIME,
    end_time TIME,
    is_available INTEGER DEFAULT 1,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE doctor_unavailable_dates (
    unavailable_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    unavailable_date DATE NOT NULL,
    reason TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE INDEX idx_doctor_name ON doctors(full_name);
CREATE INDEX idx_doctor_license ON doctors(license_number);
CREATE INDEX idx_doctor_status ON doctors(status);
```

### Class Structure

```python
class Doctor:
    def __init__(self, doctor_id, full_name, license_number, ...):
        self.doctor_id = doctor_id
        self.full_name = full_name
        self.license_number = license_number
        # ... other attributes
    
    @property
    def specializations(self):
        # Get all assigned specializations
        pass
    
    @property
    def is_available_now(self):
        # Check if doctor is currently available
        pass
    
    @property
    def current_patients_count(self):
        # Get current number of patients assigned
        pass
```

### Service Layer

```python
class DoctorService:
    def create_doctor(self, doctor_data):
        # Create new doctor
        pass
    
    def get_doctor(self, doctor_id):
        # Get doctor by ID
        pass
    
    def get_all_doctors(self, active_only=False):
        # Get all doctors
        pass
    
    def update_doctor(self, doctor_id, doctor_data):
        # Update doctor information
        pass
    
    def delete_doctor(self, doctor_id):
        # Soft delete doctor
        pass
    
    def assign_specialization(self, doctor_id, specialization_id):
        # Assign doctor to specialization
        pass
    
    def remove_specialization(self, doctor_id, specialization_id):
        # Remove doctor from specialization
        pass
    
    def set_availability(self, doctor_id, availability_data):
        # Set doctor availability schedule
        pass
    
    def check_availability(self, doctor_id, date, time):
        # Check if doctor is available at specific time
        pass
    
    def get_doctor_statistics(self, doctor_id, date_range=None):
        # Get doctor statistics
        pass
```

### UI Components

1. **Doctor List View**
   - Table with all doctors
   - Status indicators
   - Specialization tags
   - Quick stats
   - Search and filter

2. **Doctor Registration Form**
   - Input fields for all information
   - Specialization multi-select
   - License validation
   - Save/Cancel buttons

3. **Doctor Profile View**
   - Complete doctor information
   - Assigned specializations
   - Availability calendar
   - Statistics dashboard
   - Edit mode

4. **Availability Management**
   - Weekly schedule view
   - Time slot selection
   - Unavailable dates calendar
   - Quick availability toggle

5. **Doctor Search & Filter**
   - Search by name, license, specialization
   - Filter by status, specialization
   - Sort options

## Implementation Steps

1. **Database Setup**
   - Create doctors table
   - Create doctor_availability table
   - Create doctor_unavailable_dates table
   - Set up relationships

2. **Model Implementation**
   - Create Doctor model
   - Add validation methods
   - Add availability checking logic

3. **Service Layer**
   - Implement DoctorService
   - Add CRUD operations
   - Implement availability management
   - Add statistics calculations

4. **UI Components**
   - Design doctor list view
   - Create registration form
   - Build profile view
   - Implement availability interface

5. **Integration**
   - Connect to specialization management
   - Connect to appointment system
   - Add to queue management

6. **Testing**
   - Unit tests for Doctor model
   - Unit tests for DoctorService
   - Availability logic tests
   - UI tests

## Acceptance Criteria

- [ ] Can create new doctor with all required fields
- [ ] Can view all doctors
- [ ] Can edit doctor information
- [ ] Can delete/deactivate doctor
- [ ] Can assign doctor to specializations
- [ ] Can remove doctor from specializations
- [ ] Can set doctor availability schedule
- [ ] Can mark unavailable dates
- [ ] Can check doctor availability
- [ ] Can view doctor statistics
- [ ] License number validation works
- [ ] Data persists to database

## Dependencies

- Database setup (Feature 8: Data Management)
- Specialization Management (Feature 2)

## Estimated Effort

- Database design: 3 hours
- Model implementation: 4 hours
- Service layer: 8 hours
- UI components: 14 hours
- Testing: 4 hours
- **Total: 33 hours**

## Notes

- Consider doctor photo upload
- Add doctor rating/review system (future)
- Implement doctor scheduling conflicts detection
- Add doctor workload balancing
- Consider doctor specialization levels (primary/secondary)
