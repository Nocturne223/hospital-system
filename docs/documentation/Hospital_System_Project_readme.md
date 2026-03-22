# Intelligent Hospital Management and Queueing System (HMS)

**Beta.ver.1.1 — LATEST**

The **Intelligent Hospital Management and Queueing System** is a **browser-based operational dashboard** built with **Python** and **Streamlit**. It is **not** a command-line tool and **not** a PyQt6 desktop application. Staff use a web browser to manage patients, departments (specializations), queues, doctors, appointments, and **Reports & Analytics** on the **Dashboard**.

The system follows a **Layered Service-Oriented Architecture (SOA)**:

- **Presentation:** Streamlit (`app.py`) — reactive UI, interaction-driven reruns, sidebar navigation, forms, tables, and native charts (e.g. `st.bar_chart`) with **Pandas** for reporting.
- **Service layer:** Domain logic in `src/services/` — one primary service per area, constructed with a **shared `DatabaseManager`** injected from `app.py` (**dependency injection**).
- **Persistence:** **MySQL** (e.g. XAMPP) or **SQLite**, selected by **`USE_MYSQL`** in `src/config.py` (**strategy-like** resolution in `src/database/__init__.py`); services stay database-agnostic.

## Core components (architectural roles)

### Domain models (`src/models/`)

Entity classes (e.g. **`Patient`**, **`Doctor`**, **`Specialization`**, **`Appointment`**, **`QueueEntry`**) hold typed attributes and helpers such as **`to_dict()`**. They map to relational tables and are filled by the service layer; they do **not** own business workflows end-to-end.

### Service classes (`src/services/`)

Services implement **application use cases** and orchestrate validation, rules, and SQL via the injected manager, for example:

- **`PatientService`** — registration, search, updates, triage-style status (Normal / Urgent / Super-Urgent).
- **`SpecializationService`** — departments, capacity, active/inactive lifecycle.
- **`QueueService`** — enqueue, ordering (**priority first**, **FIFO** by `joined_at`), capacity, serve/remove.
- **`DoctorService`** — doctor profiles, specialization assignments, employment status.
- **`AppointmentService`** — scheduling, updates, completion/cancellation, **overlap conflict detection** for the same doctor.
- **`ReportService`** — aggregates for the Dashboard (metrics and chart-ready series).

### Presentation entry (`app.py`)

Binds Streamlit widgets to the services above; keeps the UI thin so rules remain testable and reusable.

---

For install and usage, see **[USER_MANUAL.md](USER_MANUAL.md)**, **[HOW_TO_RUN.md](HOW_TO_RUN.md)**, and **[RUN_STREAMLIT.md](RUN_STREAMLIT.md)**.
