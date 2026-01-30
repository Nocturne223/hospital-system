"""
Add Sample Specializations to Database
This script adds sample specialization data for testing purposes.
Uses the SpecializationService for proper data handling.
"""

import sys
import os

# Get project root directory (two levels up from this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
src_dir = os.path.join(project_root, 'src')

# Add src to path
sys.path.insert(0, src_dir)

from database import DatabaseManager
from services.specialization_service import SpecializationService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def add_sample_specializations():
    """Add sample specializations to the database"""
    print("=" * 60)
    print("Adding Sample Specializations to Database")
    print("=" * 60)
    
    # Initialize
    if USE_MYSQL:
        db = DatabaseManager(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            database=MYSQL_CONFIG['database']
        )
    else:
        db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])
    
    service = SpecializationService(db)
    
    # Sample specializations data
    sample_specializations = [
        {
            'name': 'Cardiology',
            'description': 'Heart and cardiovascular system diseases and disorders',
            'max_capacity': 15,
            'is_active': True
        },
        {
            'name': 'Pediatrics',
            'description': 'Medical care for infants, children, and adolescents',
            'max_capacity': 20,
            'is_active': True
        },
        {
            'name': 'Orthopedics',
            'description': 'Bones, joints, ligaments, tendons, and muscles',
            'max_capacity': 12,
            'is_active': True
        },
        {
            'name': 'Neurology',
            'description': 'Brain, spinal cord, and nervous system disorders',
            'max_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Dermatology',
            'description': 'Skin, hair, and nail conditions',
            'max_capacity': 8,
            'is_active': True
        },
        {
            'name': 'Oncology',
            'description': 'Cancer diagnosis and treatment',
            'max_capacity': 10,
            'is_active': True
        },
        {
            'name': 'Emergency Medicine',
            'description': 'Acute medical care and trauma',
            'max_capacity': 25,
            'is_active': True
        },
        {
            'name': 'Internal Medicine',
            'description': 'Adult medicine and general health',
            'max_capacity': 18,
            'is_active': True
        }
    ]
    
    print(f"\nAdding {len(sample_specializations)} specializations...")
    
    added_count = 0
    skipped_count = 0
    
    for spec_data in sample_specializations:
        try:
            specialization_id = service.create_specialization(spec_data)
            print(f"  [OK] Added: {spec_data['name']} (ID: {specialization_id})")
            added_count += 1
        except ValueError as e:
            # Specialization already exists
            print(f"  [SKIP] Skipped: {spec_data['name']} - {str(e)}")
            skipped_count += 1
        except Exception as e:
            print(f"  [ERROR] Error adding {spec_data['name']}: {e}")
    
    print("\n" + "=" * 60)
    print(f"[SUMMARY]")
    print(f"  Added: {added_count}")
    print(f"  Skipped: {skipped_count}")
    print("=" * 60)
    
    # Show all specializations
    print("\nCurrent Specializations in Database:")
    all_specs = service.get_all_specializations(active_only=False)
    for spec in all_specs:
        stats = service.get_specialization_statistics(spec.specialization_id)
        status = "[ACTIVE]" if spec.is_active else "[INACTIVE]"
        print(f"  [{spec.specialization_id}] {spec.name} - {status}")
        print(f"      Capacity: {stats.get('current_queue_size', 0)}/{spec.max_capacity}")
        print(f"      Utilization: {stats.get('utilization_percentage', 0):.1f}%")
    
    print("\n[SUCCESS] Sample specializations added successfully!")
    print("\nYou can now:")
    print("  1. View in Streamlit: python -m streamlit run app.py")
    print("  2. View in database: python src/database/view_db.py --table specializations")


if __name__ == "__main__":
    add_sample_specializations()
