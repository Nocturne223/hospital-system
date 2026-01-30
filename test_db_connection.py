"""
Test MySQL Connection - Isolated Test
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("=" * 60)
print("Testing MySQL Connection")
print("=" * 60)

try:
    from config import USE_MYSQL, MYSQL_CONFIG
    print(f"USE_MYSQL: {USE_MYSQL}")
    print(f"Config: {MYSQL_CONFIG}")
except Exception as e:
    print(f"ERROR loading config: {e}")
    sys.exit(1)

if not USE_MYSQL:
    print("Not using MySQL - skipping test")
    sys.exit(0)

print("\nStep 1: Testing mysql.connector import...")
try:
    import mysql.connector
    print("[OK] mysql.connector imported")
except ImportError as e:
    print(f"[ERROR] mysql.connector not installed: {e}")
    print("Install with: pip install mysql-connector-python")
    sys.exit(1)

print("\nStep 2: Testing direct MySQL connection...")
try:
    import mysql.connector
    print(f"Connecting to {MYSQL_CONFIG['host']}:{MYSQL_CONFIG.get('port', 3306)}...")
    
    conn = mysql.connector.connect(
        host=MYSQL_CONFIG['host'],
        port=MYSQL_CONFIG.get('port', 3306),
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database'],
        connection_timeout=5
    )
    print("[OK] Direct connection successful!")
    
    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    db_name = cursor.fetchone()[0]
    print(f"[OK] Connected to database: {db_name}")
    
    # Check tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"[OK] Found {len(tables)} tables in database")
    
    cursor.close()
    conn.close()
    print("[OK] Connection closed successfully")
    
except mysql.connector.Error as e:
    print(f"[ERROR] MySQL connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check XAMPP Control Panel - MySQL should be 'Started'")
    print("2. Verify database 'hospital_system' exists")
    print("3. Check credentials in src/config.py")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 3: Testing DatabaseManager import...")
try:
    from database import DatabaseManager
    print("[OK] DatabaseManager imported")
except Exception as e:
    print(f"[ERROR] DatabaseManager import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 4: Testing DatabaseManager initialization...")
try:
    print("Creating DatabaseManager instance...")
    db = DatabaseManager(  # type: ignore
        host=MYSQL_CONFIG['host'],
        port=MYSQL_CONFIG.get('port', 3306),
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database']
    )
    print("[OK] DatabaseManager created successfully!")
    
except Exception as e:
    print(f"[ERROR] DatabaseManager initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests passed! Database connection is working.")
print("=" * 60)
