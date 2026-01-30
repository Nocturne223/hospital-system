# Feature 8: Data Management & Persistence

## Overview
Implement robust data management system with database integration, data persistence, backup/restore functionality, and data export/import capabilities.

## Current State (POC)
- No data persistence
- All data in memory
- Data lost on application close

## Target State
- Full database integration
- Persistent data storage
- Backup and restore functionality
- Data export/import
- Database migrations
- Data integrity and validation

## Requirements

### Functional Requirements

#### 8.1 Database Design
- **Database Selection**:
  - SQLite for development (recommended)
  - PostgreSQL/MySQL for production (optional)

- **Schema Design**:
  - Normalized database structure
  - Proper relationships (foreign keys)
  - Indexes for performance
  - Constraints for data integrity

- **Tables Required**:
  - patients
  - doctors
  - specializations
  - doctor_specializations (junction)
  - queue_entries
  - appointments
  - appointment_reminders
  - users (for authentication)
  - audit_logs (optional)

#### 8.2 Data Persistence
- **CRUD Operations**:
  - Create operations save to database
  - Read operations fetch from database
  - Update operations modify database
  - Delete operations remove from database

- **Transaction Management**:
  - Atomic operations
  - Rollback on errors
  - Data consistency

#### 8.3 Database Management
- **Initialization**:
  - Database creation script
  - Schema initialization
  - Default data seeding

- **Migrations**:
  - Version control for schema
  - Migration scripts
  - Rollback capability

- **Maintenance**:
  - Database optimization
  - Index maintenance
  - Vacuum operations (SQLite)

#### 8.4 Backup & Restore
- **Backup Functionality**:
  - Manual backup
  - Scheduled backups (optional)
  - Full database backup
  - Incremental backup (optional)

- **Restore Functionality**:
  - Restore from backup file
  - Backup file validation
  - Restore confirmation

#### 8.5 Data Export/Import
- **Export Options**:
  - Export all data
  - Export by table
  - Export formats: SQL, CSV, JSON
  - Selective export

- **Import Options**:
  - Import from SQL file
  - Import from CSV
  - Import from JSON
  - Data validation on import

#### 8.6 Data Integrity
- **Validation**:
  - Foreign key constraints
  - Check constraints
  - Unique constraints
  - Not null constraints

- **Referential Integrity**:
  - Cascade deletes (where appropriate)
  - Prevent orphaned records
  - Maintain relationships

## Technical Implementation

### Database Manager

```python
# database/db_manager.py
import sqlite3
from contextlib import contextmanager
from typing import Optional

class DatabaseManager:
    def __init__(self, db_path: str = 'hospital_system.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Execute schema creation
            with open('database/schema.sql', 'r') as f:
                cursor.executescript(f.read())
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()):
        """Execute an update query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def backup_database(self, backup_path: str):
        """Create database backup"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
    
    def restore_database(self, backup_path: str):
        """Restore database from backup"""
        import shutil
        shutil.copy2(backup_path, self.db_path)
```

### Schema Definition

```sql
-- database/schema.sql

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
    phone_number TEXT,
    email TEXT,
    address TEXT,
    emergency_contact_name TEXT,
    emergency_contact_relationship TEXT,
    emergency_contact_phone TEXT,
    blood_type TEXT,
    allergies TEXT,
    medical_history TEXT,
    status INTEGER DEFAULT 0 CHECK(status IN (0, 1, 2)),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Specializations table
CREATE TABLE IF NOT EXISTS specializations (
    specialization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    max_capacity INTEGER DEFAULT 10 CHECK(max_capacity > 0),
    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    title TEXT,
    license_number TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    email TEXT,
    office_address TEXT,
    medical_degree TEXT,
    years_of_experience INTEGER,
    certifications TEXT,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'On Leave')),
    bio TEXT,
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctor-Specialization junction table
CREATE TABLE IF NOT EXISTS doctor_specializations (
    doctor_id INTEGER,
    specialization_id INTEGER,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (doctor_id, specialization_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
);

-- Queue entries table
CREATE TABLE IF NOT EXISTS queue_entries (
    queue_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    specialization_id INTEGER NOT NULL,
    status INTEGER DEFAULT 0 CHECK(status IN (0, 1, 2, 3)),
    position INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    served_at TIMESTAMP,
    removed_at TIMESTAMP,
    removal_reason TEXT,
    estimated_wait_time INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    specialization_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration INTEGER DEFAULT 30,
    appointment_type TEXT DEFAULT 'Regular' CHECK(appointment_type IN ('Regular', 'Follow-up', 'Emergency')),
    reason TEXT,
    notes TEXT,
    status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Confirmed', 'Cancelled', 'Completed', 'No-Show')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_patient_name ON patients(full_name);
CREATE INDEX IF NOT EXISTS idx_patient_phone ON patients(phone_number);
CREATE INDEX IF NOT EXISTS idx_patient_status ON patients(status);
CREATE INDEX IF NOT EXISTS idx_specialization_name ON specializations(name);
CREATE INDEX IF NOT EXISTS idx_doctor_name ON doctors(full_name);
CREATE INDEX IF NOT EXISTS idx_doctor_license ON doctors(license_number);
CREATE INDEX IF NOT EXISTS idx_queue_specialization ON queue_entries(specialization_id);
CREATE INDEX IF NOT EXISTS idx_queue_status ON queue_entries(status);
CREATE INDEX IF NOT EXISTS idx_appointment_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointment_doctor ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointment_patient ON appointments(patient_id);
```

### Export/Import Service

```python
# services/export_import_service.py
import json
import csv
import sqlite3
from datetime import datetime

class ExportImportService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def export_to_sql(self, output_path: str):
        """Export database to SQL file"""
        # Implementation
        pass
    
    def export_to_csv(self, table_name: str, output_path: str):
        """Export table to CSV"""
        # Implementation
        pass
    
    def export_to_json(self, output_path: str):
        """Export database to JSON"""
        # Implementation
        pass
    
    def import_from_sql(self, sql_file_path: str):
        """Import from SQL file"""
        # Implementation
        pass
    
    def import_from_csv(self, table_name: str, csv_file_path: str):
        """Import from CSV file"""
        # Implementation
        pass
```

## Implementation Steps

1. **Database Design**
   - Design schema
   - Define relationships
   - Plan indexes
   - Create constraints

2. **Database Manager**
   - Implement DatabaseManager class
   - Add connection management
   - Add query methods
   - Add transaction support

3. **Schema Implementation**
   - Create schema.sql
   - Add initialization script
   - Add default data seeding

4. **Service Integration**
   - Update all services to use database
   - Replace in-memory storage
   - Add error handling

5. **Backup/Restore**
   - Implement backup functionality
   - Implement restore functionality
   - Add UI for backup/restore

6. **Export/Import**
   - Implement export functionality
   - Implement import functionality
   - Add validation

7. **Testing**
   - Test database operations
   - Test backup/restore
   - Test export/import
   - Test data integrity

## Acceptance Criteria

- [ ] Database schema created correctly
- [ ] All tables have proper relationships
- [ ] Data persists across application restarts
- [ ] All CRUD operations work with database
- [ ] Backup functionality works
- [ ] Restore functionality works
- [ ] Export to SQL/CSV/JSON works
- [ ] Import from SQL/CSV works
- [ ] Data integrity maintained
- [ ] Performance is acceptable

## Dependencies

- None (foundational feature)

## Estimated Effort

- Database design: 6 hours
- Database manager: 8 hours
- Schema implementation: 4 hours
- Service integration: 10 hours
- Backup/restore: 4 hours
- Export/import: 6 hours
- Testing: 4 hours
- **Total: 42 hours**

## Notes

- Consider using SQLAlchemy ORM for better abstraction
- Implement connection pooling for better performance
- Add database versioning system
- Consider database encryption for sensitive data
- Add database health checks
- Implement query logging for debugging
