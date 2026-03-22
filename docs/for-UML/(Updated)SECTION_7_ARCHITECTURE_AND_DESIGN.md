# 7. System Architecture and Design

## 7.1 Architectural Overview

### Description of the Overall Architecture

The Intelligent Hospital Management System (HMS) employs a **layered, service-oriented architecture** that cleanly separates concerns across three primary tiers:

| Layer | Description | Key Components |
|-------|-------------|----------------|
| **Presentation Layer** | User interface and user interaction | Streamlit application (`app.py`), reactive UI components (forms, tables, navigation, charts) |
| **Service Layer (Business Logic)** | Domain logic, validation, and orchestration | `PatientService`, `SpecializationService`, `QueueService`, `DoctorService`, `AppointmentService`, `ReportService` |
| **Data Access Layer** | Persistence and database abstraction | `DatabaseManager` (SQLite) / `MySQLDatabaseManager` (MySQL), schema and initialization scripts |

Data flows in one direction: the **Presentation Layer** calls the **Service Layer**; the **Service Layer** uses the **Data Access Layer** to read and write data. Domain entities (e.g. `Patient`, `Doctor`, `Appointment`) are defined in the **Models** (`src/models/`) and are used by both the Service and Data Access layers. The UI does not access the database directly—all persistence goes through the services.

This structure is consistent with a **Layered Architecture** (also referred to as *N-Tier*) combined with a **Service-Oriented** design: each service encapsulates one domain (patients, queue, appointments, etc.) and exposes operations (create, read, update, delete, and domain-specific actions such as “serve next patient” or “check conflicts”).

### Rationale for the Chosen Architecture

- **Separation of concerns:** The UI (Streamlit) is independent of business rules and database technology. Changing the UI framework or the database (e.g. switching from MySQL to SQLite) does not require rewriting business logic.
- **Testability:** Services can be unit-tested by injecting a mock or in-memory database; the presentation layer can be tested against service interfaces.
- **Maintainability:** Each service has a single, well-defined responsibility (e.g. `QueueService` for queue logic, `AppointmentService` for scheduling and conflict detection), making the codebase easier to extend and debug.
- **Reusability:** Business logic lives in services; the same logic can be reused by a different UI (e.g. a REST API or a future mobile app) without duplication.
- **Strategy for data storage:** The system supports both MySQL and SQLite through a single abstract interface (`DatabaseManager`). The concrete implementation (SQLite or MySQL) is chosen at runtime via configuration (`src/config.py`), aligning with the **Strategy Pattern** and enabling portability between production and demonstration environments.

---

## 7.2 Object-Oriented Design

### Key Classes and Responsibilities

**Domain Models (`src/models/`)**  
These classes represent core entities and hold data and simple derived properties. They do not perform database access or business rules.

| Class | Responsibility |
|-------|----------------|
| **Patient** | Represents a patient: identity (ID, name, DOB), contact (phone, email, address), and priority status (Normal, Urgent, Super-Urgent). Exposes `to_dict()` for serialization. |
| **Specialization** | Represents a medical department/specialization: name, description, maximum queue capacity, and active flag. |
| **QueueEntry** | Represents one patient in a queue for a specialization: patient ID, specialization ID, priority, position, join/served/removed timestamps. Exposes computed properties such as `status_text`, `wait_time_minutes`. |
| **Doctor** | Represents a doctor: identity, license number, contact, status (Active, Inactive, On Leave). Exposes `display_name`, `is_active`, and `to_dict()`. Doctor–specialization assignments are stored in a junction table and resolved by `DoctorService`. |
| **Appointment** | Represents an appointment: patient ID, doctor ID, specialization ID, date, time, duration, type (Regular, Follow-up, Emergency), status (Scheduled, Confirmed, Completed, Cancelled, No-Show). Exposes `appointment_datetime` and `end_time` for conflict logic. |

**Data Access (`src/database/`)**  
These classes abstract database operations and connection management.

| Class | Responsibility |
|-------|----------------|
| **DatabaseManager** | SQLite implementation: connection lifecycle, transaction handling, schema initialization, `execute_query`, `execute_update`, backup/restore. Used when `USE_MYSQL` is False. |
| **MySQLDatabaseManager** | MySQL implementation with the same logical interface (connection, execute_query, execute_update, get_last_insert_id). Used when `USE_MYSQL` is True. The application and services depend on the abstract role “database manager,” not a specific class. |

**Services (`src/services/`)**  
These classes implement business logic and use the database manager (and, in one case, other services) to persist and retrieve data.

| Class | Responsibility |
|-------|----------------|
| **PatientService** | CRUD for patients; validation of required fields (e.g. name, DOB); mapping between database rows and `Patient` objects. |
| **SpecializationService** | CRUD for specializations; enforcement of capacity and active/inactive state; used by queue and appointment logic. |
| **QueueService** | Add patient to queue, serve next patient (priority-based ordering), change priority, remove from queue; queue statistics and analytics; enforcement of specialization capacity. |
| **DoctorService** | CRUD for doctors; assignment of doctors to specializations (junction table); used by appointment and report logic. |
| **AppointmentService** | Create/update/complete/cancel appointments; **conflict detection** (same doctor, overlapping time windows); availability checks and doctor calendar; validation of date/time and appointment type. |
| **ReportService** | Aggregation of data for dashboards and reports; uses `DatabaseManager` and instantiates other services to gather patient, queue, doctor, appointment, and specialization statistics; no direct UI—returns data structures for the presentation layer to render. |

**Presentation**  
- **`app.py` (Streamlit)** | Entry point and UI: initializes `DatabaseManager` (or MySQL equivalent) and all services (injecting the same db manager), handles navigation, forms, tables, and charts; calls service methods in response to user actions and displays results. Does not contain business or persistence logic.

### Class Relationships and Interactions

- **Dependency Injection (composition):** Each service receives a `DatabaseManager` (or MySQL implementation) in its constructor. The Streamlit app creates one database manager and injects it into every service. This keeps services decoupled from the concrete database implementation.
- **Models and services:** Services create and return model instances (e.g. `Patient`, `Appointment`). They map database rows to domain objects and vice versa. There is no inheritance among the five model classes; they are independent entities.
- **ReportService and other services:** `ReportService` constructs instances of `PatientService`, `SpecializationService`, `QueueService`, `DoctorService`, and `AppointmentService` internally (each with the same `db_manager`). It then uses these services to aggregate data for reports. No circular dependency: ReportService → other services → DatabaseManager.
- **Foreign key relationships (logical):** `Appointment` references `patient_id`, `doctor_id`, `specialization_id`; `QueueEntry` references `patient_id`, `specialization_id`. Doctor–specialization is many-to-many via `doctor_specializations`. These relationships are enforced in the database and respected by the services when validating and loading data.

### Application of OOP Principles

- **Single Responsibility (SRP):** Each service handles one domain (patients, queue, appointments, etc.). Each model represents one entity. The database manager is responsible only for connection and query execution.
- **Open/Closed (OCP):** New behavior (e.g. a new report type) is added by extending or composing services (e.g. new methods in `ReportService`) or new UI sections in `app.py`, without modifying existing service internals or the database interface. New database backends can be added by providing another implementation of the same logical interface.
- **Dependency Inversion (DIP):** Services depend on an abstract “database manager” (the interface defined by the methods they call: `execute_query`, `execute_update`, `get_connection`, etc.), not on SQLite or MySQL directly. The concrete implementation (SQLite or MySQL) is chosen at startup and injected.
- **Encapsulation:** Business rules (e.g. queue priority algorithm, appointment conflict rules) are encapsulated inside services; the UI and database layers do not duplicate this logic.
- **Composition over inheritance:** The system favors composition (e.g. services “have” a database manager, ReportService “uses” other services) rather than deep inheritance hierarchies.

---

## 7.3 UML Diagrams

The following diagrams are provided in **Mermaid** syntax so they can be rendered in Markdown viewers (e.g. GitHub, GitLab, VS Code with Mermaid support) or exported to images. For submission, you may paste the Mermaid code into a tool such as [Mermaid Live Editor](https://mermaid.live) to generate PNG/SVG and insert the image into your final document.

---

### 7.3.1 UML Class Diagram (Required)

This diagram shows the main domain models, the service layer, the data access abstraction, and their relationships (composition/dependency). The application entry point (`app.py`) is represented as a stakeholder that uses all services.

```mermaid
classDiagram
    direction TB

    class Patient {
        +int patient_id
        +str full_name
        +date date_of_birth
        +str gender
        +str phone_number
        +str email
        +int status
        +to_dict()
    }

    class Specialization {
        +int specialization_id
        +str name
        +str description
        +int max_capacity
        +bool is_active
    }

    class QueueEntry {
        +int queue_entry_id
        +int patient_id
        +int specialization_id
        +int status
        +datetime joined_at
        +datetime served_at
        +status_text
        +wait_time_minutes
    }

    class Doctor {
        +int doctor_id
        +str full_name
        +str license_number
        +str status
        +display_name
        +to_dict()
    }

    class Appointment {
        +int appointment_id
        +int patient_id
        +int doctor_id
        +int specialization_id
        +date appointment_date
        +time appointment_time
        +int duration
        +str status
        +appointment_datetime
        +end_time
    }

    class DatabaseManager {
        <<interface/abstract>>
        +get_connection()
        +execute_query()
        +execute_update()
        +init_database()
        +get_last_insert_id()
    }

    class PatientService {
        -db : DatabaseManager
        +create_patient()
        +get_patient()
        +update_patient()
        +delete_patient()
        +get_all_patients()
    }

    class SpecializationService {
        -db : DatabaseManager
        +create_specialization()
        +get_specialization()
        +update_specialization()
        +get_all_specializations()
    }

    class QueueService {
        -db : DatabaseManager
        +add_patient_to_queue()
        +serve_next_patient()
        +get_queue()
        +get_queue_statistics()
    }

    class DoctorService {
        -db : DatabaseManager
        +create_doctor()
        +get_doctor()
        +update_doctor()
        +get_doctor_specializations()
    }

    class AppointmentService {
        -db : DatabaseManager
        +create_appointment()
        +get_appointment()
        +check_conflicts()
        +update_appointment()
    }

    class ReportService {
        -db : DatabaseManager
        -patient_service : PatientService
        -queue_service : QueueService
        -doctor_service : DoctorService
        -appointment_service : AppointmentService
        +get_dashboard_summary()
        +get_patient_statistics()
        +get_queue_statistics()
    }

    class StreamlitApp {
        -db_manager : DatabaseManager
        -patient_service : PatientService
        -queue_service : QueueService
        -doctor_service : DoctorService
        -appointment_service : AppointmentService
        -report_service : ReportService
        +show_patient_management()
        +show_queue_management()
        +show_appointment_management()
    }

    PatientService --> DatabaseManager : uses
    PatientService --> Patient : creates/returns
    SpecializationService --> DatabaseManager : uses
    SpecializationService --> Specialization : creates/returns
    QueueService --> DatabaseManager : uses
    QueueService --> QueueEntry : creates/returns
    QueueService --> Specialization : reads capacity
    DoctorService --> DatabaseManager : uses
    DoctorService --> Doctor : creates/returns
    AppointmentService --> DatabaseManager : uses
    AppointmentService --> Appointment : creates/returns
    ReportService --> DatabaseManager : uses
    ReportService --> PatientService : uses
    ReportService --> QueueService : uses
    ReportService --> DoctorService : uses
    ReportService --> AppointmentService : uses
    StreamlitApp --> PatientService : uses
    StreamlitApp --> SpecializationService : uses
    StreamlitApp --> QueueService : uses
    StreamlitApp --> DoctorService : uses
    StreamlitApp --> AppointmentService : uses
    StreamlitApp --> ReportService : uses
    StreamlitApp --> DatabaseManager : creates, injects
    QueueEntry --> Patient : patient_id
    QueueEntry --> Specialization : specialization_id
    Appointment --> Patient : patient_id
    Appointment --> Doctor : doctor_id
    Appointment --> Specialization : specialization_id
```

---

### 7.3.2 UML Sequence Diagram (Required)

This sequence diagram illustrates the flow when a **user schedules a new appointment**: from the UI through the service layer and conflict checking to database persistence.

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit UI\n(app.py)
    participant AS as AppointmentService
    participant DB as DatabaseManager

    User->>UI: Fill form & click "Schedule Appointment"
    UI->>AS: create_appointment(appointment_data)

    AS->>AS: Validate patient_id, doctor_id, date, time
    AS->>AS: Parse date and time

    AS->>DB: execute_query (get existing appointments for doctor)
    DB-->>AS: List of existing appointments

    AS->>AS: check_conflicts(doctor_id, date, time, duration)
    alt Conflicts found
        AS-->>UI: raise ValueError("Appointment conflicts...")
        UI-->>User: Show error message
    else No conflicts
        AS->>DB: execute_update(INSERT INTO appointments ...)
        DB-->>AS: OK
        AS->>DB: get_last_insert_id()
        DB-->>AS: appointment_id
        AS-->>UI: return appointment_id
        UI-->>User: Show success, refresh table
    end
```

---

### 7.3.3 Activity Diagrams

The following activity diagrams describe user and system actions for the main feature flows. They complement the sequence diagram (7.3.2) and provide a process-view of each module.

---

#### 7.3.3.1 Add Patient to Queue

Describes adding a patient to a specialization queue, including capacity check and priority selection.

```mermaid
flowchart TD
    A([User: Select Specialization]) --> B([User: Click Add to Queue])
    B --> C{Specialization\nselected?}
    C -->|No| D([Show: Select a specialization])
    C -->|Yes| E([Load patient list])
    E --> F([User: Select Patient & Priority])
    F --> G{Queue at\ncapacity?}
    G -->|Yes| H([Show error: Queue full])
    G -->|No| I([System: add_patient_to_queue])
    I --> J([Insert queue_entry])
    J --> K([Return queue_entry_id])
    K --> L([Show success, refresh table])
    D --> A
    H --> F
    L --> M([End])
```

---

#### 7.3.3.2 Patient Registration (Add New Patient)

Describes the flow for registering a new patient: form entry, validation, and persistence.

```mermaid
flowchart TD
    A([User: Click Add New Patient]) --> B([Show patient form])
    B --> C([User: Enter name, DOB, optional fields])
    C --> D([User: Click Save Patient])
    D --> E{Required fields\nvalid?}
    E -->|No| F([Show validation error])
    F --> C
    E -->|Yes| G([PatientService: create_patient])
    G --> H([Validate name, DOB])
    H --> I([INSERT INTO patients])
    I --> J([Return patient_id])
    J --> K([Show success, refresh table])
    K --> L([End])
```

---

#### 7.3.3.3 Edit Patient

Describes selecting a patient, loading the form, updating fields, and saving.

```mermaid
flowchart TD
    A([User: Select patient in table]) --> B([User: Click Edit Patient])
    B --> C{Row\nselected?}
    C -->|No| D([Show: Select a patient])
    C -->|Yes| E([Load patient data into form])
    E --> F([User: Change fields])
    F --> G([User: Click Update Patient])
    G --> H{Required fields\nvalid?}
    H -->|No| I([Show validation error])
    I --> F
    H -->|Yes| J([PatientService: update_patient])
    J --> K([UPDATE patients])
    K --> L([Show success, refresh table])
    D --> A
    L --> M([End])
```

---

#### 7.3.3.4 Delete Patient

Describes selecting a patient, confirming deletion, and removing the record.

```mermaid
flowchart TD
    A([User: Select patient in table]) --> B([User: Click Delete Patient])
    B --> C{Row\nselected?}
    C -->|No| D([Show: Select a patient])
    C -->|Yes| E([Show confirmation with patient details])
    E --> F([User: Confirm Delete or Cancel])
    F --> G{Cancel?}
    G -->|Yes| H([Close, no change])
    G -->|No| I([PatientService: delete_patient])
    I --> J([DELETE FROM patients])
    J --> K([Show success, refresh table])
    D --> A
    K --> L([End])
```

---

#### 7.3.3.5 Doctor Management — Add Doctor

Describes adding a new doctor and assigning specializations.

```mermaid
flowchart TD
    A([User: Click Add New Doctor]) --> B([Show doctor form])
    B --> C([User: Enter name, license, contact, status])
    C --> D([User: Select one or more specializations])
    D --> E([User: Click Add Doctor])
    E --> F{Required fields\nvalid?}
    F -->|No| G([Show validation error])
    G --> C
    F -->|Yes| H([DoctorService: create_doctor])
    H --> I([INSERT INTO doctors])
    I --> J([Insert doctor_specializations])
    J --> K([Return doctor_id])
    K --> L([Show success, refresh table])
    L --> M([End])
```

---

#### 7.3.3.6 Doctor Management — Edit Doctor

Describes loading a doctor, updating details and specializations, and saving.

```mermaid
flowchart TD
    A([User: Select doctor in table]) --> B([User: Click Edit Doctor])
    B --> C{Row\nselected?}
    C -->|No| D([Show: Select a doctor])
    C -->|Yes| E([Load doctor and specializations into form])
    E --> F([User: Change fields / specializations])
    F --> G([User: Click Update Doctor])
    G --> H{Required fields\nvalid?}
    H -->|No| I([Show validation error])
    I --> F
    H -->|Yes| J([DoctorService: update_doctor])
    J --> K([UPDATE doctors])
    K --> L([Update doctor_specializations])
    L --> M([Show success, refresh table])
    D --> A
    M --> N([End])
```

---

#### 7.3.3.7 Doctor Management — Delete Doctor

Describes selecting a doctor, confirming, and removing the record.

```mermaid
flowchart TD
    A([User: Select doctor in table]) --> B([User: Click Delete Doctor])
    B --> C{Row\nselected?}
    C -->|No| D([Show: Select a doctor])
    C -->|Yes| E([Show confirmation])
    E --> F([User: Yes, Delete or Cancel])
    F --> G{Cancel?}
    G -->|Yes| H([Close, no change])
    G -->|No| I([DoctorService: delete_doctor])
    I --> J([Delete doctor_specializations])
    J --> K([DELETE FROM doctors])
    K --> L([Show success, refresh table])
    D --> A
    L --> M([End])
```

---

#### 7.3.3.8 Specialization Management — Add Specialization

Describes creating a new specialization with name, description, capacity, and active flag.

```mermaid
flowchart TD
    A([User: Click Add New Specialization]) --> B([Show specialization form])
    B --> C([User: Enter name, description, max capacity, active])
    C --> D([User: Click Save Specialization])
    D --> E{Required fields\nvalid?}
    E -->|No| F([Show validation error])
    F --> C
    E -->|Yes| G([SpecializationService: create_specialization])
    G --> H([INSERT INTO specializations])
    H --> I([Return specialization_id])
    I --> J([Show success, refresh table])
    J --> K([End])
```

---

#### 7.3.3.9 Specialization Management — Edit / Delete Specialization

Describes editing or deleting a specialization after selection and confirmation.

```mermaid
flowchart TD
    A([User: Select specialization in table]) --> B([User: Click Edit or Delete])
    B --> C{Row\nselected?}
    C -->|No| D([Show: Select a specialization])
    C -->|Yes| E{Action?}
    E -->|Edit| F([Load specialization into form])
    F --> G([User: Change fields, Click Update])
    G --> H([SpecializationService: update_specialization])
    H --> I([UPDATE specializations])
    I --> J([Show success, refresh table])
    E -->|Delete| K([Show confirmation])
    K --> L([User: Yes, Delete or Cancel])
    L --> M{Cancel?}
    M -->|Yes| N([Close, no change])
    M -->|No| O([SpecializationService: delete_specialization])
    O --> P([DELETE FROM specializations])
    P --> Q([Show success, refresh table])
    D --> A
    J --> R([End])
    Q --> R
```

---

#### 7.3.3.10 Schedule New Appointment

Describes the flow for scheduling an appointment: form entry, conflict check, and persistence. Complements the sequence diagram in 7.3.2.

```mermaid
flowchart TD
    A([User: Click Schedule New Appointment]) --> B([Show appointment form])
    B --> C([User: Select patient, doctor, specialization, date, time, type])
    C --> D([User: Click Schedule Appointment])
    D --> E{Required fields\nvalid?}
    E -->|No| F([Show validation error])
    F --> C
    E -->|Yes| G([AppointmentService: create_appointment])
    G --> H([Load existing appointments for doctor])
    H --> I([check_conflicts])
    I --> J{Conflict\nfound?}
    J -->|Yes| K([Raise error: overlapping time])
    K --> L([Show error, user changes time/doctor])
    L --> C
    J -->|No| M([INSERT INTO appointments])
    M --> N([Return appointment_id])
    N --> O([Show success, refresh table])
    O --> P([End])
```

---

#### 7.3.3.11 Serve Next Patient from Queue

Describes serving the next patient in line for a specialization (priority-based).

```mermaid
flowchart TD
    A([User: Select specialization]) --> B([User: Click Serve Next Patient])
    B --> C{Specialization\nselected?}
    C -->|No| D([Show: Select a specialization])
    C -->|Yes| E([QueueService: serve_next_patient])
    E --> F{Queue\nempty?}
    F -->|Yes| G([Return None / Show: No patients in queue])
    G --> H([End])
    F -->|No| I([Get next entry by priority and order])
    I --> J([UPDATE queue_entry: status = Served, served_at])
    J --> K([Return served QueueEntry])
    K --> L([Show who was served, refresh table])
    D --> A
    L --> H
```

---

#### 7.3.3.12 Report Generation

Describes selecting report type, date range, and generating the report (standard or custom).

```mermaid
flowchart TD
    A([User: Open Reports & Analytics]) --> B([Show dashboard summary])
    B --> C([User: Select report type and date range])
    C --> D{Report type?}
    D -->|Standard| E([User sets Start/End date])
    E --> F([ReportService: get_* for selected type])
    F --> G([Aggregate patients / queue / appointments / doctors / specializations])
    G --> H([Return data structures])
    H --> I([UI: Render tables and charts])
    D -->|Custom| J([User selects metrics and date range])
    J --> K([User: Click Generate Custom Report])
    K --> L([ReportService: gather selected metrics])
    L --> M([Combine into single report])
    M --> N([UI: Render custom report])
    I --> O([End])
    N --> O
```

---

### 7.3.4 Additional Diagram: Component Diagram (High-Level)

This component diagram shows the main logical blocks of the system and their dependencies, aligned with the layered, service-oriented design.

```mermaid
flowchart LR
    subgraph Presentation
        UI[Streamlit App\napp.py]
    end

    subgraph Service Layer
        PS[PatientService]
        SS[SpecializationService]
        QS[QueueService]
        DS[DoctorService]
        APS[AppointmentService]
        RS[ReportService]
    end

    subgraph Data Access
        DM[(DatabaseManager\nSQLite / MySQL)]
    end

    subgraph Models
        M[Patient, Doctor, Appointment,\nSpecialization, QueueEntry]
    end

    UI --> PS
    UI --> SS
    UI --> QS
    UI --> DS
    UI --> APS
    UI --> RS
    PS --> DM
    SS --> DM
    QS --> DM
    DS --> DM
    APS --> DM
    RS --> DM
    RS --> PS
    RS --> SS
    RS --> QS
    RS --> DS
    RS --> APS
    PS --> M
    SS --> M
    QS --> M
    DS --> M
    APS --> M
```

---

**Note for final submission:** Replace the placeholder “(Note: Visual diagrams should be inserted here during final formatting)” in your main document with the content above. For strict UML submission requirements, you may export the Mermaid diagrams to PNG or SVG using [Mermaid Live Editor](https://mermaid.live) or a CI/CD Mermaid step, then reference the resulting figures in Section 7.3.

**Document:** Section 7 — System Architecture and Design  
**Last updated:** January 31, 2026
