"""
Simple GUI Launcher - Minimal Error Handling
"""

import sys
import os

print("Starting Hospital Management System...")
print("=" * 60)

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    print("Importing GUI module...")
    from ui.main_window import main
    print("[OK] GUI module imported")
    
    print("\nStarting GUI application...")
    print("Window should open in a moment...")
    print("=" * 60 + "\n")
    
    main()
    
except KeyboardInterrupt:
    print("\nApplication interrupted by user")
    sys.exit(0)
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("Troubleshooting:")
    print("1. Check if PyQt6 is installed: pip install PyQt6")
    print("2. Check if MySQL is running in XAMPP")
    print("3. Run diagnostic: python start_gui.py")
    print("=" * 60)
    sys.exit(1)
