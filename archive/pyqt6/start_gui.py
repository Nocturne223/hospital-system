"""
Alternative GUI Launcher with Better Error Handling
"""

import sys
import os

print("=" * 60)
print("Hospital Management System - GUI Launcher")
print("=" * 60)

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print(f"Project root: {project_root}")
print(f"Source directory: {src_dir}")
print(f"Python path includes src: {src_dir in sys.path}")

# Check PyQt6
print("\nChecking dependencies...")
try:
    import PyQt6
    print("[OK] PyQt6 is installed")
except ImportError:
    print("[ERROR] PyQt6 not installed!")
    print("Install with: pip install PyQt6")
    sys.exit(1)

# Check database connection
print("\nChecking database connection...")
try:
    from database import DatabaseManager
    from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG
    
    if USE_MYSQL:
        print(f"[OK] Using MySQL database: {MYSQL_CONFIG['database']}")
        print("Creating DatabaseManager instance...")
        
        # Try to create connection with timeout handling
        try:
            print("  - Calling DatabaseManager constructor...")
            db = DatabaseManager(  # pyright: ignore[reportCallIssue]
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG.get('port', 3306),
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password'],
                database=MYSQL_CONFIG['database']
            )
            print("[OK] DatabaseManager created successfully")
        except Exception as db_error:
            print(f"[ERROR] Database connection failed: {db_error}")
            import traceback
            traceback.print_exc()
            print("\nTroubleshooting:")
            print("1. Check XAMPP Control Panel - MySQL should be 'Started' (green)")
            print("2. Verify database 'hospital_system' exists in phpMyAdmin")
            print("3. Check credentials in src/config.py")
            print("\nContinuing anyway - GUI will start but database operations will fail.")
            db = None
    else:
        print(f"[OK] Using SQLite database: {SQLITE_CONFIG['db_path']}")
        db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])  # pyright: ignore[reportCallIssue]
        print("[OK] Database connection successful")
except Exception as e:
    print(f"[WARNING] Database check failed: {e}")
    import traceback
    traceback.print_exc()
    print("The GUI may still work, but database operations might fail.")
    db = None

# Import and run GUI
print("\nStarting GUI application...")
try:
    from ui.main_window import main
    print("[OK] GUI module imported successfully")
    print("\n" + "=" * 60)
    print("GUI Window should open now...")
    print("If you don't see a window, check:")
    print("  1. Look in taskbar")
    print("  2. Try Alt+Tab")
    print("  3. Check for error messages")
    print("=" * 60 + "\n")
    
    main()
    
except ImportError as e:
    print(f"\n[ERROR] Failed to import GUI module: {e}")
    print("\nTroubleshooting:")
    print("1. Check that src/ui/main_window.py exists")
    print("2. Verify all imports are correct")
    print("3. Check file permissions")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] Failed to start GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
