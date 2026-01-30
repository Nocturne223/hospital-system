"""
Fixed GUI Launcher - Better error handling and delayed DB init
"""

import sys
import os

print("=" * 70)
print("Hospital Management System - Starting...")
print("=" * 70)

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    print("\n[1/4] Importing PyQt6...")
    from PyQt6.QtWidgets import QApplication
    print("      [OK] PyQt6 imported")
    
    print("\n[2/4] Creating QApplication...")
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    print("      [OK] QApplication created")
    
    print("\n[3/4] Importing GUI module...")
    from ui.main_window import MainWindow
    print("      [OK] GUI module imported")
    
    print("\n[4/4] Creating and showing window...")
    window = MainWindow()
    window.show()
    print("      [OK] Window created and shown")
    
    print("\n" + "=" * 70)
    print("GUI WINDOW SHOULD BE VISIBLE NOW!")
    print("=" * 70)
    print("\nIf you don't see a window:")
    print("  - Check Windows taskbar")
    print("  - Try Alt+Tab")
    print("  - Check if window opened on another monitor")
    print("\nDatabase connection will initialize in the background...")
    print("=" * 70 + "\n")
    
    # Run event loop
    sys.exit(app.exec())
    
except KeyboardInterrupt:
    print("\n\nApplication interrupted by user")
    sys.exit(0)
    
except Exception as e:
    print(f"\n\n[ERROR] Failed to start application: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 70)
    print("Troubleshooting:")
    print("  1. Check PyQt6: pip install PyQt6")
    print("  2. Check MySQL is running in XAMPP")
    print("  3. Run: python test_pyqt6_with_loop.py")
    print("=" * 70)
    input("\nPress Enter to exit...")
    sys.exit(1)
