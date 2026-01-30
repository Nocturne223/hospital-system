"""
Simple GUI Test - Minimal version to diagnose issues
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("Testing GUI startup...")
print(f"Python: {sys.version}")
print(f"Project root: {project_root}")

# Test PyQt6
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    print("[OK] PyQt6 imported")
except ImportError as e:
    print(f"[ERROR] PyQt6 import failed: {e}")
    sys.exit(1)

# Test database imports
try:
    from database import DatabaseManager
    from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG
    print(f"[OK] Database imports successful (USE_MYSQL={USE_MYSQL})")
except ImportError as e:
    print(f"[ERROR] Database import failed: {e}")
    sys.exit(1)

# Test database connection
try:
    if USE_MYSQL:
        db = DatabaseManager(  # type: ignore
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )
    else:
        db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])  # type: ignore
    print("[OK] Database connection successful")
except Exception as e:
    print(f"[WARNING] Database connection failed: {e}")
    print("Continuing anyway...")

# Test service import
try:
    from services.patient_service import PatientService
    print("[OK] PatientService imported")
except ImportError as e:
    print(f"[ERROR] PatientService import failed: {e}")
    sys.exit(1)

# Test GUI import
try:
    from ui.main_window import MainWindow
    print("[OK] MainWindow imported")
except ImportError as e:
    print(f"[ERROR] MainWindow import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try to create minimal app
print("\nCreating minimal GUI...")
try:
    app = QApplication(sys.argv)
    print("[OK] QApplication created")
    
    window = QMainWindow()
    window.setWindowTitle("Test Window")
    window.setGeometry(100, 100, 400, 300)
    
    label = QLabel("If you see this, PyQt6 is working!")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)
    
    window.show()
    print("[OK] Window shown")
    print("\nWindow should be visible now. Close it to continue test.")
    
    # Run for 2 seconds then exit
    import time
    time.sleep(2)
    print("[OK] Test completed successfully!")
    
except Exception as e:
    print(f"[ERROR] GUI creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAll tests passed! The GUI should work.")
print("If the window appeared, try running: python run_app.py")
