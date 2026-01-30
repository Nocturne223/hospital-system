# GUI Application Troubleshooting

## Common Issues and Solutions

### Issue 1: "python run_app.py won't work"

**Possible Causes**:
1. PyQt6 not installed
2. Import errors
3. Database connection issues
4. Window opens but is hidden

**Solutions**:

#### Solution A: Use Alternative Launcher
```bash
python start_gui.py
```
This launcher shows detailed error messages and checks dependencies.

#### Solution B: Check PyQt6 Installation
```bash
python -m pip install PyQt6
```

#### Solution C: Check Database Connection
Make sure:
- XAMPP MySQL is running
- Database `hospital_system` exists
- Credentials in `src/config.py` are correct

#### Solution D: Check if Window is Hidden
- Look in Windows taskbar
- Try Alt+Tab to find the window
- Check if window opened on another monitor

---

### Issue 2: "ModuleNotFoundError: No module named 'PyQt6'"

**Solution**:
```bash
pip install PyQt6
# OR
python -m pip install PyQt6
```

---

### Issue 3: "Can't connect to MySQL"

**Check**:
1. XAMPP Control Panel → MySQL is "Started" (green)
2. Database `hospital_system` exists in phpMyAdmin
3. Credentials in `src/config.py`:
   - host: localhost
   - user: root
   - password: (empty for default XAMPP)

**Fix**:
- Start MySQL in XAMPP
- Create database if missing
- Update config if needed

---

### Issue 4: "Import errors"

**Solution**:
Make sure you're in the project root directory:
```bash
cd C:\Users\Alfred Paldez\Downloads\AJEM\MIT\MIT504\FinalProj\Sys
python run_app.py
```

---

### Issue 5: Window Opens but Shows No Data

**Solution**:
1. Add sample data:
   ```bash
   python src/database/add_sample_patients.py
   ```
2. Click "Refresh" button in GUI
3. Check database has data in phpMyAdmin

---

## Diagnostic Steps

### Step 1: Check Dependencies
```bash
python -c "import PyQt6; print('PyQt6 OK')"
python -c "import mysql.connector; print('MySQL connector OK')"
```

### Step 2: Test Database Connection
```bash
python test_mysql_connection.py
```

### Step 3: Test Backend
```bash
python tests/test_patient_service.py
```

### Step 4: Run Diagnostic Launcher
```bash
python start_gui.py
```

This will show detailed information about what's working and what's not.

---

## Alternative Ways to Run

### Method 1: Direct Python Import
```python
import sys
sys.path.insert(0, 'src')
from ui.main_window import main
main()
```

### Method 2: From src directory
```bash
cd src
python -m ui.main_window
```

### Method 3: Use start_gui.py (Recommended)
```bash
python start_gui.py
```

---

## Expected Behavior

When you run the application:
1. A window should open
2. You should see "Patient Management" tab
3. Table should show patients (if data exists)
4. Buttons should be clickable

If window doesn't appear:
- Check taskbar
- Check for error messages in terminal
- Try `python start_gui.py` for detailed diagnostics

---

## Getting Help

If the GUI still won't start:
1. Run: `python start_gui.py` and share the output
2. Check error messages in terminal
3. Verify all dependencies installed
4. Check database is accessible

---

**Last Updated**: January 30, 2026
