# MySQL Setup Guide - Hospital Management System

## Prerequisites Completed ✅

- [x] XAMPP installed
- [x] MySQL service running
- [x] Database `hospital_system` created in phpMyAdmin

---

## Next Steps

### Step 1: Install MySQL Connector for Python

Open terminal/command prompt and run:

```bash
pip install mysql-connector-python
```

**Alternative** (if mysql-connector-python doesn't work):
```bash
pip install pymysql
```

**Verify Installation**:
```bash
pip list | findstr mysql
# Should show: mysql-connector-python or pymysql
```

---

### Step 2: Import MySQL Schema

You have two options:

#### Option A: Using phpMyAdmin (Recommended - Easiest)

1. **Open phpMyAdmin**: http://localhost/phpmyadmin
2. **Select Database**: Click on `hospital_system` in the left sidebar
3. **Go to SQL Tab**: Click on the "SQL" tab at the top
4. **Open Schema File**: 
   - Click "Choose File" or "Import files"
   - Navigate to: `src/database/schema_mysql.sql`
   - Click "Go" or "Import"
5. **Verify**: You should see success messages and all tables created

#### Option B: Using MySQL Command Line

1. **Open Command Line**:
   ```bash
   # Navigate to XAMPP MySQL bin directory
   cd C:\xampp\mysql\bin
   ```

2. **Run MySQL**:
   ```bash
   mysql -u root -p
   # Enter password (usually empty for XAMPP, just press Enter)
   ```

3. **Import Schema**:
   ```sql
   USE hospital_system;
   SOURCE C:/path/to/your/project/src/database/schema_mysql.sql;
   ```

4. **Verify Tables**:
   ```sql
   SHOW TABLES;
   -- Should show: patients, doctors, specializations, etc.
   ```

---

### Step 3: Verify Tables Created

In phpMyAdmin:

1. Select `hospital_system` database
2. You should see these tables:
   - ✅ patients
   - ✅ doctors
   - ✅ specializations
   - ✅ doctor_specializations
   - ✅ queue_entries
   - ✅ appointments
   - ✅ users
   - ✅ audit_logs

**Total**: 8 tables

---

### Step 4: Update DatabaseManager to Use MySQL

The MySQL DatabaseManager is already created at `src/database/mysql_db_manager.py`. 

**Update your code to use MySQL instead of SQLite**:

#### Option A: Update Existing Code

Create a configuration file or update imports:

**Create `src/config.py`**:
```python
# Database configuration
USE_MYSQL = True  # Set to True for MySQL, False for SQLite

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Empty for default XAMPP
    'database': 'hospital_system'
}
```

**Update `src/database/__init__.py`**:
```python
"""
Database package for Hospital Management System.
"""

from src.config import USE_MYSQL

if USE_MYSQL:
    from .mysql_db_manager import MySQLDatabaseManager as DatabaseManager
else:
    from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
```

#### Option B: Direct Import (Quick Test)

In your code, directly import MySQL manager:

```python
from src.database.mysql_db_manager import MySQLDatabaseManager as DatabaseManager

# Initialize with your MySQL credentials
db = DatabaseManager(
    host='localhost',
    port=3306,
    user='root',
    password='',  # Empty for default XAMPP
    database='hospital_system'
)
```

---

### Step 5: Test MySQL Connection

Create a test script: `test_mysql_connection.py`

```python
"""Test MySQL database connection"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.database.mysql_db_manager import MySQLDatabaseManager

def test_connection():
    """Test MySQL connection"""
    try:
        print("Testing MySQL connection...")
        db = MySQLDatabaseManager(
            host='localhost',
            port=3306,
            user='root',
            password='',  # Empty for default XAMPP
            database='hospital_system'
        )
        
        # Test query
        tables = db.execute_query("SHOW TABLES")
        print(f"\n✅ Connection successful!")
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {list(table.values())[0]}")
        
        # Test table counts
        print("\n📊 Table Status:")
        table_names = ['patients', 'doctors', 'specializations', 
                      'queue_entries', 'appointments', 'users']
        for table in table_names:
            count = db.get_table_count(table)
            print(f"   {table}: {count} rows")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if MySQL service is running in XAMPP")
        print("2. Verify database 'hospital_system' exists")
        print("3. Check username/password")
        print("4. Verify mysql-connector-python is installed")
        return False

if __name__ == "__main__":
    test_connection()
```

**Run the test**:
```bash
python test_mysql_connection.py
```

---

### Step 6: Update requirements.txt

Add MySQL connector to `requirements.txt`:

```txt
# Database
mysql-connector-python>=8.0.0
# OR
# pymysql>=1.0.0
```

---

## Configuration Summary

### MySQL Connection Details

```python
{
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Empty for default XAMPP
    'database': 'hospital_system'
}
```

### Default XAMPP Settings
- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: (empty/blank)
- **Database**: hospital_system

---

## Troubleshooting

### Issue: "Access denied for user 'root'@'localhost'"

**Solution**:
1. Check if you set a password during XAMPP installation
2. If yes, use that password in the configuration
3. If no, password should be empty string `''`

### Issue: "Can't connect to MySQL server"

**Solution**:
1. Open XAMPP Control Panel
2. Make sure MySQL service is **Started** (green)
3. Check if port 3306 is available
4. Try restarting MySQL service

### Issue: "Unknown database 'hospital_system'"

**Solution**:
1. Go to phpMyAdmin
2. Create database `hospital_system` if it doesn't exist
3. Or verify the database name is correct

### Issue: "Table doesn't exist"

**Solution**:
1. Make sure you imported `schema_mysql.sql`
2. Check in phpMyAdmin that tables exist
3. Verify you're using the correct database

### Issue: "ModuleNotFoundError: No module named 'mysql'"

**Solution**:
```bash
pip install mysql-connector-python
# OR
pip install pymysql
```

---

## Verification Checklist

- [ ] MySQL connector installed (`pip install mysql-connector-python`)
- [ ] Database `hospital_system` exists in phpMyAdmin
- [ ] Schema imported (all 8 tables created)
- [ ] MySQL service running in XAMPP
- [ ] Test connection script runs successfully
- [ ] Can query tables from Python
- [ ] DatabaseManager updated to use MySQL

---

## Next Steps After Setup

1. **Test Database Operations**:
   - Create a patient
   - Add to queue
   - Test all CRUD operations

2. **Update Application Code**:
   - Change imports to use MySQLDatabaseManager
   - Update any SQLite-specific code
   - Test all features

3. **Connect Navicat** (if using):
   - Open Navicat
   - Create MySQL connection
   - Connect to `hospital_system` database
   - View and manage data

---

## Quick Reference

### Import Schema in phpMyAdmin
1. phpMyAdmin → Select `hospital_system` → SQL tab
2. Choose file: `src/database/schema_mysql.sql`
3. Click Go

### Test Connection
```python
from src.database.mysql_db_manager import MySQLDatabaseManager

db = MySQLDatabaseManager(
    host='localhost',
    user='root',
    password='',
    database='hospital_system'
)
```

### View in phpMyAdmin
- URL: http://localhost/phpmyadmin
- Database: hospital_system
- Browse tables to see data

---

## Support

If you encounter issues:
1. Check XAMPP MySQL is running
2. Verify database exists
3. Check connection credentials
4. Review error messages
5. Test with simple query first

---

**Last Updated**: January 30, 2026  
**Status**: Ready for MySQL Setup
