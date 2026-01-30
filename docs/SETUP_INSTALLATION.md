# Hospital Management System - Setup and Installation Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Development Setup](#development-setup)

---

## Prerequisites

### Required Software

#### 1. Python 3.8 or Higher
- **Download**: https://www.python.org/downloads/
- **Verify Installation**:
  ```bash
  python --version
  # Should show Python 3.8.x or higher
  ```

#### 2. pip (Python Package Manager)
- Usually included with Python
- **Verify Installation**:
  ```bash
  pip --version
  ```

#### 3. Git (Optional, for version control)
- **Download**: https://git-scm.com/downloads

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Display**: 1280x720 minimum resolution

---

## Installation Steps

### Step 1: Download Project Files

1. Download or clone the project repository
2. Extract to your desired location
3. Note the project directory path

### Step 2: Navigate to Project Directory

```bash
cd path/to/Hospital-System
```

### Step 3: Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting PyQt6>=6.5.0
Collecting pytest>=7.4.0
...
Successfully installed PyQt6-6.5.0 pytest-7.4.0 ...
```

### Step 5: Initialize Database

```bash
python src/database/init_db.py
```

**Expected Output:**
```
Initializing database...
Database schema created successfully
✅ Database initialized successfully!
```

### Step 6: (Optional) Add Sample Data

```bash
python src/database/add_sample_data.py
```

This adds sample data for testing purposes.

### Step 7: Run the Application

```bash
python src/main.py
```

---

## Configuration

### Database Configuration

#### Default Database Location
- **Path**: `data/hospital_system.db`
- **Backup Location**: `data/backups/`

#### Custom Database Path

Edit `src/main.py` or configuration file:

```python
from src.database import DatabaseManager

db = DatabaseManager(db_path='custom/path/database.db')
```

### Application Configuration

#### Settings File (if implemented)
Location: `config/settings.ini` or `config/settings.json`

Example configuration:
```ini
[database]
path = data/hospital_system.db
backup_enabled = true
backup_interval = 24

[ui]
theme = default
language = en
```

---

## Verification

### Verify Installation

#### 1. Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

#### 2. Check Dependencies
```bash
pip list
# Should show PyQt6, pytest, etc.
```

#### 3. Test Database
```bash
python tests/test_database.py
```

**Expected Output:**
```
[PASS] - Table Creation
[PASS] - Basic Operations
[PASS] - Foreign Keys
[PASS] - Backup/Restore

Total: 4/4 tests passed
```

#### 4. View Database
```bash
python src/database/view_db.py --summary
```

**Expected Output:**
```
DATABASE SUMMARY
Table Name                     Row Count       Status
patients                       0               OK
doctors                        0               OK
...
```

#### 5. Run Application
```bash
python src/main.py
```

Application window should open without errors.

---

## Troubleshooting

### Common Issues

#### Issue: Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Add Python to PATH during installation
2. Or use `python3` instead of `python`
3. Or use full path: `C:\Python39\python.exe`

#### Issue: pip Not Found

**Error**: `'pip' is not recognized`

**Solution**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### Issue: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'PyQt6'`

**Solution**:
```bash
pip install PyQt6
# Or reinstall all dependencies
pip install -r requirements.txt
```

#### Issue: Database Error

**Error**: `Database not found` or `Database error`

**Solution**:
1. Verify database file exists: `data/hospital_system.db`
2. Reinitialize database:
   ```bash
   python src/database/init_db.py
   ```
3. Check file permissions
4. Verify directory exists: `data/`

#### Issue: Permission Denied

**Error**: `Permission denied` when creating database

**Solution**:
1. Run with appropriate permissions
2. Check directory write permissions
3. Create `data/` directory manually if needed

#### Issue: Import Errors

**Error**: `ImportError: cannot import name 'DatabaseManager'`

**Solution**:
1. Verify project structure is correct
2. Check you're in the project root directory
3. Verify `src/` directory exists
4. Check `__init__.py` files exist

---

## Development Setup

### For Developers

#### 1. Clone Repository
```bash
git clone <repository-url>
cd Hospital-System
```

#### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install black flake8 pytest-qt
```

#### 3. Set Up IDE

**VS Code**:
1. Install Python extension
2. Install Pylance extension
3. Configure Python interpreter to use venv

**PyCharm**:
1. Open project
2. Configure Python interpreter
3. Set up run configurations

#### 4. Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_database.py

# Run with coverage
pytest --cov=src tests/
```

#### 5. Code Quality

**Format Code**:
```bash
black src/
```

**Lint Code**:
```bash
flake8 src/
```

### Project Structure

```
Hospital-System/
├── src/
│   ├── database/        # Database layer
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── ui/              # User interface
│   └── utils/           # Utilities
├── tests/               # Test files
├── docs/                # Documentation
├── data/                # Database files
├── requirements.txt     # Dependencies
└── README.md           # Project readme
```

---

## Post-Installation

### First Run Checklist

- [ ] Application launches successfully
- [ ] Database is initialized
- [ ] Can view database summary
- [ ] Sample data loaded (if used)
- [ ] No error messages in console

### Initial Configuration

1. **Create Admin User** (if authentication implemented)
2. **Set Up Specializations**
3. **Add Doctors**
4. **Configure Settings**

### Backup Setup

1. **Enable Automatic Backups** (if implemented)
2. **Set Backup Schedule**
3. **Test Backup/Restore**

---

## Uninstallation

### Remove Application

1. **Stop Application**: Close all running instances
2. **Backup Data**: Copy `data/` directory if needed
3. **Delete Project Directory**: Remove entire project folder
4. **Remove Virtual Environment**: Delete `venv/` directory
5. **Optional**: Uninstall Python packages
   ```bash
   pip uninstall PyQt6 pytest python-dateutil
   ```

### Keep Data

If you want to keep data but remove application:
1. Backup `data/hospital_system.db`
2. Delete project files
3. Restore database when reinstalling

---

## Additional Resources

- [User Manual](USER_MANUAL.md) - How to use the system
- [Architecture Documentation](ARCHITECTURE.md) - System design
- [API Documentation](API_DOCUMENTATION.md) - Service layer APIs
- [FAQ](FAQ.md) - Common questions

---

## Support

For installation issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review error messages
3. Check system requirements
4. Contact technical support

---

**Last Updated**: January 30, 2026  
**Version**: 1.0
