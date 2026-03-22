# Running the Streamlit Application

**Documentation:** Beta.ver.1.1 — LATEST

## Quick start

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application** (project root = directory that contains `app.py`)

   ```bash
   python -m streamlit run app.py
   ```

   **Windows:** double-click or run:

   ```text
   run_streamlit.bat
   ```

   If the `streamlit` executable is not on `PATH`, always prefer `python -m streamlit`.

3. **Browser** — Streamlit serves the app (default **`http://localhost:8501`**).

---

## Prerequisites

- Python 3.9+ (see `requirements.txt`)
- **MySQL** running if `USE_MYSQL = True` in `src/config.py` (e.g. XAMPP), database `hospital_system` created  
- **OR SQLite** if `USE_MYSQL = False`, with valid `SQLITE_CONFIG['db_path']`

---

## Modules — all **Complete** (Beta v1.1)

| Sidebar module | Status | Capabilities (summary) |
|------------------|--------|-------------------------|
| **Dashboard** | **Complete** | Reports & Analytics: patient / queue / appointment / doctor / specialization reports; custom report builder; **Pandas** + **`st.bar_chart`** (no Plotly in baseline deps) |
| **Patient Management** | **Complete** | CRUD, search, filter by triage status, statistics |
| **Specialization Management** | **Complete** | Departments, max queue capacity, active/inactive |
| **Queue Management** | **Complete** | Enqueue by priority; **Super-Urgent > Urgent > Normal**, then **FIFO** by `joined_at`; serve next; capacity limits; row actions; analytics |
| **Doctor Management** | **Complete** | Profiles, assignments to specializations, status |
| **Appointments** | **Complete** | Full lifecycle; **overlap conflict detection** per doctor (time + duration) |

No **“Coming soon”** flags apply to these features in the current release documentation.

---

## Configuration

**`src/config.py`**

- `USE_MYSQL = True` — MySQL (`MYSQL_CONFIG`)  
- `USE_MYSQL = False` — SQLite (`SQLITE_CONFIG`)

Restart Streamlit after changes.

---

## Troubleshooting

### Database connection error

1. MySQL: XAMPP service running, database exists.  
2. Confirm host, user, password, database name in `src/config.py`.  
3. SQLite: path exists and is writable.

### Port in use

```bash
python -m streamlit run app.py --server.port 8502
```

### Import errors

Run commands from the **project root**; ensure `src` is discoverable (as arranged by `app.py`).

---

## Development

Auto-reload on save (optional):

```bash
python -m streamlit run app.py --server.runOnSave true
```

---

**Last Updated:** March 2026 — Beta.ver.1.1
