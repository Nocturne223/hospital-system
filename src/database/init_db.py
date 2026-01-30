"""
Database Initialization Script
Run this script to initialize or reset the database.
"""

import sys
import os

# Add src directory to path
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from database import DatabaseManager


def initialize_database(db_path: str = 'data/hospital_system.db'):
    """
    Initialize the database.
    
    Args:
        db_path: Path to the database file
    """
    print("=" * 60)
    print("Hospital Management System - Database Initialization")
    print("=" * 60)
    
    # Check if database exists
    if os.path.exists(db_path):
        response = input(
            f"\nDatabase already exists at {db_path}\n"
            "Do you want to recreate it? (This will DELETE all data!) [y/N]: "
        )
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return
        else:
            # Backup existing database
            print("\nCreating backup of existing database...")
            try:
                backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
                os.makedirs(backup_dir, exist_ok=True)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(
                    backup_dir,
                    f"hospital_system_backup_{timestamp}.db"
                )
                import shutil
                shutil.copy2(db_path, backup_path)
                print(f"✅ Backup created at: {backup_path}")
            except Exception as e:
                print(f"⚠️  Backup failed: {e}")
            
            # Remove existing database
            os.remove(db_path)
            print("✅ Existing database removed")
    
    try:
        print("\nInitializing database...")
        db = DatabaseManager(db_path=db_path)
        
        # Verify tables were created
        print("\nVerifying tables...")
        expected_tables = [
            'patients', 'doctors', 'specializations',
            'doctor_specializations', 'queue_entries',
            'appointments', 'users', 'audit_logs'
        ]
        
        all_created = True
        for table in expected_tables:
            if db.table_exists(table):
                count = db.get_table_count(table)
                print(f"  ✅ {table}: {count} rows")
            else:
                print(f"  ❌ {table}: NOT FOUND")
                all_created = False
        
        if all_created:
            print("\n" + "=" * 60)
            print("✅ Database initialized successfully!")
            print(f"   Database location: {os.path.abspath(db_path)}")
            print("=" * 60)
        else:
            print("\n⚠️  Some tables are missing. Please check the schema.")
            
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    initialize_database()
