# GUI Troubleshooting Guide

## Current Status
The GUI launchers are not showing windows. This guide helps diagnose and fix the issue.

## Diagnostic Tests

Run these tests in order:

### 1. Basic PyQt6 Test
```bash
python test_pyqt6_basic.py
```
**Expected**: All steps pass, window may or may not be visible (needs event loop)

### 2. PyQt6 with Event Loop
```bash
python test_pyqt6_with_loop.py
```
**Expected**: Window appears for 5 seconds then closes automatically

### 3. Comprehensive Diagnostic
```bash
python diagnose_gui.py
```
**Expected**: All tests pass, window should appear and stay open

### 4. Fixed Launcher (Delayed DB Init)
```bash
python run_app_fixed.py
```
**Expected**: Window appears immediately, database connects in background

## Common Issues & Solutions

### Issue 1: Window Doesn't Appear
**Symptoms**: Script runs but no window shows

**Possible Causes**:
1. Window is minimized in taskbar
2. Window opened on another monitor
3. Window is behind other windows
4. Event loop not running

**Solutions**:
- Check Windows taskbar for the application
- Press Alt+Tab to cycle through windows
- Check all monitors if you have multiple
- Make sure `app.exec()` is being called

### Issue 2: Script Exits Immediately
**Symptoms**: Script runs and exits with code 2147483647

**Possible Causes**:
1. Fatal error during initialization
2. Database connection hanging
3. Import error

**Solutions**:
- Run `python diagnose_gui.py` to see where it fails
- Check if database initialization is blocking
- Try `run_app_fixed.py` which delays DB init

### Issue 3: Database Connection Hanging
**Symptoms**: Script hangs at "Connecting to MySQL..."

**Solutions**:
- Use `run_app_fixed.py` which delays database initialization
- Check XAMPP MySQL is running
- Verify database credentials in `src/config.py`

## What I've Fixed

1. **Delayed Database Initialization** - Database now connects after window is shown
2. **Better Error Handling** - More detailed error messages
3. **Multiple Test Scripts** - To isolate the problem

## Files Created

- `test_pyqt6_basic.py` - Basic PyQt6 functionality test
- `test_pyqt6_with_loop.py` - PyQt6 with event loop
- `diagnose_gui.py` - Comprehensive diagnostic
- `run_app_fixed.py` - Fixed launcher with delayed DB init

## Next Steps

1. **Run the diagnostic**:
   ```bash
   python diagnose_gui.py
   ```
   Share the output - this will tell us exactly where it's failing.

2. **Try the fixed launcher**:
   ```bash
   python run_app_fixed.py
   ```
   This delays database initialization so window should appear immediately.

3. **Check if window is hidden**:
   - Look in taskbar
   - Try Alt+Tab
   - Check all monitors

## If Nothing Works

If none of the launchers show a window:

1. **Check PyQt6 installation**:
   ```bash
   python -c "from PyQt6.QtWidgets import QApplication; print('OK')"
   ```

2. **Check for display issues**:
   - Try `python test_pyqt6_with_loop.py`
   - If this doesn't show a window, it's a PyQt6/display issue

3. **Check Windows event viewer** for application crashes

4. **Try reinstalling PyQt6**:
   ```bash
   pip uninstall PyQt6
   pip install PyQt6
   ```

## Expected Behavior

When working correctly:
1. Script starts
2. Window appears within 1-2 seconds
3. Window stays open until closed
4. Database connects in background (may show warning if fails)

## Getting Help

If still not working, share:
1. Output from `python diagnose_gui.py`
2. Output from `python test_pyqt6_with_loop.py`
3. Any error messages
4. Whether you see the window in taskbar (even if not visible)
