# Engineered Prompt: Masters in IT Final Project Documentation

Use the prompt below to generate documentation for the Hospital Management System final project. Copy the entire **Prompt** section into your AI or documentation workflow. The prompt is designed to align with `docs/documentation` guidelines and to describe only the current implementation (Streamlit-based), **excluding all PyQt-related content**.

---

## Prompt

```
You are generating academic-quality documentation for a **Masters in Information Technology** final project: a **Hospital Management System**. The documentation must satisfy the project’s official documentation requirements (user, developer, and project docs), be suitable for submission grading, and accurately describe and explain the **current implementation only**.

---

### 1. SCOPE OF WHAT TO DOCUMENT

**In scope — document and explain these:**

- **Application stack:** Python; **Streamlit** as the sole UI framework; MySQL (e.g. via XAMPP) with SQLite fallback; `app.py` as the Streamlit entry point; `run_streamlit.bat` / `python -m streamlit run app.py`.
- **Source code to reference:**  
  - `app.py` (Streamlit UI and navigation).  
  - `src/models/`: `patient.py`, `specialization.py`, `queue_entry.py`, `doctor.py`, `appointment.py`.  
  - `src/services/`: `patient_service.py`, `specialization_service.py`, `queue_service.py`, `doctor_service.py`, `appointment_service.py`, `report_service.py`.  
  - `src/database/`: `db_manager.py`, `mysql_db_manager.py`, `init_db.py`, `schema.sql`, `schema_mysql.sql`, and data seeding scripts (e.g. `add_sample_patients.py`, `add_sample_specializations.py`, `add_sample_doctors.py`, `add_sample_queue_entries.py`, `add_sample_appointments.py`, `add_comprehensive_report_data.py`).  
  - `src/config.py` for database/config.  
  - `tests/` (e.g. `test_database.py`, `test_patient_service.py`) for testing.  
- **Features to describe:**  
  - **Feature 1 — Patient management:** Registration, search/filter, status (Normal, Urgent, Super-Urgent), demographics, statistics; `Patient` model and `PatientService`.  
  - **Feature 2 — Specialization management:** CRUD, capacity, active/inactive, queue integration; `Specialization` model and `SpecializationService`.  
  - **Feature 3 — Queue management:** Add to queue, priority, serve next patient, position/wait time, analytics, “All Specializations” view; `QueueEntry` and `QueueService`.  
  - **Feature 4 — Doctor management:** Registration, license, specialization assignments, status (Active, Inactive, On Leave), search/filter, statistics; `Doctor` and `DoctorService`.  
  - **Feature 5 — Appointments:** Scheduling, conflict detection, types (Regular, Follow-up, Emergency), statuses (Scheduled, Confirmed, Completed, Cancelled, No-Show), mark complete, date range filter; `Appointment` and `AppointmentService`.  
  - **Feature 7 — Reports & analytics:** Patient statistics, queue analytics, appointment reports, doctor performance, specialization utilization, custom report builder; `ReportService` and Streamlit reporting UI.  
- **Architecture:** Service-oriented design; separation of UI (Streamlit), services (business logic), and data (database layer); cross-database compatibility (MySQL/SQLite); design patterns in use (e.g. dependency injection for DB manager).  
- **Database:** Tables `patients`, `doctors`, `specializations`, `doctor_specializations`, `queue_entries`, `appointments`; optional `users`, `audit_logs` if present in schema.  
- **UI/UX:** Streamlit pages (navigation, statistics, interactive tables, forms, charts), run instructions (`streamlit run app.py`), and any Streamlit-specific setup.

**Out of scope — do NOT include or reference:**

- **PyQt5/PyQt6:** No mention of PyQt, PyQt5, PyQt6, or Qt in the generated documentation.  
- **PyQt-related files and docs:** Do not reference, summarize, or link to:  
  - The folder `archive/pyqt6/` or any files inside it (e.g. `main_window.py`, `start_gui.py`, `test_pyqt6_*.py`, etc.).  
  - Documents about PyQt cleanup, PyQt migration, or PyQt GUI troubleshooting (e.g. `PYQT6_CLEANUP_SUMMARY.md`, `STREAMLIT_MIGRATION.md` in a PyQt-migration context, `RUN_GUI.md`, `GUI_TROUBLESHOOTING.md`, `TROUBLESHOOTING_GUI.md`).  
- **Legacy GUI:** Do not describe or document a desktop GUI other than Streamlit. Treat the system as **Streamlit-only** for user and developer documentation.

---

### 2. DOCUMENTATION STRUCTURE TO PRODUCE

Generate documentation that satisfies the following three categories. Output in **Markdown (.md)**. Use clear headings, optional table of contents, and code blocks with language tags. Be precise and consistent with the codebase (no placeholders like “TBD” for required sections).

**2.1 User documentation**

- **User manual/guide:** Step-by-step instructions for end-users: how to run the app (Streamlit), navigate the interface, and perform core tasks (patients, specializations, queue, doctors, appointments, reports). Include run command and any prerequisites (Python, pip, dependencies).  
- **Feature walkthrough:** Walkthrough of major features with concrete examples (e.g. adding a patient, adding to queue, serving next patient, scheduling an appointment, viewing a report).  
- **FAQ:** Frequently asked questions and troubleshooting for the **Streamlit application** (e.g. run errors, database connection, common UI actions). No PyQt or legacy GUI FAQs.

**2.2 Developer documentation**

- **Architecture documentation:** System overview, layers (UI, services, data), design patterns, database design (tables and relationships), technology stack (Python, Streamlit, MySQL/SQLite). Describe the current implementation only; no PyQt or migration history.  
- **API documentation:** Service-layer API reference: for each relevant service (e.g. PatientService, SpecializationService, QueueService, DoctorService, AppointmentService, ReportService), document public methods, parameters, return values, and brief usage. Base this on the actual code in `src/services/`.  
- **Setup and installation guide:** Prerequisites (Python version, MySQL/XAMPP if used, SQLite), clone/setup steps, `pip install -r requirements.txt`, configuration (e.g. `src/config.py`), how to initialize the database and run the app with Streamlit. No PyQt or legacy GUI setup.  
- **Code documentation standards:** Conventions for module/class/method docstrings and comments (e.g. Google-style or project standard). Can reference or align with existing `CODE_DOCUMENTATION.md` in the project.

**2.3 Project documentation**

- **Requirements specification:** Functional requirements (e.g. patient, queue, specialization, doctor, appointment, reporting) and non-functional requirements (performance, usability, data integrity). Align with the implemented features; no requirements for PyQt or deprecated GUIs.  
- **Design documents:** High-level system design, architecture decisions, database design, and (if applicable) UML or diagrams. Reflect the **current** Streamlit + services + MySQL/SQLite design only.  
- **Implementation plan (or summary):** Phases, priorities, and what was implemented (features 1–5 and 7, Streamlit UI, database, services). Describe the implementation as it exists; do not include PyQt or migration from PyQt as part of the deliverable.  
- **Testing documentation:** Test strategy, test cases (e.g. database, services), and results. Reference `tests/` and any run instructions; do not include tests or instructions for PyQt/GUI.

---

### 3. QUALITY REQUIREMENTS

- **Accuracy:** All descriptions, APIs, file paths, and run instructions must match the **current** codebase (Streamlit app, `src/`, `app.py`, `tests/`). Do not describe removed or archived code (e.g. PyQt).  
- **Completeness:** Every required section above must have real content; no stub sections or “TBD.”  
- **Clarity and tone:** Clear, professional, academic tone suitable for a Masters-level IT project submission.  
- **Consistency:** Use the same terminology as the code (e.g. service names, model names, table names).  
- **Exclusion rule:** If in doubt, omit any mention of PyQt, Qt, legacy desktop GUI, and files under `archive/pyqt6/` or docs that are solely about PyQt migration/troubleshooting.

---

### 4. OUTPUT

Produce documentation that can be placed under `docs/documentation/` (and, where appropriate, `docs/implementation/` for implementation-focused content). Each major deliverable (e.g. User Manual, Architecture, API Documentation, Setup Guide, Requirements, Design, Testing) can be a separate section or file as long as the full structure in section 2 is covered. Use Markdown formatting, headings, lists, and code blocks throughout.
```

---

## How to Use This Prompt

1. **Copy** the entire content inside the ` ``` ` block above (from “You are generating…” through “…throughout.”).  
2. **Paste** it into your AI assistant (e.g. Cursor, ChatGPT, Claude) or give it to a writer as the main instruction.  
3. **Optionally attach or point to:**  
   - This file: `docs/documentation/DOCUMENTATION_GENERATION_PROMPT.md`  
   - The guideline files in `docs/documentation/` (e.g. `DOCUMENTATION_REQUIREMENTS_CHECKLIST.md`, `DOCUMENTATION_GUIDE.md`, `PROJECT_GUIDELINES.md`)  
   - Key implementation files: `app.py`, selected files under `src/models/`, `src/services/`, `src/database/`, and `docs/implementation/IMPLEMENTATION_SESSION_SUMMARY.md` (for implementation detail only; instruct the AI to ignore PyQt migration/cleanup content).  
4. **Exclusion reminder:** If the model ever mentions PyQt or legacy GUI, add: “Remember: do not include PyQt or legacy GUI; document only the Streamlit-based Hospital Management System.”

---

## Reference: Documentation Guidelines Location

- **Requirements checklist:** `docs/documentation/DOCUMENTATION_REQUIREMENTS_CHECKLIST.md`  
- **Master guide:** `docs/documentation/DOCUMENTATION_GUIDE.md`  
- **Project rubrics:** `docs/documentation/PROJECT_GUIDELINES.md`  
- **Implementation summary (use only non-PyQt parts):** `docs/implementation/IMPLEMENTATION_SESSION_SUMMARY.md`

**Excluded from documentation content:**  
`archive/pyqt6/`, `PYQT6_CLEANUP_SUMMARY.md`, `RUN_GUI.md`, `GUI_TROUBLESHOOTING.md`, `TROUBLESHOOTING_GUI.md`, and any doc or section that is solely about PyQt migration or PyQt GUI troubleshooting.
