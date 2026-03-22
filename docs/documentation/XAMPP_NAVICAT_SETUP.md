# Using XAMPP and Navicat with Hospital Management System

**Beta.ver.1.1 — LATEST:** MySQL and SQLite are **both fully integrated**. Switching engines is a **configuration change only** — set **`USE_MYSQL = True`** (and fill **`MYSQL_CONFIG`**) or **`USE_MYSQL = False`** (and **`SQLITE_CONFIG`**) in **`src/config.py`**, then restart **`python -m streamlit run app.py`**. No rewrites of `DatabaseManager` logic are required for normal use; `src/database/__init__.py` selects the concrete manager.

## Overview

1. **Option A: SQLite + Navicat**
   - Set `USE_MYSQL = False` in `src/config.py`
   - Point Navicat at the SQLite file (e.g. under `data/`)
   - Zero database server install

2. **Option B: MySQL (XAMPP) + Navicat** (common for labs)
   - Install/start **MySQL** in XAMPP; create database **`hospital_system`**
   - Set **`USE_MYSQL = True`** and matching **`MYSQL_CONFIG`**
   - Use Navicat as a MySQL client — **no application code changes** beyond config

---

## Option A: SQLite + Navicat (Recommended for Quick Start)

### Advantages
- ✅ No code changes needed
- ✅ Works immediately
- ✅ Navicat supports SQLite
- ✅ Single file database (easy to backup)

### Setup Steps

#### 1. Install Navicat
1. Download Navicat from: https://www.navicat.com/
2. Install Navicat (you can use the free trial or purchase)
3. Navicat supports SQLite, MySQL, PostgreSQL, and more

#### 2. Connect to SQLite Database in Navicat
1. Open Navicat
2. Click **Connection** → **SQLite**
3. Connection Settings:
   - **Connection Name**: Hospital System
   - **Database File**: Browse to `data/hospital_system.db`
   - Click **Test Connection** → **OK**

#### 3. View Your Database
- Navigate to the connection in Navicat
- Expand to see all tables
- Double-click any table to view/edit data
- Use the SQL editor to run queries

### Using Navicat with SQLite
- ✅ View all tables and data
- ✅ Edit data directly
- ✅ Run SQL queries
- ✅ Export/Import data
- ✅ Design database structure
- ✅ Create backups

---

## Option B: MySQL (XAMPP) + Navicat

### Advantages
- ✅ More powerful database features
- ✅ Better for multi-user scenarios
- ✅ More similar to production databases
- ✅ Advanced features (stored procedures, triggers, etc.)

### Setup Steps

#### 1. Install and Start XAMPP
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Start XAMPP Control Panel
4. Start **MySQL** service

#### 2. Create MySQL Database
1. Open phpMyAdmin (http://localhost/phpmyadmin)
2. Click **New** to create a database
3. Database name: `hospital_system`
4. Collation: `utf8mb4_general_ci`
5. Click **Create**

#### 3. Convert Schema to MySQL
The SQLite schema needs minor adjustments for MySQL:
- `INTEGER PRIMARY KEY AUTOINCREMENT` → `INT AUTO_INCREMENT PRIMARY KEY`
- `TEXT` → `VARCHAR` or `TEXT`
- `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` → `TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
- Remove `IF NOT EXISTS` (or keep it, MySQL supports it)

#### 4. Update DatabaseManager for MySQL
You'll need to modify `src/database/db_manager.py` to use MySQL instead of SQLite.

#### 5. Connect Navicat to MySQL
1. Open Navicat
2. Click **Connection** → **MySQL**
3. Connection Settings:
   - **Connection Name**: Hospital System MySQL
   - **Host**: `localhost` or `127.0.0.1`
   - **Port**: `3306` (default)
   - **Username**: `root` (default XAMPP)
   - **Password**: (leave empty for default XAMPP, or your password)
   - Click **Test Connection** → **OK**

---

## MySQL schema

Use the repository’s MySQL schema / init scripts (see `src/database/` and project root helpers). Minor SQL dialect differences from SQLite are already handled in the dual-manager design.

---

## Recommendation

### For quick start: **Option A (SQLite + Navicat)**
- ✅ No database server
- ✅ Single file backup

### For XAMPP / lab parity: **Option B (MySQL + Navicat)**
- ✅ Toggle **`USE_MYSQL = True`** in **`src/config.py`**
- ✅ Keep XAMPP MySQL running while using the app
- ✅ **No** custom rewrite of `DatabaseManager` required for switching

---

## Quick Start: SQLite + Navicat

1. **Install Navicat** (if not already installed)
2. **Open Navicat** → **Connection** → **SQLite**
3. **Database File**: `C:\Users\Alfred Paldez\Downloads\AJEM\MIT\MIT504\FinalProj\Sys\data\hospital_system.db`
4. **Click OK** → You're done!

You can now:
- View all tables
- Edit data
- Run SQL queries
- Export data
- Design database structure

---

## Using Navicat Features

### View Data
- Double-click any table to view data
- Use filters to search
- Sort by any column

### Edit Data
- Click on any cell to edit
- Right-click for more options
- Add/Delete rows

### SQL Editor
- Click **Query** → **New Query**
- Write SQL queries
- Execute and see results

### Export/Import
- Right-click table → **Export Wizard**
- Choose format (CSV, Excel, SQL, etc.)
- Import data similarly

### Database Design
- View table structures
- See relationships
- Modify schema (be careful!)

---

## Troubleshooting

### Navicat Can't Connect to SQLite
- Check file path is correct
- Ensure database file exists
- Check file permissions

### XAMPP MySQL Won't Start
- Check if port 3306 is already in use
- Check XAMPP error logs
- Try changing MySQL port in XAMPP config

### Connection Issues
- Verify database file exists
- Check file permissions
- Ensure path is correct (use absolute path)

---

## Next Steps

1. **If choosing Option A**: Just install Navicat and connect to SQLite
2. **If choosing Option B**: 
   - Install XAMPP
   - Create MySQL database
   - Let me know and I'll help convert the code to MySQL

**Which option would you prefer?**
