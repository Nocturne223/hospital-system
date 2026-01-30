# Hospital Management System - Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [System Layers](#system-layers)
4. [Design Patterns](#design-patterns)
5. [Database Design](#database-design)
6. [Class Structure](#class-structure)
7. [Component Interactions](#component-interactions)
8. [Technology Stack](#technology-stack)

---

## System Overview

### Architecture Type
The Hospital Management System follows a **Layered Architecture** (also known as N-Tier Architecture) with clear separation of concerns.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│                  (UI Components - PyQt6)                │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Business Logic Layer                     │
│                    (Services)                            │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   Data Access Layer                      │
│              (Database Manager - SQLite)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                    Database Layer                        │
│                  (SQLite Database)                       │
└──────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Dependency Inversion**: Upper layers depend on abstractions
3. **Single Responsibility**: Each class/module has one clear purpose
4. **Open/Closed Principle**: Open for extension, closed for modification

---

## Architecture Patterns

### 1. Layered Architecture

The system is organized into distinct layers:

#### Presentation Layer
- **Responsibility**: User interface and user interactions
- **Components**: PyQt6 widgets, windows, dialogs
- **Dependencies**: Business Logic Layer

#### Business Logic Layer
- **Responsibility**: Business rules and operations
- **Components**: Service classes (PatientService, QueueService, etc.)
- **Dependencies**: Data Access Layer

#### Data Access Layer
- **Responsibility**: Database operations
- **Components**: DatabaseManager, data models
- **Dependencies**: Database Layer

#### Database Layer
- **Responsibility**: Data storage
- **Components**: SQLite database, schema

### 2. Service Layer Pattern

Business logic is encapsulated in service classes:

```python
class PatientService:
    def create_patient(self, patient_data):
        # Validation
        # Business rules
        # Database operations
        pass
```

### 3. Repository Pattern (Implicit)

Database operations are abstracted through DatabaseManager:

```python
class DatabaseManager:
    def execute_query(self, query, params):
        # Database abstraction
        pass
```

---

## System Layers

### Presentation Layer

#### Components
- **Main Window**: Application entry point
- **Widgets**: Reusable UI components
- **Dialogs**: Modal windows for user input
- **Views**: Data display components

#### Responsibilities
- User input validation (UI level)
- Display data to users
- Handle user events
- Provide user feedback

#### Example Structure
```
src/ui/
├── main_window.py          # Main application window
├── widgets/
│   ├── patient_widget.py   # Patient management UI
│   ├── queue_widget.py     # Queue management UI
│   └── dashboard_widget.py # Dashboard UI
└── dialogs/
    ├── patient_dialog.py   # Patient form dialog
    └── appointment_dialog.py
```

### Business Logic Layer

#### Components
- **Service Classes**: Business logic encapsulation
- **Validators**: Data validation logic
- **Business Rules**: Domain-specific rules

#### Responsibilities
- Implement business rules
- Validate business logic
- Coordinate between UI and data layers
- Handle business exceptions

#### Example Structure
```
src/services/
├── patient_service.py      # Patient business logic
├── queue_service.py        # Queue business logic
├── doctor_service.py       # Doctor business logic
└── appointment_service.py  # Appointment business logic
```

### Data Access Layer

#### Components
- **DatabaseManager**: Database connection and operations
- **Models**: Data models representing database entities
- **Repositories**: Data access abstractions (if needed)

#### Responsibilities
- Database connection management
- CRUD operations
- Transaction management
- Data mapping

#### Example Structure
```
src/database/
├── db_manager.py           # Database manager
├── schema.sql              # Database schema
└── migrations/             # Database migrations

src/models/
├── patient.py              # Patient model
├── doctor.py                # Doctor model
└── specialization.py        # Specialization model
```

---

## Design Patterns

### 1. Singleton Pattern

**DatabaseManager** uses Singleton-like pattern (single instance per application):

```python
class DatabaseManager:
    def __init__(self, db_path='data/hospital_system.db'):
        # Single database connection
        pass
```

### 2. Factory Pattern

Used for creating UI components and service instances:

```python
class ServiceFactory:
    @staticmethod
    def create_patient_service():
        return PatientService(DatabaseManager())
```

### 3. Observer Pattern

Used for UI updates when data changes:

```python
# PyQt6 signals and slots
class QueueWidget(QWidget):
    queue_updated = pyqtSignal()
    
    def update_queue(self):
        self.queue_updated.emit()
```

### 4. Strategy Pattern

Used for different queue ordering strategies:

```python
class QueueOrderingStrategy:
    def order_patients(self, patients):
        pass

class PriorityQueueStrategy(QueueOrderingStrategy):
    def order_patients(self, patients):
        # Sort by priority
        pass
```

### 5. Repository Pattern

Database operations abstracted through DatabaseManager:

```python
# Implicit repository pattern
db = DatabaseManager()
patients = db.execute_query("SELECT * FROM patients")
```

---

## Database Design

### Schema Overview

The database follows **Third Normal Form (3NF)** with proper normalization:

#### Core Tables
1. **patients**: Patient information
2. **doctors**: Doctor information
3. **specializations**: Medical specializations
4. **doctor_specializations**: Many-to-many relationship
5. **queue_entries**: Queue management
6. **appointments**: Appointment scheduling
7. **users**: User accounts
8. **audit_logs**: System audit trail

### Relationships

```
patients (1) ──< (M) queue_entries
patients (1) ──< (M) appointments
doctors (1) ──< (M) appointments
specializations (1) ──< (M) queue_entries
specializations (1) ──< (M) appointments
doctors (M) ──< (M) specializations (via doctor_specializations)
```

### Data Integrity

- **Foreign Keys**: Enforced referential integrity
- **Check Constraints**: Validate data values
- **Unique Constraints**: Prevent duplicates
- **Not Null Constraints**: Ensure required data

---

## Class Structure

### Model Classes

```python
class Patient:
    """Patient data model"""
    def __init__(self, patient_id, full_name, date_of_birth, ...):
        self.patient_id = patient_id
        self.full_name = full_name
        # ... other attributes
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        pass
    
    def to_dict(self):
        """Convert to dictionary"""
        pass
```

### Service Classes

```python
class PatientService:
    """Business logic for patient management"""
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_patient(self, patient_data):
        """Create new patient with validation"""
        # Validate
        # Business rules
        # Save to database
        pass
    
    def get_patient(self, patient_id):
        """Retrieve patient by ID"""
        pass
    
    def search_patients(self, search_term):
        """Search patients"""
        pass
```

### UI Classes

```python
class PatientWidget(QWidget):
    """UI component for patient management"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.patient_service = PatientService(DatabaseManager())
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize UI components"""
        pass
    
    def on_add_patient(self):
        """Handle add patient action"""
        pass
```

---

## Component Interactions

### Adding a Patient Flow

```
User Input (UI)
    ↓
PatientWidget.on_add_patient()
    ↓
PatientService.create_patient()
    ↓
Validation (PatientService)
    ↓
DatabaseManager.execute_update()
    ↓
SQLite Database
    ↓
Success Response
    ↓
UI Update (PatientWidget)
```

### Queue Processing Flow

```
User Action (UI)
    ↓
QueueWidget.get_next_patient()
    ↓
QueueService.get_next_patient()
    ↓
Database Query (DatabaseManager)
    ↓
Business Logic (QueueService)
    ↓
Database Update (DatabaseManager)
    ↓
UI Refresh (QueueWidget)
```

---

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Database**: SQLite 3
- **ORM**: None (direct SQL with DatabaseManager)

### Frontend
- **Framework**: PyQt6
- **UI Design**: Custom widgets and layouts
- **Styling**: QStyleSheet (CSS-like)

### Development Tools
- **Version Control**: Git
- **Testing**: pytest
- **Code Quality**: PEP 8 compliance

### Dependencies
```
PyQt6>=6.5.0
pytest>=7.4.0
python-dateutil>=2.8.2
```

---

## SOLID Principles Application

### Single Responsibility Principle (SRP)
- Each class has one clear responsibility
- PatientService handles patient logic only
- DatabaseManager handles database operations only

### Open/Closed Principle (OCP)
- Services can be extended without modification
- New features added through inheritance or composition

### Liskov Substitution Principle (LSP)
- Subclasses can replace base classes
- Interface implementations are interchangeable

### Interface Segregation Principle (ISP)
- Clients depend only on interfaces they use
- Services expose only necessary methods

### Dependency Inversion Principle (DIP)
- High-level modules don't depend on low-level modules
- Both depend on abstractions
- Services depend on DatabaseManager abstraction

---

## Security Architecture

### Authentication
- User login with username/password
- Password hashing (bcrypt/argon2)
- Session management

### Authorization
- Role-based access control (RBAC)
- Permission checks at service layer
- UI elements hidden based on role

### Data Security
- SQL injection prevention (parameterized queries)
- Input validation at multiple layers
- Audit logging for sensitive operations

---

## Performance Considerations

### Database Optimization
- Indexes on frequently queried columns
- Efficient queries with proper joins
- Connection pooling (if needed)

### UI Responsiveness
- Asynchronous operations for long tasks
- Progress indicators
- Background processing

### Caching Strategy
- In-memory caching for frequently accessed data
- Cache invalidation on updates

---

## Scalability

### Current Design
- Single-user or small team usage
- SQLite database (file-based)
- Desktop application

### Future Scalability Options
- Migrate to PostgreSQL/MySQL for multi-user
- Add web interface
- Implement microservices architecture
- Add load balancing

---

## Extension Points

### Adding New Features
1. Create model class in `src/models/`
2. Create service class in `src/services/`
3. Create UI component in `src/ui/`
4. Update database schema if needed
5. Add tests

### Adding New Reports
1. Create report service
2. Add UI component
3. Implement export functionality

---

## Conclusion

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Maintainable code structure
- ✅ Extensible design
- ✅ Testable components
- ✅ Professional software engineering practices

**Last Updated**: January 30, 2026  
**Version**: 1.0
