"""
Comprehensive GUI Diagnostic
"""

import sys
import os
import traceback

print("=" * 70)
print("COMPREHENSIVE GUI DIAGNOSTIC")
print("=" * 70)

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Test 1: PyQt6 import
print("\n[TEST 1] PyQt6 Import")
print("-" * 70)
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    print("[PASS] PyQt6 imported successfully")
except Exception as e:
    print(f"[FAIL] PyQt6 import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: QApplication creation
print("\n[TEST 2] QApplication Creation")
print("-" * 70)
try:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    print(f"[PASS] QApplication created")
    print(f"       Platform: {app.platformName()}")
    print(f"       App name: {app.applicationName()}")
except Exception as e:
    print(f"[FAIL] QApplication creation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Simple window
print("\n[TEST 3] Simple Window Creation")
print("-" * 70)
try:
    test_window = QMainWindow()
    test_window.setWindowTitle("Diagnostic Test Window")
    test_window.setGeometry(100, 100, 400, 300)
    
    label = QLabel("Diagnostic Test\n\nIf you see this, basic GUI works!")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    test_window.setCentralWidget(label)
    
    print("[PASS] Simple window created")
    test_window.show()
    print("[PASS] window.show() called")
    
    app.processEvents()
    print("[PASS] Events processed")
    print("[INFO] Simple window should be visible (may close quickly)")
    
    # Close test window
    test_window.close()
    
except Exception as e:
    print(f"[FAIL] Simple window failed: {e}")
    traceback.print_exc()

# Test 4: Database imports
print("\n[TEST 4] Database Module Import")
print("-" * 70)
try:
    from database import DatabaseManager
    from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG
    print(f"[PASS] Database modules imported")
    print(f"       USE_MYSQL: {USE_MYSQL}")
except Exception as e:
    print(f"[FAIL] Database import failed: {e}")
    traceback.print_exc()

# Test 5: Service import
print("\n[TEST 5] Service Module Import")
print("-" * 70)
try:
    from services.patient_service import PatientService
    print("[PASS] PatientService imported")
except Exception as e:
    print(f"[FAIL] Service import failed: {e}")
    traceback.print_exc()

# Test 6: GUI module import
print("\n[TEST 6] GUI Module Import")
print("-" * 70)
try:
    from ui.main_window import MainWindow, main
    print("[PASS] GUI module imported")
except Exception as e:
    print(f"[FAIL] GUI module import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 7: MainWindow creation (without showing)
print("\n[TEST 7] MainWindow Creation (No Display)")
print("-" * 70)
try:
    print("Creating MainWindow instance...")
    main_window = MainWindow()
    print("[PASS] MainWindow created")
    print(f"       Title: {main_window.windowTitle()}")
    print(f"       Geometry: {main_window.geometry()}")
    print(f"       Central widget: {type(main_window.centralWidget()).__name__}")
except Exception as e:
    print(f"[FAIL] MainWindow creation failed: {e}")
    traceback.print_exc()
    print("\n[INFO] This error likely occurs during PatientManagementWidget initialization")
    print("       The database connection might be hanging here.")
    sys.exit(1)

# Test 8: Show MainWindow
print("\n[TEST 8] Showing MainWindow")
print("-" * 70)
try:
    print("Calling window.show()...")
    main_window.show()
    print("[PASS] window.show() called")
    
    print("Processing events...")
    app.processEvents()
    print("[PASS] Events processed")
    
    print("\n" + "=" * 70)
    print("MAIN WINDOW SHOULD BE VISIBLE NOW!")
    print("=" * 70)
    print("\nIf you see the window:")
    print("  ✓ GUI is working correctly")
    print("  ✓ The issue was likely database initialization blocking")
    print("\nIf you DON'T see the window:")
    print("  - Check Windows taskbar")
    print("  - Try Alt+Tab")
    print("  - Window might be minimized or on another monitor")
    print("\nWindow will stay open. Close it manually or press Ctrl+C.")
    print("=" * 70 + "\n")
    
    # Run event loop
    print("Starting event loop...")
    sys.exit(app.exec())
    
except KeyboardInterrupt:
    print("\n\n[INFO] Application interrupted by user")
    sys.exit(0)
except Exception as e:
    print(f"\n[FAIL] Error showing window: {e}")
    traceback.print_exc()
    sys.exit(1)
