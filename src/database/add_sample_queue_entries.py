"""
Script to add sample queue entries to the database
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from services.queue_service import QueueService
from services.patient_service import PatientService
from services.specialization_service import SpecializationService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG


def add_sample_queue_entries():
    """Add sample queue entries to the database"""
    try:
        # Initialize database
        if USE_MYSQL:
            db_manager = DatabaseManager(  # type: ignore
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG['port'],
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password'],
                database=MYSQL_CONFIG['database']
            )
        else:
            db_manager = DatabaseManager(  # type: ignore
                db_path=SQLITE_CONFIG['db_path']
            )
        
        queue_service = QueueService(db_manager)
        patient_service = PatientService(db_manager)
        specialization_service = SpecializationService(db_manager)
        
        # Get all patients and specializations
        patients = patient_service.get_all_patients()
        specializations = specialization_service.get_all_specializations(active_only=True)
        
        if not patients:
            print("[ERROR] No patients found. Please add patients first.")
            return
        
        if not specializations:
            print("[ERROR] No active specializations found. Please add specializations first.")
            return
        
        print(f"[INFO] Found {len(patients)} patients and {len(specializations)} specializations")
        
        # Add queue entries - target at least 30 entries
        target_count = 30
        added_count = 0
        skipped_count = 0
        max_attempts = 200  # Prevent infinite loops
        
        # Shuffle patients and specializations for variety
        random.shuffle(patients)
        random.shuffle(specializations)
        
        # Track which patients have been used per specialization to avoid duplicates
        used_patients_per_spec = {spec.specialization_id: set() for spec in specializations}
        
        attempt = 0
        while added_count < target_count and attempt < max_attempts:
            attempt += 1
            
            # Cycle through specializations
            for spec in specializations:
                if added_count >= target_count:
                    break
                
                # Get current queue size
                current_queue = queue_service.get_queue(spec.specialization_id, active_only=True)
                current_size = len(current_queue)
                
                # Calculate how many we can add
                available_slots = spec.max_capacity - current_size
                if available_slots <= 0:
                    continue
                
                # Find patients not yet in this specialization's queue
                available_patients = [
                    p for p in patients 
                    if p.patient_id not in used_patients_per_spec[spec.specialization_id]
                ]
                
                if not available_patients:
                    # Reset for this specialization if we've used all patients
                    used_patients_per_spec[spec.specialization_id] = set()
                    available_patients = patients
                
                # Select a random patient
                patient = random.choice(available_patients)
                
                # Check if patient is already in this queue
                existing = queue_service.get_active_queue_entry(patient.patient_id, spec.specialization_id)
                if existing:
                    used_patients_per_spec[spec.specialization_id].add(patient.patient_id)
                    continue
                
                try:
                    # Random priority (weighted towards normal)
                    priority_weights = [0.5, 0.3, 0.2]  # Normal, Urgent, Super-Urgent
                    priority = random.choices([0, 1, 2], weights=priority_weights)[0]
                    
                    # Add to queue
                    queue_entry_id = queue_service.add_patient_to_queue(
                        patient.patient_id,
                        spec.specialization_id,
                        priority
                    )
                    
                    # Mark patient as used for this specialization
                    used_patients_per_spec[spec.specialization_id].add(patient.patient_id)
                    
                    # Simulate some patients joining at different times
                    # (This would normally be handled by the database, but we can update joined_at)
                    if random.random() < 0.4:  # 40% chance to have earlier join time
                        minutes_ago = random.randint(5, 45)
                        earlier_time = datetime.now() - timedelta(minutes=minutes_ago)
                        
                        query = "UPDATE queue_entries SET joined_at = %s WHERE queue_entry_id = %s"
                        db_manager.execute_update(query, (earlier_time, queue_entry_id))
                    
                    added_count += 1
                    priority_text = ['Normal', 'Urgent', 'Super-Urgent'][priority]
                    print(f"[OK] [{added_count}] Added {patient.full_name} to {spec.name} queue (Priority: {priority_text})")
                
                except ValueError as e:
                    # Patient already in queue or capacity exceeded
                    used_patients_per_spec[spec.specialization_id].add(patient.patient_id)
                    skipped_count += 1
                    # Only print if it's not a common "already in queue" error
                    if "already in" not in str(e).lower():
                        print(f"[WARNING] Skipped {patient.full_name} for {spec.name}: {str(e)}")
                    continue
                except Exception as e:
                    import traceback
                    error_msg = str(e) if str(e) else type(e).__name__
                    print(f"[ERROR] Error adding {patient.full_name} to {spec.name}: {error_msg}")
                    # Uncomment for debugging:
                    # traceback.print_exc()
                    skipped_count += 1
                    continue
        
        print("\n" + "="*50)
        print(f"[SUCCESS] Successfully added {added_count} queue entries")
        if skipped_count > 0:
            print(f"[WARNING] Skipped {skipped_count} entries (already in queue or capacity exceeded)")
        print("="*50)
    
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("[START] Adding sample queue entries...")
    print("="*50)
    add_sample_queue_entries()
