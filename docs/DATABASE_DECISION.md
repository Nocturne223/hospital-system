# Database Selection Decision

## Decision: SQLite for Development and Production

**Date**: January 28, 2026  
**Status**: Approved

## Rationale

### Selected: SQLite 3

**Why SQLite?**
1. **Zero Configuration**: No server setup required, works out of the box
2. **Built-in Python Support**: `sqlite3` module is part of Python standard library
3. **Single File Database**: Easy to backup, share, and version control
4. **Sufficient for Project Scope**: Handles all required features:
   - Foreign key constraints
   - Transactions
   - Indexes
   - Complex queries
   - Data integrity
5. **Perfect for Academic Project**: 
   - Easy to demonstrate
   - Simple deployment
   - No external dependencies
6. **Future-Proof**: Can migrate to PostgreSQL/MySQL later if needed

### Alternative Considered: PostgreSQL

**Why Not PostgreSQL?**
- Requires separate database server installation
- More complex setup and configuration
- Overkill for single-user/small-scale academic project
- Adds unnecessary complexity for development

**When to Use PostgreSQL:**
- Multi-user concurrent access (10+ simultaneous users)
- Very large datasets (millions of records)
- Production deployment with high traffic
- Need advanced features (full-text search, complex analytics)

## Database Specifications

### File Location
- **Development**: `data/hospital_system.db`
- **Backups**: `data/backups/`

### Features Used
- ✅ Foreign Key Constraints
- ✅ Transactions (ACID compliance)
- ✅ Indexes for performance
- ✅ Check Constraints
- ✅ Unique Constraints
- ✅ Timestamps (CURRENT_TIMESTAMP)

### Migration Path
If needed in the future, migration to PostgreSQL/MySQL is straightforward:
- SQLAlchemy ORM can abstract database differences
- Schema can be exported and adapted
- Data can be migrated using SQL dump

## Database Schema Overview

### Core Tables
1. **patients** - Patient information and profiles
2. **doctors** - Doctor information and credentials
3. **specializations** - Medical specializations
4. **doctor_specializations** - Many-to-many relationship
5. **queue_entries** - Queue management
6. **appointments** - Appointment scheduling
7. **users** - Authentication and authorization
8. **audit_logs** - System activity tracking (optional)

### Relationships
- Patients → Queue Entries (One-to-Many)
- Patients → Appointments (One-to-Many)
- Doctors → Appointments (One-to-Many)
- Doctors ↔ Specializations (Many-to-Many)
- Specializations → Queue Entries (One-to-Many)

## Implementation Notes

- Use connection context managers for proper resource management
- Enable foreign keys: `PRAGMA foreign_keys = ON;`
- Use transactions for multi-step operations
- Implement proper error handling and rollback
- Create indexes on frequently queried columns

## Backup Strategy

- Manual backup functionality
- Export to SQL file
- Export to CSV/JSON for data portability
- Regular backup reminders (optional)

---

**Decision Approved**: SQLite 3 for all development and production use.
