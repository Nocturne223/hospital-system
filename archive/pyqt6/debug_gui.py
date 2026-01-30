"""
Debug GUI - Captures all errors and output
"""

import sys
import os
import traceback

# Redirect stderr to capture all errors
class ErrorCapture:
    def __init__(self):
        self.errors = []
        self.original_stderr = sys.stderr
    
    def write(self, text):
        self.errors.append(text)
        self.original_stderr.write(text)
    
    def flush(self):
        self.original_stderr.flush()

error_capture = ErrorCapture()
sys.stderr = error_capture

print("=" * 70)
print("GUI Debug Session")
print("=" * 70)
print(f"Python: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print()

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print(f"Project root: {project_root}")
print(f"Source directory: {src_dir}")
print()

# Step 1: Test PyQt6
print("Step 1: Testing PyQt6...")
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    print("[OK] PyQt6 imported successfully")
except Exception as e:
    print(f"[ERROR] PyQt6 import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 2: Test minimal QApplication
print("\nStep 2: Testing QApplication creation...")
try:
    app = QApplication(sys.argv)
    print("[OK] QApplication created")
    print(f"  - Application name: {app.applicationName()}")
    print(f"  - Platform: {app.platformName()}")
except Exception as e:
    print(f"[ERROR] QApplication creation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test window creation
print("\nStep 3: Testing window creation...")
try:
    window = QMainWindow()
    window.setWindowTitle("Debug Test Window")
    window.setGeometry(100, 100, 600, 400)
    
    label = QLabel("If you see this window, PyQt6 is working!\n\nThis window will close in 10 seconds.")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("font-size: 16px; padding: 20px;")
    window.setCentralWidget(label)
    
    print("[OK] Window created")
except Exception as e:
    print(f"[ERROR] Window creation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 4: Show window
print("\nStep 4: Showing window...")
try:
    window.show()
    print("[OK] Window.show() called")
    print("\n" + "=" * 70)
    print("WINDOW SHOULD BE VISIBLE NOW!")
    print("=" * 70)
    print("\nIf you don't see a window:")
    print("  1. Check Windows taskbar")
    print("  2. Try Alt+Tab")
    print("  3. Check if window opened on another monitor")
    print("\nWindow will close automatically in 10 seconds...")
    print()
    
    # Process events to make sure window appears
    app.processEvents()
    print("[OK] Events processed")
    
    # Run for 10 seconds
    import time
    start_time = time.time()
    while time.time() - start_time < 10:
        app.processEvents()
        time.sleep(0.1)
    
    print("\n[OK] Test completed - closing window")
    window.close()
    
except Exception as e:
    print(f"[ERROR] Window display failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 5: Test actual GUI import
print("\nStep 5: Testing actual GUI module import...")
try:
    from ui.main_window import MainWindow, main
    print("[OK] GUI module imported")
except Exception as e:
    print(f"[ERROR] GUI module import failed: {e}")
    traceback.print_exc()
    print("\nThis means there's an issue with the GUI code itself.")
    sys.exit(1)

# Step 6: Try to create MainWindow (but don't show it yet)
print("\nStep 6: Testing MainWindow creation (without showing)...")
try:
    # Create a new QApplication for this test
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication(sys.argv)
    
    print("Creating MainWindow instance...")
    main_window = MainWindow()
    print("[OK] MainWindow created successfully")
    print("  - Window title:", main_window.windowTitle())
    print("  - Window geometry:", main_window.geometry())
    
    # Don't show it yet - just test creation
    print("[OK] MainWindow creation test passed")
    
except Exception as e:
    print(f"[ERROR] MainWindow creation failed: {e}")
    traceback.print_exc()
    print("\nThis means there's an issue when creating the MainWindow.")
    print("The error might be in PatientManagementWidget initialization.")
    sys.exit(1)

print("\n" + "=" * 70)
print("ALL TESTS PASSED!")
print("=" * 70)
print("\nThe GUI components are working.")
print("If the window appeared in Step 4, PyQt6 is working correctly.")
print("\nNow try running the actual application:")
print("  python run_app_simple.py")
print("=" * 70)

# Check for any errors captured
if error_capture.errors:
    print("\nErrors captured during execution:")
    for error in error_capture.errors:
        print(f"  {error}")
