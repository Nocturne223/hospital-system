-- Hospital Management System Database Schema
-- SQLite 3 Database Schema
-- Version: 1.0
-- Date: 2026-01-30

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================
-- PATIENTS TABLE
-- ============================================
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

-- ============================================
-- SPECIALIZATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS specializations (
    specialization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    max_capacity INTEGER DEFAULT 10 CHECK(max_capacity > 0),
    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- DOCTORS TABLE
-- ============================================
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

-- ============================================
-- DOCTOR-SPECIALIZATION JUNCTION TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS doctor_specializations (
    doctor_id INTEGER,
    specialization_id INTEGER,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (doctor_id, specialization_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
);

-- ============================================
-- QUEUE ENTRIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS queue_entries (
    queue_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    specialization_id INTEGER NOT NULL,
    status INTEGER DEFAULT 0 CHECK(status IN (0, 1, 2, 3)),
    -- Status: 0 = Normal, 1 = Urgent, 2 = Super-Urgent, 3 = Served
    position INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    served_at TIMESTAMP,
    removed_at TIMESTAMP,
    removal_reason TEXT,
    estimated_wait_time INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
);

-- ============================================
-- APPOINTMENTS TABLE
-- ============================================
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

-- ============================================
-- USERS TABLE (for authentication)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Administrator', 'Doctor', 'Receptionist', 'Nurse', 'Viewer')),
    full_name TEXT NOT NULL,
    email TEXT,
    phone_number TEXT,
    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AUDIT LOGS TABLE (optional)
-- ============================================
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    table_name TEXT,
    record_id INTEGER,
    old_values TEXT,
    new_values TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Patients indexes
CREATE INDEX IF NOT EXISTS idx_patient_name ON patients(full_name);
CREATE INDEX IF NOT EXISTS idx_patient_phone ON patients(phone_number);
CREATE INDEX IF NOT EXISTS idx_patient_status ON patients(status);
CREATE INDEX IF NOT EXISTS idx_patient_email ON patients(email);

-- Specializations indexes
CREATE INDEX IF NOT EXISTS idx_specialization_name ON specializations(name);
CREATE INDEX IF NOT EXISTS idx_specialization_active ON specializations(is_active);

-- Doctors indexes
CREATE INDEX IF NOT EXISTS idx_doctor_name ON doctors(full_name);
CREATE INDEX IF NOT EXISTS idx_doctor_license ON doctors(license_number);
CREATE INDEX IF NOT EXISTS idx_doctor_status ON doctors(status);

-- Queue entries indexes
CREATE INDEX IF NOT EXISTS idx_queue_specialization ON queue_entries(specialization_id);
CREATE INDEX IF NOT EXISTS idx_queue_status ON queue_entries(status);
CREATE INDEX IF NOT EXISTS idx_queue_patient ON queue_entries(patient_id);
CREATE INDEX IF NOT EXISTS idx_queue_joined_at ON queue_entries(joined_at);

-- Appointments indexes
CREATE INDEX IF NOT EXISTS idx_appointment_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointment_doctor ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointment_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointment_status ON appointments(status);

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_user_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_user_role ON users(role);

-- Audit logs indexes
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_table ON audit_logs(table_name);
