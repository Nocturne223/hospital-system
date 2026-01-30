# Next Steps Roadmap - Hospital Management System

## Current Status ✅

- [x] Database foundation complete (Feature 8)
- [x] MySQL database set up and tested
- [x] All tables created
- [x] Database connection working
- [x] Documentation structure complete

---

## Immediate Next Steps

### Step 1: Update Application to Use MySQL (30 minutes)

**Goal**: Switch from SQLite to MySQL in your application code.

#### 1.1 Create Configuration File

Create `src/config.py`:

```python
"""
Configuration file for Hospital Management System
"""

# Database Configuration
USE_MYSQL = True  # Set to False to use SQLite

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Empty for default XAMPP
    'database': 'hospital_system'
}

# SQLite Configuration (if needed)
SQLITE_CONFIG = {
    'db_path': 'data/hospital_system.db'
}
```

#### 1.2 Update Database Imports

Update `src/database/__init__.py`:

```python
"""
Database package for Hospital Management System.
"""

from src.config import USE_MYSQL

if USE_MYSQL:
    from .mysql_db_manager import MySQLDatabaseManager as DatabaseManager
else:
    from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
```

#### 1.3 Update Database Initialization

Update any code that creates DatabaseManager:

```python
from src.database import DatabaseManager
from src.config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG

if USE_MYSQL:
    db = DatabaseManager(**MYSQL_CONFIG)
else:
    db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])
```

**Test**: Run your test script again to verify everything works.

---

### Step 2: Create Model Classes (2-3 hours)

**Goal**: Create data model classes that represent database entities.

#### 2.1 Create Patient Model

Create `src/models/patient.py`:

```python
"""
Patient Model
"""

from datetime import date
from typing import Optional

class Patient:
    """Represents a patient in the hospital management system."""
    
    def __init__(self, patient_id: int, full_name: str, 
                 date_of_birth: date, status: int = 0,
                 gender: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 email: Optional[str] = None,
                 **kwargs):
        self.patient_id = patient_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.status = status
        self.gender = gender
        self.phone_number = phone_number
        self.email = email
        # Add other attributes as needed
    
    @property
    def age(self) -> int:
        """Calculate patient's age."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < 
            (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def to_dict(self) -> dict:
        """Convert patient to dictionary."""
        return {
            'patient_id': self.patient_id,
            'full_name': self.full_name,
            'date_of_birth': str(self.date_of_birth),
            'status': self.status,
            'gender': self.gender,
            # ... other fields
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Patient':
        """Create Patient from dictionary."""
        return Patient(**data)
```

#### 2.2 Create Other Models

Create similar model classes for:
- `src/models/doctor.py`
- `src/models/specialization.py`
- `src/models/appointment.py`
- `src/models/queue_entry.py`

**Priority**: Start with Patient and Specialization models first.

---

### Step 3: Create Service Layer (4-6 hours)

**Goal**: Implement business logic services that interact with the database.

#### 3.1 Create PatientService

Create `src/services/patient_service.py`:

```python
"""
Patient Service - Business logic for patient management
"""

from typing import List, Optional, Dict
from src.database import DatabaseManager
from src.models.patient import Patient
from datetime import date

class PatientService:
    """Service class for patient management operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_patient(self, patient_data: dict) -> int:
        """
        Create a new patient.
        
        Args:
            patient_data: Dictionary with patient information
        
        Returns:
            Patient ID
        """
        # Validation
        if not patient_data.get('full_name'):
            raise ValueError("Full name is required")
        if not patient_data.get('date_of_birth'):
            raise ValueError("Date of birth is required")
        
        # Build query
        query = """
            INSERT INTO patients 
            (full_name, date_of_birth, gender, phone_number, email, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            patient_data['full_name'],
            patient_data['date_of_birth'],
            patient_data.get('gender'),
            patient_data.get('phone_number'),
            patient_data.get('email'),
            patient_data.get('status', 0)
        )
        
        self.db.execute_update(query, params)
        return self.db.get_last_insert_id()
    
    def get_patient(self, patient_id: int) -> Optional[dict]:
        """Get patient by ID."""
        query = "SELECT * FROM patients WHERE patient_id = %s"
        results = self.db.execute_query(query, (patient_id,))
        return dict(results[0]) if results else None
    
    def search_patients(self, search_term: str) -> List[dict]:
        """Search patients by name, phone, or email."""
        query = """
            SELECT * FROM patients 
            WHERE full_name LIKE %s 
               OR phone_number LIKE %s 
               OR email LIKE %s
        """
        search_pattern = f"%{search_term}%"
        results = self.db.execute_query(
            query, 
            (search_pattern, search_pattern, search_pattern)
        )
        return [dict(row) for row in results]
    
    # Add more methods: update_patient, delete_patient, etc.
```

#### 3.2 Create Other Services

Create service classes for:
- `src/services/specialization_service.py`
- `src/services/queue_service.py`
- `src/services/doctor_service.py` (later)
- `src/services/appointment_service.py` (later)

**Priority**: PatientService and QueueService first.

---

### Step 4: Test Services (1-2 hours)

**Goal**: Create and run tests for your services.

#### 4.1 Create Test Script

Create `tests/test_patient_service.py`:

```python
"""Test PatientService"""

from src.database import DatabaseManager
from src.services.patient_service import PatientService
from src.config import USE_MYSQL, MYSQL_CONFIG

def test_patient_service():
    """Test patient service operations"""
    # Initialize
    db = DatabaseManager(**MYSQL_CONFIG) if USE_MYSQL else DatabaseManager()
    service = PatientService(db)
    
    # Test create
    patient_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1990-01-01',
        'gender': 'Male',
        'status': 0
    }
    patient_id = service.create_patient(patient_data)
    print(f"Created patient with ID: {patient_id}")
    
    # Test get
    patient = service.get_patient(patient_id)
    print(f"Retrieved patient: {patient['full_name']}")
    
    # Test search
    results = service.search_patients("Test")
    print(f"Found {len(results)} patients")
    
    # Clean up
    # service.delete_patient(patient_id)

if __name__ == "__main__":
    test_patient_service()
```

---

### Step 5: Implement Feature 1 - Enhanced Patient Management (6-8 hours)

**Goal**: Complete patient management with full CRUD operations.

#### Tasks:
1. ✅ Patient model created
2. ✅ PatientService created
3. [ ] Add validation logic
4. [ ] Add search and filtering
5. [ ] Add patient history tracking
6. [ ] Create unit tests
7. [ ] Test all operations

**Reference**: `features/01-patient-management.md`

---

### Step 6: Implement Feature 2 - Enhanced Specialization Management (4-6 hours)

**Goal**: Complete specialization management.

#### Tasks:
1. [ ] Specialization model
2. [ ] SpecializationService
3. [ ] Capacity management
4. [ ] Doctor assignment
5. [ ] Tests

**Reference**: `features/02-specialization-management.md`

---

### Step 7: Implement Feature 3 - Enhanced Queue Management (6-8 hours)

**Goal**: Complete queue management with priority ordering.

#### Tasks:
1. [ ] QueueService
2. [ ] Priority-based ordering
3. [ ] Queue capacity management
4. [ ] Queue position tracking
5. [ ] Tests

**Reference**: `features/03-queue-management.md`

---

## Development Workflow

### Daily Workflow

1. **Morning**:
   - Review what you did yesterday
   - Plan today's tasks
   - Check for any issues

2. **Development**:
   - Work on assigned feature
   - Write code following standards
   - Test as you go
   - Commit frequently

3. **End of Day**:
   - Test your changes
   - Commit your work
   - Update progress notes

### Code Organization

```
src/
├── models/          # Data models (Patient, Doctor, etc.)
├── services/        # Business logic (PatientService, etc.)
├── database/         # Database layer (✅ Done)
├── ui/              # User interface (Later)
└── utils/           # Utilities (validators, helpers)
```

---

## Recommended Implementation Order

### Week 1: Foundation
1. ✅ Database setup (DONE)
2. ⏳ Update to MySQL (30 min)
3. ⏳ Create model classes (2-3 hours)
4. ⏳ Create service layer (4-6 hours)
5. ⏳ Test services (1-2 hours)

### Week 2: Core Features
1. ⏳ Feature 1: Patient Management (6-8 hours)
2. ⏳ Feature 2: Specialization Management (4-6 hours)
3. ⏳ Feature 3: Queue Management (6-8 hours)

### Week 3: Advanced Features
1. ⏳ Feature 4: Doctor Management
2. ⏳ Feature 5: Appointment System

### Week 4: UI Development
1. ⏳ Feature 6: User Interface (PyQt6)
2. ⏳ Connect UI to services
3. ⏳ Testing and refinement

---

## Quick Start: Next 2 Hours

### Immediate Actions (Right Now)

1. **Create config.py** (5 minutes)
   - File: `src/config.py`
   - Set USE_MYSQL = True

2. **Update database imports** (5 minutes)
   - File: `src/database/__init__.py`
   - Add conditional import

3. **Create Patient Model** (30 minutes)
   - File: `src/models/patient.py`
   - Basic structure with to_dict, from_dict

4. **Create PatientService** (1 hour)
   - File: `src/services/patient_service.py`
   - Implement create_patient, get_patient, search_patients

5. **Test PatientService** (20 minutes)
   - Create test script
   - Test create, get, search operations

---

## Testing Strategy

### As You Develop

1. **Unit Tests**: Test each method individually
2. **Integration Tests**: Test service + database
3. **Manual Testing**: Test in Python console
4. **Edge Cases**: Test error conditions

### Test Checklist

For each service method:
- [ ] Happy path (normal operation)
- [ ] Invalid input (validation)
- [ ] Edge cases (empty, null, etc.)
- [ ] Error handling

---

## Code Quality Checklist

As you write code:

- [ ] Follow PEP 8 style guide
- [ ] Add docstrings to all classes/methods
- [ ] Use type hints
- [ ] Handle errors properly
- [ ] Validate inputs
- [ ] Write comments for complex logic
- [ ] Keep functions small and focused

---

## Resources

### Documentation
- Feature specs: `features/` directory
- Architecture: `docs/documentation/ARCHITECTURE.md`
- API docs: `docs/documentation/API_DOCUMENTATION.md`
- Code standards: `docs/documentation/CODE_DOCUMENTATION.md`

### Reference
- MySQL syntax: Use `%s` for parameters
- Database schema: `src/database/schema_mysql.sql`
- Test examples: `tests/test_database.py`

---

## Getting Help

### If Stuck

1. **Review Documentation**: Check feature specs and architecture docs
2. **Check Examples**: Look at existing code (DatabaseManager)
3. **Test Incrementally**: Test small pieces at a time
4. **Debug**: Use print statements or debugger
5. **Ask Questions**: Document what you tried

### Common Issues

**MySQL Connection Issues**:
- Check XAMPP MySQL is running
- Verify credentials
- Test with test_mysql_connection.py

**Import Errors**:
- Check Python path
- Verify __init__.py files exist
- Check module names

**SQL Errors**:
- Use `%s` for MySQL parameters (not `?`)
- Check table/column names
- Verify data types

---

## Progress Tracking

### Track Your Progress

Create a simple progress file or use checkboxes:

```markdown
## Implementation Progress

### Foundation ✅
- [x] Database setup
- [x] MySQL connection
- [ ] Config file
- [ ] Model classes
- [ ] Service classes

### Features
- [ ] Feature 1: Patient Management
- [ ] Feature 2: Specialization Management
- [ ] Feature 3: Queue Management
- [ ] Feature 4: Doctor Management
- [ ] Feature 5: Appointment System
- [ ] Feature 6: UI
```

---

## Next Immediate Action

**Start Here**: Create `src/config.py` and update database imports.

Then move to creating model classes, starting with the Patient model.

**Estimated Time for Next Steps**:
- Config setup: 10 minutes
- Patient Model: 30 minutes
- PatientService: 1-2 hours
- Testing: 30 minutes

**Total**: ~3-4 hours to get Patient Management working

---

**Last Updated**: January 30, 2026  
**Status**: Ready to proceed with implementation
