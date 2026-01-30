"""
Database Viewer Script
View database contents in a readable format.
"""

import sys
import os

# Add src directory to path
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from database import DatabaseManager


def print_table(db: DatabaseManager, table_name: str):
    """Print all rows from a table."""
    print(f"\n{'=' * 80}")
    print(f"TABLE: {table_name.upper()}")
    print('=' * 80)
    
    try:
        # Get table info
        table_info = db.get_table_info(table_name)
        if not table_info:
            print(f"Table '{table_name}' not found or empty.")
            return
        
        # Get column names
        columns = [col['name'] for col in table_info]
        
        # Get all rows
        rows = db.execute_query(f"SELECT * FROM {table_name}")
        
        if not rows:
            print(f"No data in table '{table_name}'.")
            return
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            col_widths[col] = max(len(col), 15)  # Minimum width 15
        
        # Adjust widths based on data
        for row in rows:
            row_dict = dict(row)
            for col in columns:
                value = str(row_dict.get(col, '')) if row_dict.get(col) is not None else 'NULL'
                col_widths[col] = max(col_widths[col], len(value), 15)
        
        # Print header
        header = " | ".join([col.ljust(col_widths[col]) for col in columns])
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in rows:
            row_dict = dict(row)
            values = []
            for col in columns:
                value = str(row_dict.get(col, '')) if row_dict.get(col) is not None else 'NULL'
                # Truncate long values
                if len(value) > col_widths[col]:
                    value = value[:col_widths[col]-3] + "..."
                values.append(value.ljust(col_widths[col]))
            print(" | ".join(values))
        
        print(f"\nTotal rows: {len(rows)}")
        
    except Exception as e:
        print(f"Error reading table '{table_name}': {e}")


def print_table_summary(db: DatabaseManager):
    """Print summary of all tables."""
    print("\n" + "=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)
    
    tables = [
        'patients', 'doctors', 'specializations', 'doctor_specializations',
        'queue_entries', 'appointments', 'users', 'audit_logs'
    ]
    
    print(f"\n{'Table Name':<30} {'Row Count':<15} {'Status'}")
    print("-" * 60)
    
    for table in tables:
        try:
            count = db.get_table_count(table)
            status = "OK" if db.table_exists(table) else "MISSING"
            print(f"{table:<30} {count:<15} {status}")
        except Exception as e:
            print(f"{table:<30} {'ERROR':<15} {str(e)[:30]}")


def view_specific_table(db: DatabaseManager, table_name: str):
    """View a specific table."""
    if not db.table_exists(table_name):
        print(f"\n[ERROR] Table '{table_name}' does not exist.")
        print("\nAvailable tables:")
        tables = [
            'patients', 'doctors', 'specializations', 'doctor_specializations',
            'queue_entries', 'appointments', 'users', 'audit_logs'
        ]
        for table in tables:
            if db.table_exists(table):
                print(f"  - {table}")
        return
    
    print_table(db, table_name)


def view_all_tables(db: DatabaseManager):
    """View all tables."""
    tables = [
        'patients', 'doctors', 'specializations', 'doctor_specializations',
        'queue_entries', 'appointments', 'users', 'audit_logs'
    ]
    
    for table in tables:
        if db.table_exists(table):
            print_table(db, table)


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='View Hospital Management System Database')
    parser.add_argument(
        '--table', '-t',
        type=str,
        help='View specific table (patients, doctors, specializations, etc.)'
    )
    parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Show database summary only'
    )
    parser.add_argument(
        '--db-path',
        type=str,
        default='data/hospital_system.db',
        help='Path to database file (default: data/hospital_system.db)'
    )
    
    args = parser.parse_args()
    
    # Check if database exists
    if not os.path.exists(args.db_path):
        print(f"[ERROR] Database not found at: {args.db_path}")
        print("\nTo create the database, run:")
        print("  python src/database/init_db.py")
        return
    
    try:
        db = DatabaseManager(db_path=args.db_path)
        
        if args.summary:
            print_table_summary(db)
        elif args.table:
            view_specific_table(db, args.table)
        else:
            print_table_summary(db)
            print("\n" + "=" * 80)
            print("To view a specific table, use: python src/database/view_db.py --table <table_name>")
            print("Available tables: patients, doctors, specializations, queue_entries, appointments, users")
            print("=" * 80)
            
    except Exception as e:
        print(f"[ERROR] Failed to open database: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
