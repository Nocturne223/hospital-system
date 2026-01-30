"""
Minimal GUI Test - No Database
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("=" * 60)
print("Minimal GUI Test (No Database)")
print("=" * 60)

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

print("\nCreating QApplication...")
app = QApplication(sys.argv)
print("[OK] QApplication created")

print("\nCreating window...")
window = QMainWindow()
window.setWindowTitle("Test Window - If you see this, GUI works!")
window.setGeometry(100, 100, 500, 300)

label = QLabel("GUI is working!\n\nClose this window to continue.")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
window.setCentralWidget(label)

print("[OK] Window created")
print("\nShowing window...")
window.show()
print("[OK] Window shown")
print("\n" + "=" * 60)
print("Window should be visible now!")
print("If you see the window, GUI is working.")
print("Close the window to continue...")
print("=" * 60 + "\n")

# Run for 5 seconds then exit
import time
time.sleep(5)
print("\nTest completed!")
