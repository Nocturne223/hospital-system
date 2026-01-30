# Hospital Management System - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [System Overview](#system-overview)
4. [Features Guide](#features-guide)
5. [Common Tasks](#common-tasks)
6. [Troubleshooting](#troubleshooting)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Glossary](#glossary)

---

## Introduction

### Welcome

Welcome to the Hospital Management System! This comprehensive system is designed to help hospital staff manage patients, doctors, specializations, queues, and appointments efficiently.

### What is This System?

The Hospital Management System is a desktop application that provides:
- **Patient Management**: Register and manage patient information
- **Queue Management**: Manage patient queues by specialization with priority-based ordering
- **Doctor Management**: Manage doctor profiles and assignments
- **Appointment Scheduling**: Schedule and manage patient appointments
- **Reporting**: Generate reports and analytics
- **User Management**: Role-based access control

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Display**: 1280x720 minimum resolution

---

## Getting Started

### Installation

1. **Download the Application**
   - Download the project files
   - Extract to your desired location

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   python src/database/init_db.py
   ```

4. **Run the Application**
   ```bash
   python src/main.py
   ```

### First Launch

1. **Login Screen**
   - Enter your username and password
   - Default administrator credentials (if applicable)
   - Click "Login"

2. **Dashboard**
   - You'll see the main dashboard
   - Overview of system statistics
   - Quick access to main features

### User Interface Overview

The application has a modern, intuitive interface with:
- **Menu Bar**: Access to all features
- **Toolbar**: Quick actions
- **Main Area**: Content display
- **Status Bar**: System status and notifications

---

## System Overview

### Main Components

#### 1. Dashboard
- System overview and statistics
- Quick access to common tasks
- Recent activity display

#### 2. Patient Management
- Register new patients
- View patient profiles
- Search and filter patients
- Update patient information

#### 3. Queue Management
- View queues by specialization
- Add patients to queues
- Process next patient
- Monitor queue status

#### 4. Doctor Management
- Register doctors
- Assign doctors to specializations
- Manage doctor schedules
- View doctor profiles

#### 5. Appointment System
- Schedule appointments
- View appointment calendar
- Manage appointments
- Appointment reminders

#### 6. Specialization Management
- Create specializations
- Set capacity limits
- Assign doctors
- View statistics

#### 7. Reporting
- Patient statistics
- Queue analytics
- Appointment reports
- System usage reports

---

## Features Guide

### Patient Management

#### Registering a New Patient

1. Navigate to **Patients** → **New Patient**
2. Fill in the required information:
   - Full Name (required)
   - Date of Birth (required)
   - Gender
   - Contact Information
   - Emergency Contact
   - Medical Information
3. Set patient status:
   - **Normal** (0): Regular patient
   - **Urgent** (1): Requires priority
   - **Super-Urgent** (2): Highest priority
4. Click **Save**

#### Searching for a Patient

1. Go to **Patients** → **Search**
2. Enter search criteria:
   - Patient ID
   - Name (partial match)
   - Phone number
   - Email
3. Click **Search**
4. Results display in a table

#### Viewing Patient Profile

1. Find the patient using search
2. Double-click the patient or click **View**
3. View complete patient information:
   - Personal details
   - Contact information
   - Medical history
   - Visit history
   - Queue history
   - Appointment history

#### Editing Patient Information

1. Open patient profile
2. Click **Edit**
3. Modify information
4. Click **Save**

#### Deleting a Patient

1. Select patient from list
2. Click **Delete**
3. Confirm deletion
4. **Note**: This action may be restricted based on user role

### Queue Management

#### Adding a Patient to Queue

1. Navigate to **Queue** → **Add to Queue**
2. Select **Specialization**
3. Select **Patient**
4. System automatically assigns priority based on patient status
5. Click **Add to Queue**

#### Viewing Queue Status

1. Go to **Queue** → **View Queues**
2. Select specialization
3. View queue list:
   - Patient name
   - Status (Normal/Urgent/Super-Urgent)
   - Position in queue
   - Estimated wait time

#### Processing Next Patient

1. Select specialization
2. Click **Next Patient**
3. System displays the highest priority patient
4. Patient is removed from queue
5. Record is saved to history

#### Removing a Patient from Queue

1. Find patient in queue
2. Click **Remove**
3. Enter removal reason (optional)
4. Confirm removal

### Doctor Management

#### Registering a Doctor

1. Navigate to **Doctors** → **New Doctor**
2. Fill in information:
   - Full Name (required)
   - License Number (required, unique)
   - Title/Qualifications
   - Contact Information
   - Medical Degree
   - Years of Experience
   - Certifications
3. Click **Save**

#### Assigning Doctor to Specialization

1. Open doctor profile
2. Go to **Specializations** tab
3. Click **Assign Specialization**
4. Select specialization
5. Click **Save**

### Appointment System

#### Scheduling an Appointment

1. Navigate to **Appointments** → **New Appointment**
2. Select:
   - Patient
   - Doctor
   - Specialization
   - Date and Time
   - Duration
   - Appointment Type
   - Reason
3. Click **Schedule**

#### Viewing Appointments

1. Go to **Appointments** → **Calendar**
2. Choose view:
   - **Day View**: Appointments for a specific day
   - **Week View**: Weekly calendar
   - **Month View**: Monthly calendar
3. Click on appointment to view details

#### Managing Appointments

- **Confirm**: Mark appointment as confirmed
- **Cancel**: Cancel appointment with reason
- **Reschedule**: Change date/time
- **Complete**: Mark as completed
- **No-Show**: Mark patient as no-show

### Specialization Management

#### Creating a Specialization

1. Navigate to **Specializations** → **New Specialization**
2. Enter:
   - Name (required, unique)
   - Description
   - Maximum Capacity
3. Click **Save**

#### Managing Specialization Capacity

1. Open specialization
2. View current queue count
3. Adjust maximum capacity if needed
4. System prevents adding patients when at capacity

---

## Common Tasks

### Daily Workflow

#### Morning Routine
1. Login to system
2. Check dashboard for updates
3. Review today's appointments
4. Check queue status

#### Adding a New Patient
1. Register patient
2. Add to appropriate queue
3. Confirm patient information

#### Processing Patients
1. View queue for specialization
2. Process next patient
3. Update patient status if needed

#### End of Day
1. Review completed appointments
2. Generate daily reports
3. Backup data (if authorized)

### Weekly Tasks

- Review weekly statistics
- Generate weekly reports
- Update doctor schedules
- Review queue analytics

---

## Troubleshooting

### Common Issues

#### Cannot Login
- **Problem**: Login fails
- **Solution**: 
  - Verify username and password
  - Check if account is active
  - Contact administrator

#### Patient Not Found
- **Problem**: Search returns no results
- **Solution**:
  - Check spelling
  - Try partial name search
  - Verify patient exists

#### Queue Full
- **Problem**: Cannot add patient to queue
- **Solution**:
  - Queue has reached maximum capacity
  - Process existing patients first
  - Contact administrator to increase capacity

#### Database Error
- **Problem**: Database connection error
- **Solution**:
  - Verify database file exists
  - Check file permissions
  - Restore from backup if needed
  - Contact technical support

#### Application Crashes
- **Problem**: Application closes unexpectedly
- **Solution**:
  - Save work frequently
  - Check error logs
  - Restart application
  - Report issue to support

### Getting Help

1. **Check FAQ**: See [FAQ.md](FAQ.md)
2. **Review Documentation**: Check relevant sections
3. **Contact Support**: Reach out to system administrator
4. **Report Bugs**: Use bug reporting system

---

## Keyboard Shortcuts

### General
- **Ctrl+N**: New record
- **Ctrl+S**: Save
- **Ctrl+F**: Search
- **Ctrl+Q**: Quit application
- **F1**: Help

### Navigation
- **Tab**: Next field
- **Shift+Tab**: Previous field
- **Enter**: Submit/Save
- **Esc**: Cancel/Close

### Patient Management
- **Ctrl+P**: New Patient
- **Ctrl+Shift+F**: Search Patients

### Queue Management
- **Ctrl+Q**: View Queues
- **Ctrl+N**: Next Patient

---

## Glossary

### Terms

- **Patient**: Individual receiving medical care
- **Queue**: Ordered list of patients waiting for service
- **Specialization**: Medical field (e.g., Cardiology, Pediatrics)
- **Status**: Patient priority level (Normal, Urgent, Super-Urgent)
- **Appointment**: Scheduled medical consultation
- **Capacity**: Maximum number of patients in a queue
- **Dashboard**: Main overview screen
- **Profile**: Complete information about a patient or doctor

### Status Levels

- **Normal (0)**: Standard priority patient
- **Urgent (1)**: Requires priority attention
- **Super-Urgent (2)**: Highest priority, immediate attention needed

### User Roles

- **Administrator**: Full system access
- **Doctor**: Access to patient records and appointments
- **Receptionist**: Patient and queue management
- **Nurse**: Patient care and queue management
- **Viewer**: Read-only access

---

## Conclusion

This user manual provides comprehensive guidance for using the Hospital Management System. For additional help:

- Review the [Feature Walkthrough](FEATURE_WALKTHROUGH.md)
- Check the [FAQ](FAQ.md)
- Contact system administrator

**Last Updated**: January 30, 2026  
**Version**: 1.0
