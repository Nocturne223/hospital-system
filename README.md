# Intelligent Hospital Management and Queueing System (HMS)

**Beta.ver.1.1 — LATEST**

A **web-based** hospital operations dashboard built with **Python** and **Streamlit**. Staff use a **browser** to manage patients, specializations (departments), waiting queues, doctors, appointments, and **Reports & Analytics** on the **Dashboard**—all backed by a relational database (**MySQL** or **SQLite**).

## Technical foundation

The codebase applies **Advanced OOP** principles as the structural baseline:

- **SOLID** — especially single-responsibility **service** classes and clear separation from persistence.  
- **Dependency injection** — services receive a shared **`DatabaseManager`** instance wired in `app.py` (`st.session_state`).  
- **Strategy-like database selection** — `src/database/__init__.py` resolves **MySQL** (`MySQLDatabaseManager`) or **SQLite** (`DatabaseManager`) from `src/config.py` without changing service-layer code.

**Analytics and charts** use **Pandas** and **Streamlit’s native chart APIs** (e.g. `st.bar_chart`). Separate charting stacks such as **Plotly** are intentionally omitted from the baseline requirements to keep the shell lightweight.

**Queue policy:** **priority first** (Super-Urgent → Urgent → Normal), then **FIFO** by `joined_at` (`ORDER BY status DESC, joined_at ASC` in `QueueService.get_queue`).  

**Appointments:** **interval-based conflict detection** blocks overlapping bookings for the same doctor (`AppointmentService.check_conflicts`).

## Quick start

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

**Windows:** you can run `run_streamlit.bat` from the project root.

Configure the database in **`src/config.py`** (`USE_MYSQL`, `MYSQL_CONFIG`, or `SQLITE_CONFIG`). Default browser URL: `http://localhost:8501`.

## Primary modules (complete)

| Module | Description |
|--------|-------------|
| **Dashboard** | Reports & Analytics: multiselect reports, date range, metrics, `st.bar_chart` visualizations |
| **Patient Management** | CRUD, search, filter, triage-style status |
| **Specialization Management** | Departments, max queue capacity, active/inactive |
| **Queue Management** | Enqueue, serve next, priorities, capacity, row actions, analytics |
| **Doctor Management** | Profiles, specialization assignments, employment status |
| **Appointment Management** | Schedule, edit, complete, cancel; overlap prevention |

## Documentation

| Location | Contents |
|----------|----------|
| [docs/documentation](docs/documentation/) | Architecture, design, API, requirements, **HOW_TO_RUN**, **RUN_STREAMLIT**, user manual, FAQ |
| [docs/documentation/INDEX.md](docs/documentation/INDEX.md) | Documentation index |

## Feature specs

See the **[features](features/)** directory for feature narratives and planning notes.

---

*Academic / pilot use. Production deployment requires separate security, access control, and compliance review.*
