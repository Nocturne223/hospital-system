# Hospital Management System — Setup and Installation Guide

**Beta.ver.1.1 — LATEST** — **Streamlit** web application (`app.py`)

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Development Setup](#development-setup)

---

## Prerequisites

### Required software

#### 1. Python 3.9+ (recommended)
- **Download**: https://www.python.org/downloads/
- **Verify**:
  ```bash
  python --version
  ```

#### 2. pip
- **Verify**: `pip --version`

#### 3. Web browser
- Chrome, Edge, Firefox, or equivalent (for `http://localhost:8501`)

#### 4. MySQL (optional but common)
- **XAMPP** with MySQL running if `USE_MYSQL = True` in `src/config.py`

### System requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux  
- **RAM**: 4GB minimum (8GB recommended)  
- **Storage**: 500MB+ free  
- **Display**: 1280×720 minimum  

---

## Installation steps

### Step 1: Obtain the project

Clone or extract the repository and note the **project root** (folder containing `app.py`).

### Step 2: Open a terminal in the project root

```bash
cd path/to/hospital-system
```

### Step 3: Virtual environment (recommended)

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

**Expected packages include** (non-exhaustive): `streamlit`, `pandas`, `mysql-connector-python` (for MySQL), `pytest`, `python-dateutil`. There is **no PyQt6** requirement.

### Step 5: Configure database

Edit **`src/config.py`**:

- **`USE_MYSQL = True`** — set `MYSQL_CONFIG` (host, user, password, database `hospital_system`, etc.) for XAMPP/MySQL.  
- **`USE_MYSQL = False`** — SQLite file path in `SQLITE_CONFIG['db_path']`.

### Step 6: Initialize database

Run the project’s database initialization scripts as documented for your environment (e.g. `python src/database/init_db.py` for SQLite, or MySQL schema/seed scripts if applicable). Ensure the `data/` directory exists for SQLite if used.

### Step 7: Run the application

From the **project root**:

```bash
python -m streamlit run app.py
```

**Windows (batch launcher):**

```text
run_streamlit.bat
```

The app opens in the browser (default **`http://localhost:8501`**). If the `streamlit` command is not on `PATH`, always use **`python -m streamlit`**.

---

## Configuration

- **Database**: `src/config.py` — `USE_MYSQL`, `MYSQL_CONFIG`, `SQLITE_CONFIG`  
- **No separate PyQt / desktop theme config** — UI is Streamlit defaults plus `app.py` styling.

---

## Verification

1. **`python --version`** — 3.9+ recommended  
2. **`pip list`** — includes `streamlit`, `pandas`  
3. **`pytest`** or `python tests/test_database.py` — as applicable  
4. **Run Streamlit** — sidebar shows **Dashboard**, **Patient**, **Specialization**, **Queue**, **Doctor**, **Appointments**; database status **Connected** when configuration is correct  

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'`

```bash
pip install -r requirements.txt
```

### Database connection error

- **MySQL:** XAMPP MySQL running, database created, credentials in `src/config.py`  
- **SQLite:** path writable, `data/` exists  

### Port 8501 in use

```bash
python -m streamlit run app.py --server.port 8502
```

### Import errors

Run commands from **project root**; `app.py` adds `src` to `sys.path`.

---

## Development setup

```bash
python -m venv venv
# activate venv
pip install -r requirements.txt
pytest
```

Optional quality tools (`black`, `flake8`) — comment in `requirements.txt`; **pytest-qt is not used** for Streamlit.

### Project structure (high level)

```
hospital-system/
├── app.py                 # Streamlit entry
├── run_streamlit.bat
├── src/
│   ├── config.py
│   ├── database/
│   ├── models/
│   └── services/
├── tests/
├── docs/documentation/
├── data/                  # SQLite file (if used)
└── requirements.txt
```

---

## Additional resources

- [USER_MANUAL.md](USER_MANUAL.md)  
- [HOW_TO_RUN.md](HOW_TO_RUN.md)  
- [RUN_STREAMLIT.md](RUN_STREAMLIT.md)  
- [ARCHITECTURE.md](ARCHITECTURE.md)  
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md)  
- [FAQ.md](FAQ.md)  

---

**Last Updated:** March 2026  
**Version:** Beta.ver.1.1
