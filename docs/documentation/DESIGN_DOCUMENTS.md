# Hospital Management System - Design Documents

## Document Information

**Project**: Intelligent Hospital Management and Queueing System (HMS)  
**Version**: Beta.ver.1.1 — LATEST  
**Date**: March 2026  
**Status**: Complete (documentation aligned with Streamlit implementation)

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
│   Presentation Layer (Browser UI)   │
│   Streamlit: reactive widgets,      │
│   interaction-driven reruns,        │
│   st.session_state, st.bar_chart    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Service Layer (Business Logic)  │
│  Patient, Queue, Doctor, Appt, etc. │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Data Access Layer                │
│  DatabaseManager (MySQL or SQLite)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Database (MySQL or SQLite file)   │
└─────────────────────────────────────┘
```

---

## Architecture Design

### Layer Responsibilities

#### Presentation Layer
- **Purpose**: Browser-based user interface and user interactions
- **Components**: Streamlit `app.py` — sidebar navigation, forms, `st.data_editor`, metrics, multiselect report picker, native charts (e.g. `st.bar_chart`)
- **Execution model**: **Interaction-driven** — each user action reruns the Streamlit script; widgets rebuild from current service/database state
- **Responsibilities**:
  - Display data to users
  - Capture user input
  - Validate input at UI level where appropriate
  - Provide immediate feedback (success/error) after service calls

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
User Action (browser)
    ↓
Streamlit widget event → script rerun
    ↓
Service Layer (Business Logic)
    ↓
Database Manager (MySQL or SQLite)
    ↓
Relational Database
    ↓
Response → UI update on next render
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

### Presentation structure (Streamlit)

#### Application shell (`app.py`)
```text
- st.set_page_config(...)
- init_database() → constructs DatabaseManager + injects into all services → st.session_state
- Sidebar: navigation buttons (Dashboard, Patient, Specialization, Queue, Doctor, Appointments)
- Route by st.session_state.current_page → show_*_management() or show_reports_analytics()
```

#### Module pages
Each major feature is implemented as a function group in `app.py` (forms, tables, buttons) calling the corresponding **service**; no PyQt6 windows or Qt widgets.

---

## User Interface Design

### Design Principles

1. **Consistency**: Uniform design language
2. **Clarity**: Clear visual hierarchy
3. **Efficiency**: Minimal clicks to complete tasks
4. **Feedback**: Clear response to user actions

### Layout Structure (browser)

```
┌──────────────┬──────────────────────────────────────────┐
│   Sidebar    │  Main area                                │
│  • Branding  │  • Page title + metrics                   │
│  • Nav (6)   │  • Search / filters                       │
│  • Status    │  • Action buttons                         │
│  • Quick     │  • Forms (add/edit) when open             │
│    stats     │  • st.data_editor tables + charts         │
└──────────────┴──────────────────────────────────────────┘
```

**Dashboard:** multiselect report types, date range, **Pandas**-backed metrics, **Streamlit** `st.bar_chart` (lightweight; Plotly not in baseline requirements).

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

### 3. Presentation refresh model (Streamlit)

The UI does not use Qt signals/slots. **User interaction triggers a full script rerun**; the presentation layer re-invokes services and redraws widgets. Shared state (database handle, services, navigation page, table selection) lives in **`st.session_state`**.

### 4. Strategy Pattern

**Database strategy (composition root):** `src/database/__init__.py` selects **MySQL** (`MySQLDatabaseManager`) or **SQLite** (`DatabaseManager`) based on `USE_MYSQL` in `src/config.py`, exporting a single **`DatabaseManager`** symbol for dependency injection into services.

**Queue ordering (implemented policy):** Active queue entries are sorted **priority first** (Super-Urgent > Urgent > Normal via `status DESC`), then **FIFO** by **`joined_at ASC`** in `QueueService.get_queue` (SQL-level ordering for consistency).

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
│  Streamlit UI    │
│  (app.py pages)  │
├──────────────────┤
│ session services │
│ + on_click_*()   │
└──────────────────┘
```

### Sequence Diagram: Add Patient to Queue

```
User    Streamlit UI    QueueService    DatabaseManager    Database
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

### Decision 2: MySQL or SQLite (configurable)

**Decision**: Support **MySQL** (e.g. XAMPP) and **SQLite** via configuration (`src/config.py`, `USE_MYSQL`).  
**Rationale**:
- MySQL suits networked lab and demo environments
- SQLite offers zero-server, file-based runs for portability
- **Dependency injection** at the app entry keeps **services database-agnostic**

### Decision 3: Streamlit for UI (browser-based)

**Decision**: Use **Streamlit** for the presentation layer — a **browser-based web application**, not a desktop Qt client.  
**Rationale**:
- Rapid development of forms, tables, and charts in pure Python
- **Reactive** widget model aligned with course focus on backend OOP
- **Native chart APIs** (`st.bar_chart`) plus **Pandas** avoid pulling in a separate charting stack (e.g. Plotly) for baseline analytics
- Accessible on LAN via browser without installing a desktop shell per seat

### Decision 4: Service Layer Pattern

**Decision**: Encapsulate business logic in services  
**Rationale**:
- Separation of concerns
- Reusable business logic
- Easier testing
- Clear API

### Decision 5: Priority-Based Queue

**Decision**: **Priority-first** ordering (Super-Urgent > Urgent > Normal), with **FIFO** among equals using **`joined_at`**.  
**Rationale**:
- Clinical urgency dominates; same-tier patients are served in arrival order
- Implemented in `QueueService.get_queue` with `ORDER BY status DESC, joined_at ASC`
- Reduces manual reordering while keeping predictable behavior

### Decision 6: Appointment conflict detection

**Decision**: Block new or updated appointments when the same **doctor** has an **overlapping time interval** (start time plus **duration**) with an existing active booking.  
**Rationale**:
- Prevents double-booking without relying on manual calendar checks
- Implemented in `AppointmentService.check_conflicts` and invoked from create/update paths
- Surfaces a clear error in the Streamlit scheduling UI when a conflict exists

---

## Design Constraints

### Technical Constraints

- Python 3.9+ recommended (see `requirements.txt`)
- **Browser-based** application (Streamlit); not a PyQt6 desktop executable
- **MySQL or SQLite** per configuration; not locked to a single engine
- Suited to pilot, classroom, or small-team intranet use; production scale requires further hardening (authentication, formal load testing, compliance review)

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

1. **Patient portal** and authenticated multi-user access (RBAC)
2. **REST or GraphQL API** alongside Streamlit for third-party integrations
3. **Mobile-optimized** or companion PWA
4. **Cloud-hosted** database and CI/CD packaging
5. **Microservices** only if scale and team structure justify operational complexity

### Scalability Considerations

- PostgreSQL or managed MySQL for larger concurrency
- Caching layer for heavy reporting
- Load balancing and session affinity for multi-instance Streamlit (if adopted)
- **Appointment conflict detection** and **queue ordering** remain service-layer concerns if the presentation tier changes

---

## Conclusion

This design document provides:
- ✅ Clear architecture
- ✅ Well-defined components
- ✅ Appropriate design patterns
- ✅ Scalable structure
- ✅ Professional software engineering

**Last Updated**: March 2026  
**Version**: Beta.ver.1.1 — LATEST
