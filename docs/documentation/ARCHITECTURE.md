# Hospital Management System — Architecture Documentation

**Documentation:** Beta.ver.1.1 — LATEST  
**Application:** Browser-based web UI (`app.py`, Streamlit)

## Table of Contents

1. [System Overview](#system-overview)
2. [Layered Service-Oriented Architecture](#layered-service-oriented-architecture)
3. [Presentation Layer (Streamlit)](#presentation-layer-streamlit)
4. [Service and Data Access Layers](#service-and-data-access-layers)
5. [Queue Ordering and Appointment Conflicts](#queue-ordering-and-appointment-conflicts)
6. [Design Patterns (SOLID, Strategy, DI)](#design-patterns-solid-strategy-di)
7. [Database Design](#database-design)
8. [Technology Stack](#technology-stack)
9. [Component Interactions](#component-interactions)
10. [Extension Points](#extension-points)

---

## System Overview

### Architecture Type

The Intelligent Hospital Management and Queueing System (HMS) follows a **Layered Service-Oriented Architecture (SOA)**:

- **Presentation:** Streamlit in a web browser (reactive widgets, interaction-driven reruns).
- **Services:** Domain logic in `src/services/` (one primary concern per service).
- **Persistence:** Database access via a **single injected `DatabaseManager` symbol**, resolved at import time to either **SQLite** (`DatabaseManager`) or **MySQL** (`MySQLDatabaseManager`) based on `src/config.py`.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Presentation Layer                           │
│   Streamlit (browser): sidebar nav, forms, data_editor,     │
│   metrics, native charts (e.g. st.bar_chart), session_state │
└───────────────────────────┬─────────────────────────────────┘
                            │ calls
┌───────────────────────────▼─────────────────────────────────┐
│                  Service Layer (Business Logic)              │
│  PatientService, SpecializationService, QueueService,      │
│  DoctorService, AppointmentService, ReportService          │
└───────────────────────────┬─────────────────────────────────┘
                            │ uses (injected)
┌───────────────────────────▼─────────────────────────────────┐
│              Data Access Layer                               │
│  DatabaseManager ←── strategy-like selection in               │
│       src/database/__init__.py (USE_MYSQL / config)          │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│         Database Layer (MySQL or SQLite)                     │
└──────────────────────────────────────────────────────────────┘
```

### Core Principles

1. **Separation of concerns** — UI does not embed SQL; services encapsulate rules.
2. **Dependency injection** — Services receive `DatabaseManager` at construction (see `app.py` `init_database()`).
3. **Database-agnostic services** — Same service code paths for MySQL and SQLite; differences isolated in DB managers and parameter handling.
4. **Lightweight visualization** — Dashboard analytics use **Pandas** and **Streamlit native chart APIs** (e.g. `st.bar_chart`); separate charting libraries such as Plotly are **not** required for the baseline stack, keeping dependencies lean.

---

## Layered Service-Oriented Architecture

| Layer | Responsibility | Primary location |
|--------|----------------|------------------|
| **Presentation** | Render UI, capture input, trigger service calls on user action | `app.py` (Streamlit) |
| **Service** | Validation, business rules, orchestration | `src/services/*.py` |
| **Data access** | Connections, queries, transactions | `src/database/db_manager.py`, `mysql_db_manager.py` |
| **Models** | Entity structure, `to_dict`, helpers | `src/models/*.py` |

The **ReportService** aggregates data for the **Dashboard** (Reports & Analytics), combining SQL-backed queries with Pandas where reshaping is needed for charts.

---

## Presentation Layer (Streamlit)

### Characteristics

- **Browser-based:** Users open `http://localhost:8501` (default) after `python -m streamlit run app.py` or `run_streamlit.bat`.
- **Reactive UI:** Widgets (buttons, forms, `st.data_editor`, `st.selectbox`, etc.) are declared each run; **user interaction causes a script rerun**, reloading state from the database through services.
- **Session state:** `st.session_state` holds the shared `DatabaseManager` and service instances, selected navigation page, and table selection flags.
- **Navigation:** Sidebar buttons for **Dashboard**, **Patient Management**, **Specialization Management**, **Queue Management**, **Doctor Management**, **Appointments**.

### Six primary modules (feature-complete in Beta v1.1)

1. **Dashboard** — Multiselect report types, date range, bar charts and tables via Streamlit + Pandas.  
2. **Patient Management** — CRUD, search, filter, statistics.  
3. **Specialization Management** — Departments, capacity, active/inactive.  
4. **Queue Management** — Add/serve, priorities, capacity, per-row actions, analytics panel.  
5. **Doctor Management** — CRUD, specialization assignments, status.  
6. **Appointment Management** — Schedule/edit/complete/cancel, **conflict detection** for overlapping doctor slots.

---

## Service and Data Access Layers

### Dependency injection (runtime wiring)

In `app.py`, after a successful connection:

- `PatientService(db_manager)`, `QueueService(db_manager)`, `DoctorService(db_manager)`, `AppointmentService(db_manager)`, `ReportService(db_manager)`, etc.

Services depend on the **concrete manager** exported as `DatabaseManager` from `src/database/__init__.py`, not on MySQL- or SQLite-specific types in the UI.

### Strategy-like database selection

`src/database/__init__.py` selects:

- `MySQLDatabaseManager` aliased as `DatabaseManager` when `USE_MYSQL` is true.  
- SQLite `DatabaseManager` when using file-based storage.

This preserves **open/closed** behavior at the composition root: services remain unchanged when switching engines.

---

## Queue Ordering and Appointment Conflicts

### Queue ordering

Active queue rows are ordered **priority first**, then **FIFO by join time**:

- **Priority:** Super-Urgent > Urgent > Normal (higher `status` value first; see `QueueService.get_queue`).  
- **Tie-breaker:** Earlier `joined_at` first.

Implemented as SQL-style ordering: `ORDER BY status DESC, joined_at ASC` in `QueueService.get_queue`, ensuring consistent, atomic ordering per specialization.

### Appointment conflicts

`AppointmentService.check_conflicts` (used on create and when date/time changes) compares **interval overlap** for the same doctor: start/end derived from appointment time and **duration**. Overlaps block the operation with a user-visible error in the Streamlit form.

---

## Design Patterns (SOLID, Strategy, DI)

| Pattern / principle | Application |
|---------------------|-------------|
| **Dependency Injection** | Services take `db_manager` in `__init__`; `app.py` constructs and stores them in `st.session_state`. |
| **Strategy (database)** | Conditional import / alias in `src/database/__init__.py` for MySQL vs SQLite. |
| **Single Responsibility (SOLID)** | One service per aggregate (patients, queues, appointments, …). |
| **Repository-style access** | `DatabaseManager.execute_query` / `execute_update` centralize SQL execution. |

Legacy examples referring to PyQt6 signals or desktop widgets are **obsolete**; the live UI is Streamlit-driven reruns, not signal/slot graphs.

---

## Database Design

Schema follows normalized relational design (patients, doctors, specializations, doctor_specializations, queue_entries, appointments, users, audit_logs, etc.).  

**Engines:** MySQL (e.g. XAMPP) or SQLite file (`data/hospital_system.db` or configured path), selected in `src/config.py`.

---

## Technology Stack

| Area | Choice |
|------|--------|
| Language | Python 3.9+ (see `requirements.txt`) |
| UI | Streamlit ≥ 1.28 |
| Data processing | Pandas |
| Charts | Streamlit native APIs (`st.bar_chart`, etc.); no Plotly dependency in baseline requirements |
| Database | MySQL (`mysql-connector-python`) or SQLite (stdlib) |
| Tests | pytest |

---

## Component Interactions

### Example: Schedule appointment (simplified)

```
Browser → Streamlit form submit
    → AppointmentService.create_appointment(data)
        → AppointmentService.check_conflicts(doctor, date, time, duration)
        → DatabaseManager.execute_update / queries
    → Streamlit success or error → rerun → updated table
```

### Example: Serve next in queue

```
Streamlit button → QueueService.get_next_patient(specialization_id)
    → QueueService.get_queue (ordered)
    → QueueService.serve_patient(entry_id)
    → DatabaseManager.execute_update
    → Streamlit rerun → refreshed queue table
```

---

## Extension Points

1. Add a **model** in `src/models/`, **service** in `src/services/`, **UI section** in `app.py` (or split modules if desired).  
2. Extend **ReportService** / Dashboard multiselect for new report types.  
3. Optional: add chart libraries later; baseline intentionally stays lightweight.

---

## Conclusion

This architecture delivers:

- Browser-based **Streamlit** presentation with an **interaction-driven** execution model.  
- **SOA-style** service layer with **dependency injection** and **database strategy** at the package boundary.  
- **Documented queue policy** and **appointment conflict** rules aligned with implementation.

**Last Updated:** March 2026  
**Version:** Beta 1.1 (documentation alignment)
