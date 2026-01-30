# Hospital Management System - Design Documents

## Document Information

**Project**: Hospital Management System  
**Version**: 1.0  
**Date**: January 30, 2026  
**Status**: Complete

---

## Table of Contents

1. [System Design Overview](#system-design-overview)
2. [Architecture Design](#architecture-design)
3. [Database Design](#database-design)
4. [Class Design](#class-design)
5. [User Interface Design](#user-interface-design)
6. [Design Patterns](#design-patterns)
7. [UML Diagrams](#uml-diagrams)
8. [Design Decisions](#design-decisions)

---

## System Design Overview

### Design Philosophy

The Hospital Management System follows these design principles:
- **Separation of Concerns**: Clear layer boundaries
- **Single Responsibility**: Each class has one purpose
- **Open/Closed Principle**: Open for extension, closed for modification
- **Dependency Inversion**: Depend on abstractions
- **DRY (Don't Repeat Yourself)**: Reusable components

### System Architecture

The system uses a **Layered Architecture** with three main layers:

```
┌─────────────────────────────────────┐
│      Presentation Layer (UI)        │
│         PyQt6 Components             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Business Logic Layer (Services)  │
│    PatientService, QueueService, etc.│
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Data Access Layer (Database)     │
│        DatabaseManager               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Database (SQLite)           │
└─────────────────────────────────────┘
```

---

## Architecture Design

### Layer Responsibilities

#### Presentation Layer
- **Purpose**: User interface and user interactions
- **Components**: Windows, widgets, dialogs
- **Responsibilities**:
  - Display data to users
  - Capture user input
  - Validate input at UI level
  - Provide user feedback

#### Business Logic Layer
- **Purpose**: Business rules and operations
- **Components**: Service classes
- **Responsibilities**:
  - Implement business logic
  - Validate business rules
  - Coordinate between UI and data layers
  - Handle business exceptions

#### Data Access Layer
- **Purpose**: Database operations
- **Components**: DatabaseManager, models
- **Responsibilities**:
  - Database connection management
  - CRUD operations
  - Transaction management
  - Data mapping

### Data Flow

```
User Action
    ↓
UI Component
    ↓
Service Layer (Business Logic)
    ↓
Database Manager
    ↓
SQLite Database
    ↓
Response (reverse flow)
```

---

## Database Design

### Entity-Relationship Model

#### Core Entities

1. **Patient**
   - Attributes: patient_id, full_name, date_of_birth, gender, status, etc.
   - Relationships: One-to-Many with QueueEntries, Appointments

2. **Doctor**
   - Attributes: doctor_id, full_name, license_number, etc.
   - Relationships: Many-to-Many with Specializations, One-to-Many with Appointments

3. **Specialization**
   - Attributes: specialization_id, name, max_capacity, etc.
   - Relationships: Many-to-Many with Doctors, One-to-Many with QueueEntries

4. **QueueEntry**
   - Attributes: queue_entry_id, patient_id, specialization_id, status, position
   - Relationships: Many-to-One with Patient, Many-to-One with Specialization

5. **Appointment**
   - Attributes: appointment_id, patient_id, doctor_id, date, time, status
   - Relationships: Many-to-One with Patient, Doctor, Specialization

### Database Schema

See `src/database/schema.sql` for complete schema definition.

### Normalization

The database follows **Third Normal Form (3NF)**:
- No redundant data
- Proper foreign key relationships
- Appropriate indexes for performance

---

## Class Design

### Model Classes

#### Patient Model
```python
class Patient:
    """Patient data model"""
    - patient_id: int
    - full_name: str
    - date_of_birth: date
    - gender: str
    - status: int
    - phone_number: str
    - email: str
    + age: property
    + to_dict(): dict
```

#### Doctor Model
```python
class Doctor:
    """Doctor data model"""
    - doctor_id: int
    - full_name: str
    - license_number: str
    - status: str
    + to_dict(): dict
```

### Service Classes

#### PatientService
```python
class PatientService:
    """Patient business logic"""
    - db_manager: DatabaseManager
    + create_patient(data: dict) -> int
    + get_patient(id: int) -> dict
    + update_patient(id: int, data: dict) -> bool
    + delete_patient(id: int) -> bool
    + search_patients(term: str) -> List[dict]
```

#### QueueService
```python
class QueueService:
    """Queue business logic"""
    - db_manager: DatabaseManager
    + add_to_queue(patient_id: int, spec_id: int) -> int
    + get_next_patient(spec_id: int) -> dict
    + get_queue(spec_id: int) -> List[dict]
    + remove_from_queue(entry_id: int) -> bool
```

### UI Classes

#### MainWindow
```python
class MainWindow(QMainWindow):
    """Main application window"""
    - menu_bar: QMenuBar
    - status_bar: QStatusBar
    - central_widget: QWidget
    + setup_ui()
    + setup_menu()
```

#### PatientWidget
```python
class PatientWidget(QWidget):
    """Patient management UI"""
    - patient_service: PatientService
    - table: QTableWidget
    + setup_ui()
    + on_add_patient()
    + on_search()
```

---

## User Interface Design

### Design Principles

1. **Consistency**: Uniform design language
2. **Clarity**: Clear visual hierarchy
3. **Efficiency**: Minimal clicks to complete tasks
4. **Feedback**: Clear response to user actions

### Layout Structure

```
┌─────────────────────────────────────────┐
│  Menu Bar (File, Edit, View, Help)      │
├─────────────────────────────────────────┤
│  Toolbar (Quick Actions)                │
├─────────────────────────────────────────┤
│                                          │
│  Main Content Area                      │
│  (Tabs/Views for different features)     │
│                                          │
│                                          │
├─────────────────────────────────────────┤
│  Status Bar (Status, Notifications)      │
└─────────────────────────────────────────┘
```

### Color Scheme

- **Primary**: Professional blue (#2C3E50)
- **Secondary**: Light gray (#ECF0F1)
- **Success**: Green (#27AE60)
- **Warning**: Orange (#F39C12)
- **Error**: Red (#E74C3C)

### Typography

- **Headers**: Bold, 14-16pt
- **Body**: Regular, 10-12pt
- **Font Family**: System default (Sans-serif)

---

## Design Patterns

### 1. Singleton Pattern

**DatabaseManager** uses Singleton-like pattern:
- Single database connection per application
- Shared across all services

### 2. Factory Pattern

Service creation:
```python
class ServiceFactory:
    @staticmethod
    def create_patient_service():
        return PatientService(DatabaseManager())
```

### 3. Observer Pattern

PyQt6 signals and slots for UI updates:
```python
class QueueWidget(QWidget):
    queue_updated = pyqtSignal()
    
    def update_queue(self):
        self.queue_updated.emit()
```

### 4. Strategy Pattern

Queue ordering strategies:
```python
class QueueOrderingStrategy:
    def order_patients(self, patients):
        pass

class PriorityQueueStrategy(QueueOrderingStrategy):
    def order_patients(self, patients):
        return sorted(patients, key=lambda p: p.status, reverse=True)
```

### 5. Repository Pattern

Database operations abstracted:
```python
# DatabaseManager acts as repository
db = DatabaseManager()
patients = db.execute_query("SELECT * FROM patients")
```

---

## UML Diagrams

### Class Diagram (Simplified)

```
┌─────────────────┐
│  DatabaseManager │
├─────────────────┤
│ +execute_query()│
│ +execute_update()│
└────────┬────────┘
         │
         │ uses
         │
┌────────▼────────┐      ┌──────────────┐
│  PatientService │──────│    Patient   │
├─────────────────┤      ├──────────────┤
│ +create_patient()│     │ -patient_id  │
│ +get_patient()   │     │ -full_name   │
└────────┬─────────┘     │ -status      │
         │               └──────────────┘
         │ uses
         │
┌────────▼─────────┐
│  PatientWidget   │
├──────────────────┤
│ -patient_service │
│ +on_add_patient()│
└──────────────────┘
```

### Sequence Diagram: Add Patient to Queue

```
User    PatientWidget    QueueService    DatabaseManager    Database
 │            │                │                │              │
 │──click──>  │                │                │              │
 │            │──add_to_queue─>│                │              │
 │            │                │──execute_query>│              │
 │            │                │                │──SELECT──>   │
 │            │                │<─results──────│<─data───────│
 │            │                │──execute_update>│             │
 │            │                │                │──INSERT──>   │
 │            │                │<─success───────│<─OK─────────│
 │            │<─success───────│                │              │
 │<─updated───│                │                │              │
```

### Use Case Diagram

```
┌─────────────┐
│  Receptionist│
└──────┬───────┘
       │
       │ Register Patient
       │ Add to Queue
       │ Schedule Appointment
       │
┌──────▼──────────────────┐
│  Hospital Management     │
│        System            │
└──────┬───────────────────┘
       │
       │ View Patients
       │ Process Queue
       │
┌──────▼──────┐
│    Doctor   │
└─────────────┘
```

---

## Design Decisions

### Decision 1: Layered Architecture

**Decision**: Use layered architecture with clear separation  
**Rationale**: 
- Maintainability
- Testability
- Clear responsibilities
- Industry standard

### Decision 2: SQLite Database

**Decision**: Use SQLite for data storage  
**Rationale**:
- Zero configuration
- Single file database
- Sufficient for project scope
- Easy to backup

### Decision 3: PyQt6 for UI

**Decision**: Use PyQt6 for user interface  
**Rationale**:
- Modern and professional
- Cross-platform
- Rich widget set
- Good documentation

### Decision 4: Service Layer Pattern

**Decision**: Encapsulate business logic in services  
**Rationale**:
- Separation of concerns
- Reusable business logic
- Easier testing
- Clear API

### Decision 5: Priority-Based Queue

**Decision**: Automatic priority-based queue ordering  
**Rationale**:
- Fair patient processing
- Urgent cases handled first
- Automatic sorting
- No manual intervention needed

---

## Design Constraints

### Technical Constraints

- Python 3.8+ required
- Desktop application (not web-based)
- SQLite database (file-based)
- Single-user or small team usage

### Business Constraints

- Must handle patient data securely
- Must maintain data integrity
- Must support audit requirements
- Must be user-friendly

---

## Design Validation

### Design Review Checklist

- [x] Architecture follows best practices
- [x] Database design is normalized
- [x] Classes follow SOLID principles
- [x] Design patterns are appropriate
- [x] UI design is intuitive
- [x] Error handling is comprehensive
- [x] Security considerations addressed

---

## Future Design Considerations

### Potential Enhancements

1. **Web Interface**: Add web-based UI
2. **Mobile App**: Mobile companion app
3. **Cloud Storage**: Cloud database integration
4. **API**: RESTful API for external integration
5. **Microservices**: Split into microservices

### Scalability Considerations

- Database migration to PostgreSQL/MySQL
- Caching layer for performance
- Load balancing for multi-user
- Distributed architecture

---

## Conclusion

This design document provides:
- ✅ Clear architecture
- ✅ Well-defined components
- ✅ Appropriate design patterns
- ✅ Scalable structure
- ✅ Professional software engineering

**Last Updated**: January 30, 2026  
**Version**: 1.0
