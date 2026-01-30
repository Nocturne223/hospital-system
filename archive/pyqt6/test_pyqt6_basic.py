"""
Basic PyQt6 Test - Minimal test to see if PyQt6 works at all
"""

import sys
import os

print("Testing PyQt6 Basic Functionality")
print("=" * 60)

try:
    print("Step 1: Importing PyQt6...")
    import PyQt6
    print(f"[OK] PyQt6 imported - version info available")
except Exception as e:
    print(f"[ERROR] Cannot import PyQt6: {e}")
    sys.exit(1)

try:
    print("\nStep 2: Importing QtWidgets...")
    from PyQt6 import QtWidgets
    print("[OK] QtWidgets imported")
except Exception as e:
    print(f"[ERROR] Cannot import QtWidgets: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\nStep 3: Creating QApplication...")
    app = QtWidgets.QApplication(sys.argv)
    print("[OK] QApplication created")
    print(f"  - Platform: {app.platformName()}")
    print(f"  - Application name: {app.applicationName()}")
except Exception as e:
    print(f"[ERROR] Cannot create QApplication: {e}")
    import traceback
    traceback.print_exc()
    print("\nThis might indicate:")
    print("  1. PyQt6 installation is corrupted")
    print("  2. Missing system dependencies")
    print("  3. Display/graphics driver issue")
    sys.exit(1)

try:
    print("\nStep 4: Creating simple window...")
    from PyQt6.QtWidgets import QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    
    window = QMainWindow()
    window.setWindowTitle("Test")
    window.resize(400, 300)
    
    label = QLabel("Test Window")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)
    
    print("[OK] Window created")
except Exception as e:
    print(f"[ERROR] Cannot create window: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\nStep 5: Showing window (non-blocking test)...")
    window.show()
    print("[OK] window.show() called")
    
    # Process events once
    app.processEvents()
    print("[OK] Events processed")
    
    print("\n" + "=" * 60)
    print("If you see a window, PyQt6 is working!")
    print("The window should be visible now.")
    print("=" * 60)
    
    # Don't run event loop - just test if window can be shown
    print("\n[OK] Basic PyQt6 test completed")
    print("Window was created and shown (may not be visible without event loop)")
    
except Exception as e:
    print(f"[ERROR] Cannot show window: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("All basic tests passed!")
print("=" * 60)
print("\nIf you didn't see a window, try running with event loop:")
print("  python test_pyqt6_with_loop.py")
