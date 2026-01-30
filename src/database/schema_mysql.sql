-- Hospital Management System Database Schema
-- MySQL Database Schema
-- Version: 1.0
-- Date: 2026-01-30
-- Database: hospital_system

-- Use the database
USE hospital_system;

-- ============================================
-- PATIENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL,
    address TEXT DEFAULT NULL,
    emergency_contact_name VARCHAR(255) DEFAULT NULL,
    emergency_contact_relationship VARCHAR(50) DEFAULT NULL,
    emergency_contact_phone VARCHAR(20) DEFAULT NULL,
    blood_type VARCHAR(10) DEFAULT NULL,
    allergies TEXT DEFAULT NULL,
    medical_history TEXT DEFAULT NULL,
    status INT DEFAULT 0 CHECK(status IN (0, 1, 2)),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- SPECIALIZATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS specializations (
    specialization_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT DEFAULT NULL,
    max_capacity INT DEFAULT 10 CHECK(max_capacity > 0),
    is_active TINYINT(1) DEFAULT 1 CHECK(is_active IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- DOCTORS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(50) DEFAULT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    phone_number VARCHAR(20) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL,
    office_address TEXT DEFAULT NULL,
    medical_degree VARCHAR(255) DEFAULT NULL,
    years_of_experience INT DEFAULT NULL,
    certifications TEXT DEFAULT NULL,
    status ENUM('Active', 'Inactive', 'On Leave') DEFAULT 'Active',
    bio TEXT DEFAULT NULL,
    hire_date DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- DOCTOR-SPECIALIZATION JUNCTION TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS doctor_specializations (
    doctor_id INT NOT NULL,
    specialization_id INT NOT NULL,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (doctor_id, specialization_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- QUEUE ENTRIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS queue_entries (
    queue_entry_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    specialization_id INT NOT NULL,
    status INT DEFAULT 0 CHECK(status IN (0, 1, 2, 3)),
    -- Status: 0 = Normal, 1 = Urgent, 2 = Super-Urgent, 3 = Served
    position INT DEFAULT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    served_at TIMESTAMP NULL DEFAULT NULL,
    removed_at TIMESTAMP NULL DEFAULT NULL,
    removal_reason TEXT DEFAULT NULL,
    estimated_wait_time INT DEFAULT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- APPOINTMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    specialization_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration INT DEFAULT 30,
    appointment_type ENUM('Regular', 'Follow-up', 'Emergency') DEFAULT 'Regular',
    reason TEXT DEFAULT NULL,
    notes TEXT DEFAULT NULL,
    status ENUM('Scheduled', 'Confirmed', 'Cancelled', 'Completed', 'No-Show') DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP NULL DEFAULT NULL,
    cancellation_reason TEXT DEFAULT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- USERS TABLE (for authentication)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Administrator', 'Doctor', 'Receptionist', 'Nurse', 'Viewer') NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    is_active TINYINT(1) DEFAULT 1 CHECK(is_active IN (0, 1)),
    last_login TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
-- AUDIT LOGS TABLE (optional)
-- ============================================
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50) DEFAULT NULL,
    record_id INT DEFAULT NULL,
    old_values TEXT DEFAULT NULL,
    new_values TEXT DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
