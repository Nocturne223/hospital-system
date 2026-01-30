# How to View the Database

There are several ways to view and interact with the SQLite database. Here are the options:

## Option 1: Python Database Viewer Script (Recommended)

We've created a simple Python script to view the database.

### View Database Summary
```bash
python src/database/view_db.py
```

### View a Specific Table
```bash
python src/database/view_db.py --table patients
python src/database/view_db.py --table doctors
python src/database/view_db.py --table specializations
python src/database/view_db.py --table queue_entries
python src/database/view_db.py --table appointments
```

### View Summary Only
```bash
python src/database/view_db.py --summary
```

### Custom Database Path
```bash
python src/database/view_db.py --db-path data/custom_database.db
```

## Option 2: SQLite Command Line Tool

SQLite comes with a command-line tool that you can use directly.

### Open Database
```bash
sqlite3 data/hospital_system.db
```

### Useful SQLite Commands
Once inside SQLite:
```sql
-- List all tables
.tables

-- View table structure
.schema patients

-- View all data from a table
SELECT * FROM patients;

-- View with formatting
.mode column
.headers on
SELECT * FROM patients;

-- Exit
.quit
```

### Example Session
```bash
$ sqlite3 data/hospital_system.db
SQLite version 3.x.x
Enter ".help" for usage hints.
sqlite> .tables
patients  doctors  specializations  ...
sqlite> .mode column
sqlite> .headers on
sqlite> SELECT * FROM patients LIMIT 5;
sqlite> .quit
```

## Option 3: DB Browser for SQLite (GUI Tool)

**DB Browser for SQLite** is a free, open-source GUI tool for viewing and editing SQLite databases.

### Installation
1. Download from: https://sqlitebrowser.org/
2. Install the application
3. Open the application

### Using DB Browser
1. Click "Open Database"
2. Navigate to `data/hospital_system.db`
3. Browse tables, view data, run queries, and edit data

**Features:**
- Browse Database Structure
- View/Edit Table Data
- Execute SQL Queries
- Export Data
- Import Data

## Option 4: VS Code Extension

If you're using VS Code, you can install the **SQLite Viewer** extension.

1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search for "SQLite Viewer"
3. Install the extension
4. Right-click on `data/hospital_system.db` → "Open Database"

## Option 5: Python Interactive Session

You can also use Python interactively:

```python
from src.database import DatabaseManager

# Open database
db = DatabaseManager()

# View all patients
patients = db.execute_query("SELECT * FROM patients")
for patient in patients:
    print(dict(patient))

# View table count
count = db.get_table_count('patients')
print(f"Total patients: {count}")

# View specific patient
patient = db.execute_query(
    "SELECT * FROM patients WHERE patient_id = ?",
    (1,)
)
if patient:
    print(dict(patient[0]))
```

## Quick Reference

### Database Location
- **Main Database**: `data/hospital_system.db`
- **Test Database**: `data/test_hospital_system.db` (created by tests)
- **Backups**: `data/backups/hospital_system_backup_*.db`

### Available Tables
- `patients` - Patient information
- `doctors` - Doctor information
- `specializations` - Medical specializations
- `doctor_specializations` - Doctor-specialization assignments
- `queue_entries` - Queue management
- `appointments` - Appointment scheduling
- `users` - User accounts
- `audit_logs` - System logs

### Common Queries

**View all patients:**
```sql
SELECT * FROM patients;
```

**View patients by status:**
```sql
SELECT * FROM patients WHERE status = 1;  -- Urgent
```

**View queue entries:**
```sql
SELECT q.*, p.full_name, s.name as specialization
FROM queue_entries q
JOIN patients p ON q.patient_id = p.patient_id
JOIN specializations s ON q.specialization_id = s.specialization_id;
```

**View appointments:**
```sql
SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id;
```

## Troubleshooting

### Database Not Found
If you get "Database not found", initialize it first:
```bash
python src/database/init_db.py
```

### Permission Errors
Make sure you have read/write permissions to the `data/` directory.

### Empty Database
If the database is empty, that's normal! You need to add data through the application or manually insert test data.

---

**Recommended**: Start with the Python viewer script (`view_db.py`) for quick viewing, and use DB Browser for SQLite for more advanced operations.
