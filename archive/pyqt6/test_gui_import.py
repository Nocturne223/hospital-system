"""
Test GUI Import - Isolated Test
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("=" * 60)
print("Testing GUI Import")
print("=" * 60)

print("\nStep 1: Testing PyQt6 import...")
try:
    from PyQt6.QtWidgets import QApplication
    print("[OK] PyQt6 imported")
except Exception as e:
    print(f"[ERROR] PyQt6 import failed: {e}")
    sys.exit(1)

print("\nStep 2: Testing database imports...")
try:
    from database import DatabaseManager
    from config import USE_MYSQL, MYSQL_CONFIG
    print("[OK] Database imports successful")
except Exception as e:
    print(f"[ERROR] Database import failed: {e}")
    sys.exit(1)

print("\nStep 3: Testing service imports...")
try:
    from services.patient_service import PatientService
    print("[OK] PatientService imported")
except Exception as e:
    print(f"[ERROR] PatientService import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 4: Testing GUI module import...")
try:
    print("Importing ui.main_window...")
    from ui import main_window
    print("[OK] ui.main_window module imported")
except Exception as e:
    print(f"[ERROR] GUI module import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 5: Testing MainWindow class...")
try:
    from ui.main_window import MainWindow
    print("[OK] MainWindow class imported")
except Exception as e:
    print(f"[ERROR] MainWindow import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 6: Testing main() function import...")
try:
    from ui.main_window import main
    print("[OK] main() function imported")
except Exception as e:
    print(f"[ERROR] main() function import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("All imports successful!")
print("=" * 60)
print("\nThe GUI should work. Try running: python run_app.py")
