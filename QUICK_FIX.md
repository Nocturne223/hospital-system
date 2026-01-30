# Quick Fix for GUI Not Starting

## The Problem
`python run_app.py` exits immediately without showing the GUI window.

## Common Causes & Solutions

### 1. **Database Connection Issue** (Most Likely)
The app might be crashing because it can't connect to MySQL.

**Check:**
- Open XAMPP Control Panel
- Make sure MySQL is **Started** (green)
- Verify database `hospital_system` exists in phpMyAdmin

**Fix:**
```bash
# Option A: Use SQLite instead (for testing)
# Edit src/config.py and set:
USE_MYSQL = False

# Option B: Fix MySQL connection
# Make sure XAMPP MySQL is running
# Check src/config.py has correct credentials
```

### 2. **PyQt6 Display Issue**
On some systems, PyQt6 needs a display server.

**Try:**
```bash
# Run with explicit display (if on WSL/Linux)
export DISPLAY=:0
python run_app.py

# Or try the diagnostic script
python start_gui.py
```

### 3. **Import Errors**
**Check:**
```bash
python -c "from PyQt6.QtWidgets import QApplication; print('OK')"
```

**If fails:**
```bash
pip install PyQt6
```

### 4. **Run Diagnostic Script**
```bash
python start_gui.py
```
This will show detailed error messages.

### 5. **Check Error Output**
Run in terminal to see errors:
```bash
python run_app.py 2>&1 | more
```

Or use the batch file:
```bash
run_app.bat
```

## Quick Test

Try this minimal test:
```bash
python test_gui_simple.py
```

If this works, the issue is in the main app initialization.

## Most Common Solution

**90% of the time, it's the database connection:**

1. Start XAMPP MySQL
2. Verify database exists
3. Check `src/config.py` credentials
4. Try running again

If still failing, share the error output from:
```bash
python start_gui.py
```
