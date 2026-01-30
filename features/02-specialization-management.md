# Feature 2: Enhanced Specialization Management

## Overview
Enhance the basic specialization management from the POC to support comprehensive specialization administration with capacity management, doctor assignments, and statistics.

## Current State (POC)
- Basic Specialization class with name and queue
- Fixed capacity of 10 patients
- No doctor assignment
- No statistics or analytics

## Target State
- Configurable specialization capacity
- Doctor assignment to specializations
- Specialization statistics and analytics
- Specialization description and details
- Active/inactive status management

## Requirements

### Functional Requirements

#### 2.1 Specialization CRUD Operations
- **Create Specialization**:
  - Name (required, unique)
  - Description
  - Maximum queue capacity (configurable, default: 10)
  - Active status (active/inactive)
  - Created date

- **Read Specialization**:
  - View specialization details
  - View assigned doctors
  - View current queue status
  - View statistics

- **Update Specialization**:
  - Edit name, description
  - Update capacity (with validation)
  - Toggle active status
  - Manage doctor assignments

- **Delete Specialization**:
  - Soft delete (mark as inactive)
  - Validation: Cannot delete if has active patients in queue
  - Validation: Cannot delete if has assigned doctors

#### 2.2 Capacity Management
- Set maximum queue capacity per specialization
- View current queue utilization
- Capacity warnings (e.g., 80% full)
- Prevent adding patients when at capacity

#### 2.3 Doctor Assignment
- Assign doctors to specializations
- Remove doctor assignments
- View all doctors in a specialization
- View all specializations for a doctor

#### 2.4 Specialization Statistics
- Current queue size
- Average queue wait time
- Total patients served
- Utilization percentage
- Peak hours analysis

## Technical Implementation

### Database Schema

```sql
CREATE TABLE specializations (
    specialization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    max_capacity INTEGER DEFAULT 10 CHECK(max_capacity > 0),
    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctor_specializations (
    doctor_id INTEGER,
    specialization_id INTEGER,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (doctor_id, specialization_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id)
);

CREATE INDEX idx_specialization_name ON specializations(name);
CREATE INDEX idx_specialization_active ON specializations(is_active);
```

### Class Structure

```python
class Specialization:
    def __init__(self, specialization_id, name, description, max_capacity, is_active):
        self.specialization_id = specialization_id
        self.name = name
        self.description = description
        self.max_capacity = max_capacity
        self.is_active = is_active
    
    @property
    def current_queue_size(self):
        # Get current number of patients in queue
        pass
    
    @property
    def utilization_percentage(self):
        # Calculate queue utilization
        pass
    
    @property
    def is_full(self):
        # Check if queue is at capacity
        pass
```

### Service Layer

```python
class SpecializationService:
    def create_specialization(self, specialization_data):
        # Create new specialization
        pass
    
    def get_specialization(self, specialization_id):
        # Get specialization by ID
        pass
    
    def get_all_specializations(self, active_only=False):
        # Get all specializations
        pass
    
    def update_specialization(self, specialization_id, specialization_data):
        # Update specialization
        pass
    
    def delete_specialization(self, specialization_id):
        # Soft delete specialization
        pass
    
    def assign_doctor(self, specialization_id, doctor_id):
        # Assign doctor to specialization
        pass
    
    def remove_doctor(self, specialization_id, doctor_id):
        # Remove doctor from specialization
        pass
    
    def get_specialization_statistics(self, specialization_id):
        # Get statistics for specialization
        pass
```

### UI Components

1. **Specialization List View**
   - Table with all specializations
   - Status indicators (active/inactive)
   - Capacity indicators
   - Quick stats display

2. **Specialization Form**
   - Create/Edit specialization
   - Input fields for all attributes
   - Capacity slider/input
   - Active status toggle

3. **Specialization Details View**
   - Full specialization information
   - Assigned doctors list
   - Current queue status
   - Statistics dashboard

4. **Doctor Assignment Dialog**
   - Select doctors to assign
   - View current assignments
   - Add/remove assignments

## Implementation Steps

1. **Database Setup**
   - Create specializations table
   - Create doctor_specializations junction table
   - Set up foreign keys and constraints

2. **Model Implementation**
   - Create Specialization model
   - Add validation methods
   - Add computed properties

3. **Service Layer**
   - Implement SpecializationService
   - Add CRUD operations
   - Implement doctor assignment logic
   - Add statistics calculation

4. **UI Components**
   - Design specialization list view
   - Create specialization form
   - Build details view
   - Implement assignment interface

5. **Integration**
   - Connect to queue management
   - Connect to doctor management
   - Add real-time updates

6. **Testing**
   - Unit tests for Specialization model
   - Unit tests for SpecializationService
   - Integration tests
   - UI tests

## Acceptance Criteria

- [ ] Can create new specialization with all fields
- [ ] Can view all specializations
- [ ] Can edit specialization details
- [ ] Can delete/deactivate specialization (with validations)
- [ ] Can set and update capacity
- [ ] Can assign doctors to specializations
- [ ] Can remove doctor assignments
- [ ] Can view specialization statistics
- [ ] Capacity validation works correctly
- [ ] UI shows real-time queue status
- [ ] Data persists to database

## Dependencies

- Database setup (Feature 8: Data Management)
- Doctor Management (Feature 4)
- Queue Management (Feature 3)

## Estimated Effort

- Database design: 2 hours
- Model implementation: 3 hours
- Service layer: 6 hours
- UI components: 10 hours
- Testing: 3 hours
- **Total: 24 hours**

## Notes

- Consider allowing multiple specializations per doctor
- Implement capacity warnings in UI
- Add bulk operations for doctor assignments
- Consider specialization categories/groups
