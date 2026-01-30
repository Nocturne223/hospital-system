# Using XAMPP and Navicat with Hospital Management System

## Overview

You have two options for using XAMPP and Navicat:

1. **Option A: Keep SQLite + Use Navicat** (Easiest - No code changes)
   - Continue using SQLite database
   - Use Navicat to view/manage SQLite database
   - No code changes needed

2. **Option B: Switch to MySQL (XAMPP) + Use Navicat** (More features)
   - Use MySQL database from XAMPP
   - Use Navicat to manage MySQL database
   - Requires code changes to DatabaseManager

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

## Code Changes for MySQL (Option B)

If you choose Option B, here's what needs to change:

### 1. Install MySQL Connector
Add to `requirements.txt`:
```txt
mysql-connector-python>=8.0.0
# OR
pymysql>=1.0.0
```

### 2. Update DatabaseManager

Create a new file `src/database/mysql_db_manager.py`:

```python
import mysql.connector
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import logging

class MySQLDatabaseManager:
    def __init__(self, 
                 host='localhost',
                 port=3306,
                 user='root',
                 password='',
                 database='hospital_system'):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        conn = mysql.connector.connect(**self.config)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    # Similar methods to SQLite version...
```

### 3. Create MySQL Schema
Convert `schema.sql` to MySQL format (minor syntax differences).

---

## Recommendation

### For Academic Project: **Option A (SQLite + Navicat)**
- ✅ Faster to set up
- ✅ No additional services to run
- ✅ Works perfectly for the project scope
- ✅ Navicat can view/edit SQLite easily
- ✅ Less complexity

### For Production-Like Setup: **Option B (MySQL + Navicat)**
- ✅ More realistic production environment
- ✅ Better for demonstrating enterprise features
- ✅ More powerful database features
- ⚠️ Requires code changes
- ⚠️ Need to keep XAMPP running

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
