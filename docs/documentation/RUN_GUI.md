# How to Run the GUI

## Quick Start

### Method 1: Standard Launcher (Recommended)
```bash
python run_app.py
```

### Method 2: Diagnostic Launcher (Shows detailed info)
```bash
python start_gui.py
```

### Method 3: Batch File (Windows)
```bash
run_app.bat
```

## If GUI Doesn't Appear

### Check 1: Database Connection
```bash
python test_db_connection.py
```
This should show all tests passing.

### Check 2: Look for the Window
- Check Windows taskbar
- Try Alt+Tab to find the window
- Check if window opened on another monitor

### Check 3: Check for Errors
Run the diagnostic launcher:
```bash
python start_gui.py
```
This will show detailed error messages.

## Common Issues

### Issue: Window Opens but Closes Immediately
**Solution**: Check the terminal/console for error messages. The app might be crashing due to:
- Missing dependencies
- Database connection issues
- Import errors

### Issue: "ModuleNotFoundError"
**Solution**: Install missing dependencies:
```bash
pip install PyQt6 mysql-connector-python
```

### Issue: Database Connection Fails
**Solution**: 
1. Start XAMPP MySQL
2. Verify database exists
3. Check `src/config.py` credentials

## Expected Behavior

When you run the app:
1. A window should open (may take 2-3 seconds)
2. You should see "Patient Management" tab
3. Table should show patients (if data exists)
4. Buttons should be clickable

## Testing

Before running GUI, test components:
```bash
# Test database
python test_db_connection.py

# Test backend
python tests/test_patient_service.py

# Test interactive CLI
python interactive_test.py
```

## Still Having Issues?

1. Run diagnostic: `python start_gui.py`
2. Check error messages in terminal
3. Verify all dependencies installed
4. Check database is accessible
