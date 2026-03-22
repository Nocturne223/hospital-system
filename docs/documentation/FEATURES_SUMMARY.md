# Hospital Management System — Features Summary

**Beta.ver.1.1 — LATEST**  
This document summarizes feature areas and their **implementation status** in the current Streamlit-based HMS. Detailed narratives remain in the `features/` directory where applicable.

## Feature list

### 1. Enhanced Patient Management
**File**: `features/01-patient-management.md`

**Key capabilities (implemented)**:
- Patient registration and profiles, search/filter, triage status (Normal / Urgent / Super-Urgent), CRUD via **`PatientService`** and Streamlit UI.

**Status**: **Implemented** (Streamlit)

---

### 2. Enhanced Specialization Management
**File**: `features/02-specialization-management.md`

**Key capabilities (implemented)**:
- Specialization CRUD, queue capacity, active/inactive, utilization context in lists.

**Status**: **Implemented**

---

### 3. Enhanced Queue Management
**File**: `features/03-queue-management.md`

**Key capabilities (implemented)**:
- Priority-based ordering (**Super-Urgent > Urgent > Normal**, then **FIFO** by `joined_at`), capacity enforcement, serve/next, row actions, analytics panel.

**Status**: **Implemented**

---

### 4. Doctor Management
**File**: `features/04-doctor-management.md`

**Key capabilities (implemented)**:
- Doctor profiles, multi-specialization assignment, employment status, soft-delete pattern where applicable.

**Status**: **Implemented**

---

### 5. Appointment System
**File**: `features/05-appointment-system.md`

**Key capabilities (implemented)**:
- Schedule, edit, complete, cancel; **doctor overlap conflict detection** (time + duration).

**Status**: **Implemented**

---

### 6. User Interface & Experience
**File**: `features/06-user-interface.md`

**Key capabilities (implemented)**:
- **Browser-based Streamlit** application: sidebar navigation, forms, `st.data_editor`, metrics, **native Streamlit charts** (`st.bar_chart`) with **Pandas** — **no Plotly** in baseline dependencies.

**Status**: **Implemented**

---

### 7. Reporting & Analytics
**File**: `features/07-reporting-analytics.md`

**Key capabilities (implemented)**:
- **Dashboard** module: multiselect report types, date range, patient/queue/appointment/doctor/specialization summaries, custom report builder. Export depth may vary; core reporting is live in-app.

**Status**: **Implemented**

---

### 8. Data Management & Persistence
**File**: `features/08-data-management.md`

**Key capabilities (implemented)**:
- Relational schema, **SQLite or MySQL** via `src/config.py`, backup-oriented APIs where present in `DatabaseManager`.

**Status**: **Implemented** (dual-database strategy)

---

### 9. Security & Authentication
**File**: `features/09-security-authentication.md`

**Key capabilities**:
- **Beta v1.1** operates on a **trusted workstation** model; dedicated login/RBAC UI is **not** part of the baseline Streamlit shell. Schema may include `users` for future work.

**Status**: **Partial / future** (documented in Beta scope as out of baseline UI)

---

## Implementation priority — **100% complete** (delivered scope)

| Phase | Scope | Status |
|-------|--------|--------|
| **Phase 1** | Data layer, Patient, Specialization, Queue, Streamlit shell | **Complete** |
| **Phase 2** | Doctor, Appointments, UI polish | **Complete** |
| **Phase 3** | Dashboard / Reporting & Analytics, documentation alignment | **Complete** |

*Full enterprise security, RBAC UI, and external export pipelines may be tracked as future enhancements outside Beta v1.1 UI scope.*

---

## Quick start (current app)

1. `pip install -r requirements.txt`
2. Configure `src/config.py` (`USE_MYSQL` / `MYSQL_CONFIG` / `SQLITE_CONFIG`)
3. Initialize database per project scripts as needed
4. Run: **`python -m streamlit run app.py`** or **`run_streamlit.bat`**

---

*For detailed requirements per feature, see individual files under `features/`.*
