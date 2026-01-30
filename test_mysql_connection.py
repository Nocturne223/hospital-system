"""Test MySQL database connection for Hospital Management System"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from database.mysql_db_manager import MySQLDatabaseManager
except ImportError:
    print("ERROR: mysql-connector-python not installed.")
    print("Install it with: pip install mysql-connector-python")
    sys.exit(1)


def test_connection():
    """Test MySQL connection and database setup"""
    print("=" * 60)
    print("Hospital Management System - MySQL Connection Test")
    print("=" * 60)
    
    try:
        print("\n1. Testing MySQL connection...")
        db = MySQLDatabaseManager(
            host='localhost',
            port=3306,
            user='root',
            password='',  # Empty for default XAMPP
            database='hospital_system'
        )
        print("   [OK] Connection successful!")
        
        # Test query - get tables
        print("\n2. Checking database tables...")
        tables = db.execute_query("SHOW TABLES")
        table_names = [list(table.values())[0] for table in tables]
        
        expected_tables = [
            'patients', 'doctors', 'specializations',
            'doctor_specializations', 'queue_entries',
            'appointments', 'users', 'audit_logs'
        ]
        
        print(f"   Found {len(table_names)} tables:")
        for table in table_names:
            status = "[OK]" if table in expected_tables else "[WARNING]"
            print(f"   {status} {table}")
        
        # Check if all expected tables exist
        missing_tables = set(expected_tables) - set(table_names)
        if missing_tables:
            print(f"\n   [WARNING] Missing tables: {', '.join(missing_tables)}")
            print("   -> Import schema_mysql.sql in phpMyAdmin")
        else:
            print("\n   [OK] All expected tables found!")
        
        # Test table counts
        print("\n3. Checking table status...")
        print(f"\n   {'Table Name':<30} {'Row Count':<15} {'Status'}")
        print("   " + "-" * 60)
        
        for table in expected_tables:
            try:
                count = db.get_table_count(table)
                status = "OK" if db.table_exists(table) else "MISSING"
                print(f"   {table:<30} {count:<15} {status}")
            except Exception as e:
                print(f"   {table:<30} {'ERROR':<15} {str(e)[:30]}")
        
        # Test basic operations
        print("\n4. Testing basic operations...")
        
        # Test INSERT
        try:
            db.execute_update(
                "INSERT INTO patients (full_name, date_of_birth, status) VALUES (%s, %s, %s)",
                ("Test Patient", "1990-01-01", 0)
            )
            print("   [OK] INSERT operation works")
            
            # Test SELECT
            results = db.execute_query(
                "SELECT * FROM patients WHERE full_name = %s",
                ("Test Patient",)
            )
            if results:
                print("   [OK] SELECT operation works")
            
            # Clean up test data
            db.execute_update(
                "DELETE FROM patients WHERE full_name = %s",
                ("Test Patient",)
            )
            print("   [OK] DELETE operation works")
            
        except Exception as e:
            print(f"   [WARNING] Operation test failed: {e}")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] MySQL connection test completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Update your code to use MySQLDatabaseManager")
        print("2. Test your application with MySQL")
        print("3. Connect Navicat to view/manage database")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        print("\n" + "=" * 60)
        print("Troubleshooting Steps:")
        print("=" * 60)
        print("\n1. Check XAMPP MySQL Service:")
        print("   → Open XAMPP Control Panel")
        print("   → Make sure MySQL is 'Started' (green)")
        
        print("\n2. Verify Database Exists:")
        print("   → Open phpMyAdmin: http://localhost/phpmyadmin")
        print("   → Check if 'hospital_system' database exists")
        
        print("\n3. Check Connection Credentials:")
        print("   → Host: localhost")
        print("   → Port: 3306")
        print("   → User: root")
        print("   → Password: (empty for default XAMPP)")
        
        print("\n4. Install MySQL Connector:")
        print("   → pip install mysql-connector-python")
        
        print("\n5. Import Schema:")
        print("   → phpMyAdmin → hospital_system → SQL tab")
        print("   → Import: src/database/schema_mysql.sql")
        
        return False


if __name__ == "__main__":
    test_connection()
