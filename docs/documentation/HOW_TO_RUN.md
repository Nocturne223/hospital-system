# How to Run the Hospital Management System

**Documentation:** Beta.ver.1.1 — LATEST  
**Application:** Browser-based **Streamlit** web app (`app.py`)

---

## Quick start

### 1. Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database

- **MySQL (e.g. XAMPP):** start MySQL, ensure database `hospital_system` exists, credentials match **`src/config.py`**.  
- **SQLite:** set `USE_MYSQL = False` in **`src/config.py`** and verify `SQLITE_CONFIG['db_path']`.

### 3. Start the application (recommended commands)

From the **project root** (folder containing `app.py`):

```bash
python -m streamlit run app.py
```

**Windows — batch launcher:**

```text
run_streamlit.bat
```

The app opens in your browser (default **`http://localhost:8501`**).

**Alternative:** If your environment provides `run_app.py` / `run_app.bat`, they may delegate to Streamlit; the canonical commands above always apply.

---

## Feature status — all six primary modules **Complete**

| Module | Status | Notes |
|--------|--------|--------|
| **Dashboard** (Reports & Analytics) | **Complete** | Multiselect report types, date range, Pandas + `st.bar_chart` |
| **Patient Management** | **Complete** | CRUD, search, filter, statistics |
| **Specialization Management** | **Complete** | Capacity, active/inactive, utilization context |
| **Queue Management** | **Complete** | Add/serve, priorities, capacity, row actions, analytics |
| **Doctor Management** | **Complete** | CRUD, multi-specialization assignment, status |
| **Appointments** | **Complete** | Schedule/edit/complete/cancel; **doctor overlap conflict detection** |

There are **no** “Coming Soon” or “Planned” labels for these modules in Beta v1.1.

---

## Using the interface (summary)

1. **Sidebar:** click **Dashboard**, **Patient Management**, **Specialization Management**, **Queue Management**, **Doctor Management**, or **Appointments**.  
2. **System status** and **Quick Stats** appear in the sidebar when the database connects.  
3. Each page: metrics → search/filters (where applicable) → action buttons → tables/forms.  
4. For edit/delete flows, select **one** row via the **Select** checkbox column, then use the action button above the table.

For step-by-step clicks and field names, see **[USER_MANUAL.md](USER_MANUAL.md)**.

---

## System requirements

- Python 3.9+ recommended (see `requirements.txt`)  
- Streamlit, Pandas, and (if MySQL) `mysql-connector-python`  
- Browser (Chrome, Edge, Firefox, etc.)

---

## Troubleshooting

| Issue | What to try |
|--------|-------------|
| `ModuleNotFoundError: streamlit` | `pip install -r requirements.txt` |
| `streamlit` command not found | Use `python -m streamlit run app.py` |
| Database connection error | XAMPP MySQL on, DB exists, check **`src/config.py`** |
| Port 8501 in use | `python -m streamlit run app.py --server.port 8502` |

---

## Quick reference commands

```bash
python -m streamlit run app.py
# Windows: run_streamlit.bat

pip install -r requirements.txt

# Optional: run tests (see tests/)
pytest
```

---

**Last Updated:** March 2026 — aligned with Beta.ver.1.1 implementation.
