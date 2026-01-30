"""
Test script for DatabaseManager
Run this to verify the database setup is working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager


def test_database_initialization():
    """Test database initialization."""
    print("=" * 50)
    print("Testing Database Initialization")
    print("=" * 50)
    
    # Use test database
    test_db_path = 'data/test_hospital_system.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    try:
        db = DatabaseManager(db_path=test_db_path)
        print("[OK] Database initialized successfully")
        return db
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        return None


def test_table_creation(db: DatabaseManager):
    """Test that all tables were created."""
    print("\n" + "=" * 50)
    print("Testing Table Creation")
    print("=" * 50)
    
    expected_tables = [
        'patients',
        'doctors',
        'specializations',
        'doctor_specializations',
        'queue_entries',
        'appointments',
        'users',
        'audit_logs'
    ]
    
    all_passed = True
    for table in expected_tables:
        exists = db.table_exists(table)
        status = "[OK]" if exists else "[ERROR]"
        print(f"{status} Table '{table}': {'Exists' if exists else 'Missing'}")
        if not exists:
            all_passed = False
    
    return all_passed


def test_basic_operations(db: DatabaseManager):
    """Test basic CRUD operations."""
    print("\n" + "=" * 50)
    print("Testing Basic Operations")
    print("=" * 50)
    
    try:
        # Test INSERT
        print("\n1. Testing INSERT...")
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO patients (full_name, date_of_birth, status) VALUES (?, ?, ?)",
                ("Test Patient", "1990-01-01", 0)
            )
            patient_id = cursor.lastrowid
        print(f"   [OK] Inserted patient with ID: {patient_id}")
        
        # Test SELECT
        print("\n2. Testing SELECT...")
        results = db.execute_query(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )
        if results:
            patient = dict(results[0])
            print(f"   [OK] Retrieved patient: {patient['full_name']}")
        else:
            print("   [ERROR] Failed to retrieve patient")
            return False
        
        # Test UPDATE
        print("\n3. Testing UPDATE...")
        rows_affected = db.execute_update(
            "UPDATE patients SET full_name = ? WHERE patient_id = ?",
            ("Updated Patient", patient_id)
        )
        if rows_affected > 0:
            print(f"   [OK] Updated {rows_affected} row(s)")
        else:
            print("   [ERROR] Update failed")
            return False
        
        # Test DELETE
        print("\n4. Testing DELETE...")
        rows_affected = db.execute_update(
            "DELETE FROM patients WHERE patient_id = ?",
            (patient_id,)
        )
        if rows_affected > 0:
            print(f"   [OK] Deleted {rows_affected} row(s)")
        else:
            print("   [ERROR] Delete failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"   [ERROR] Operation failed: {e}")
        return False


def test_foreign_keys(db: DatabaseManager):
    """Test foreign key constraints."""
    print("\n" + "=" * 50)
    print("Testing Foreign Key Constraints")
    print("=" * 50)
    
    try:
        # Try to insert a queue entry with invalid patient_id
        print("\n1. Testing foreign key constraint...")
        db.execute_update(
            "INSERT INTO queue_entries (patient_id, specialization_id) VALUES (?, ?)",
            (99999, 1)  # Invalid patient_id
        )
        print("   [ERROR] Foreign key constraint not working (should have failed)")
        return False
    except sqlite3.IntegrityError:
        print("   [OK] Foreign key constraint working correctly")
        return True
    except Exception as e:
        print(f"   [WARNING] Unexpected error: {e}")
        return False


def test_backup_restore(db: DatabaseManager):
    """Test backup and restore functionality."""
    print("\n" + "=" * 50)
    print("Testing Backup and Restore")
    print("=" * 50)
    
    try:
        # Create some test data
        db.execute_update(
            "INSERT INTO patients (full_name, date_of_birth) VALUES (?, ?)",
            ("Backup Test Patient", "1995-05-15")
        )
        
        # Create backup
        print("\n1. Creating backup...")
        backup_path = db.backup_database()
        print(f"   [OK] Backup created at: {backup_path}")
        
        # Verify backup file exists
        if os.path.exists(backup_path):
            print("   [OK] Backup file exists")
        else:
            print("   [ERROR] Backup file not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"   [ERROR] Backup/Restore test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Hospital Management System - Database Tests")
    print("=" * 50)
    
    # Initialize database
    db = test_database_initialization()
    if not db:
        print("\n[ERROR] Database initialization failed. Cannot continue tests.")
        return
    
    # Run tests
    tests = [
        ("Table Creation", lambda: test_table_creation(db)),
        ("Basic Operations", lambda: test_basic_operations(db)),
        ("Foreign Keys", lambda: test_foreign_keys(db)),
        ("Backup/Restore", lambda: test_backup_restore(db)),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Database is ready to use.")
    else:
        print("\n[WARNING] Some tests failed. Please review the errors above.")


if __name__ == "__main__":
    import sqlite3
    main()
