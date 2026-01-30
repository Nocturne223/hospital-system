"""
PyQt6 Test with Event Loop
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QTimer

print("Creating QApplication...")
app = QApplication(sys.argv)

print("Creating window...")
window = QMainWindow()
window.setWindowTitle("PyQt6 Test - Close Me")
window.setGeometry(100, 100, 500, 300)

label = QLabel(
    "PyQt6 is working!\n\n"
    "If you see this window, everything is OK.\n\n"
    "This window will close automatically in 5 seconds."
)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
label.setStyleSheet("font-size: 14px; padding: 20px;")
window.setCentralWidget(label)

print("Showing window...")
window.show()

# Auto-close after 5 seconds
def close_window():
    print("Closing window...")
    window.close()
    app.quit()

timer = QTimer()
timer.timeout.connect(close_window)
timer.setSingleShot(True)
timer.start(5000)  # 5 seconds

print("\n" + "=" * 60)
print("Window should be visible now!")
print("It will close automatically in 5 seconds.")
print("=" * 60 + "\n")

# Run event loop
print("Starting event loop...")
sys.exit(app.exec())
