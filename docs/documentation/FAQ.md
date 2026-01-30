# Hospital Management System - Frequently Asked Questions (FAQ)

## Table of Contents

1. [General Questions](#general-questions)
2. [Installation and Setup](#installation-and-setup)
3. [Patient Management](#patient-management)
4. [Queue Management](#queue-management)
5. [Appointments](#appointments)
6. [Technical Issues](#technical-issues)
7. [Data Management](#data-management)
8. [User Accounts and Permissions](#user-accounts-and-permissions)

---

## General Questions

### Q: What is the Hospital Management System?
**A:** The Hospital Management System is a comprehensive desktop application designed to manage hospital operations including patient registration, queue management, doctor assignments, appointment scheduling, and reporting.

### Q: Who can use this system?
**A:** The system is designed for hospital staff including administrators, doctors, receptionists, and nurses. Each user role has appropriate access levels.

### Q: What operating systems are supported?
**A:** The system runs on Windows 10/11, macOS 10.14+, and Linux. It requires Python 3.8 or higher.

### Q: Is the system free to use?
**A:** This is an academic project. Usage terms depend on the project license and institutional policies.

### Q: Can I customize the system?
**A:** Yes, the system is open-source and can be customized. However, modifications should follow the project's coding standards and architecture.

---

## Installation and Setup

### Q: How do I install the system?
**A:** 
1. Ensure Python 3.8+ is installed
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database: `python src/database/init_db.py`
4. Run application: `python src/main.py`

### Q: What are the system requirements?
**A:**
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space
- 1280x720 minimum screen resolution

### Q: Do I need to install a database server?
**A:** No, the system uses SQLite which is file-based and requires no separate server installation.

### Q: How do I update the system?
**A:** 
1. Backup your database
2. Download latest version
3. Replace application files
4. Run database migrations if needed
5. Restore database backup

### Q: Can I use MySQL or PostgreSQL instead of SQLite?
**A:** Yes, the system can be configured to use MySQL or PostgreSQL. See the [XAMPP/Navicat Setup Guide](XAMPP_NAVICAT_SETUP.md) for details.

---

## Patient Management

### Q: How do I register a new patient?
**A:** Navigate to **Patients** → **New Patient**, fill in the required information (name and date of birth), and click **Save**. See the [User Manual](USER_MANUAL.md) for detailed steps.

### Q: What information is required for patient registration?
**A:** Minimum required fields are:
- Full Name
- Date of Birth

All other fields are optional but recommended for complete patient profiles.

### Q: Can I search for patients by partial name?
**A:** Yes, the search function supports partial name matching. Enter any part of the patient's name to find matches.

### Q: How do I update patient information?
**A:** 
1. Search for the patient
2. Open patient profile
3. Click **Edit**
4. Make changes
5. Click **Save**

### Q: Can I delete a patient?
**A:** Yes, but this action may be restricted based on user role. Deletion removes the patient and all associated records (queue entries, appointments). Use with caution.

### Q: What do patient status levels mean?
**A:**
- **Normal (0)**: Standard priority patient
- **Urgent (1)**: Requires priority attention
- **Super-Urgent (2)**: Highest priority, immediate attention needed

### Q: How does patient status affect queue position?
**A:** Patients are automatically sorted in queues by status priority:
1. Super-Urgent (highest)
2. Urgent (medium)
3. Normal (lowest)

---

## Queue Management

### Q: How do I add a patient to a queue?
**A:** 
1. Go to **Queue** → **Add to Queue**
2. Select specialization
3. Select patient
4. Click **Add to Queue**

### Q: What happens when a queue is full?
**A:** The system prevents adding new patients when the queue reaches maximum capacity. You must process existing patients first or increase the capacity limit.

### Q: How is queue order determined?
**A:** Queue order is based on:
1. Patient status (Super-Urgent > Urgent > Normal)
2. Time added to queue (within same status)

### Q: Can I manually reorder the queue?
**A:** Queue order is automatic based on priority. You can update patient status to change priority.

### Q: What happens when I process the next patient?
**A:** The system:
1. Displays the highest priority patient
2. Removes them from the queue
3. Records the service time
4. Updates queue positions

### Q: Can I remove a patient from the queue?
**A:** Yes, select the patient and click **Remove**. You can optionally enter a removal reason.

---

## Appointments

### Q: How do I schedule an appointment?
**A:** 
1. Go to **Appointments** → **New Appointment**
2. Select patient, doctor, and specialization
3. Choose date and time
4. Enter appointment details
5. Click **Schedule**

### Q: Can I schedule multiple appointments for the same patient?
**A:** Yes, a patient can have multiple appointments scheduled.

### Q: What if there's a scheduling conflict?
**A:** The system checks for conflicts and prevents double-booking. You'll receive a warning if a conflict is detected.

### Q: How do I cancel an appointment?
**A:** 
1. Find the appointment in the calendar
2. Open appointment details
3. Click **Cancel**
4. Enter cancellation reason
5. Confirm cancellation

### Q: Can I reschedule an appointment?
**A:** Yes, open the appointment and click **Reschedule**. Select a new date and time.

### Q: What appointment statuses are available?
**A:**
- **Scheduled**: Initial status
- **Confirmed**: Patient confirmed
- **Cancelled**: Appointment cancelled
- **Completed**: Appointment finished
- **No-Show**: Patient didn't arrive

---

## Technical Issues

### Q: The application won't start. What should I do?
**A:**
1. Verify Python 3.8+ is installed: `python --version`
2. Check dependencies are installed: `pip install -r requirements.txt`
3. Verify database exists: Check `data/hospital_system.db`
4. Check error messages in console
5. Review system logs

### Q: I'm getting a database error. How do I fix it?
**A:**
1. Verify database file exists at `data/hospital_system.db`
2. Check file permissions
3. Try restoring from backup
4. Reinitialize database if needed: `python src/database/init_db.py`
5. Contact technical support if issue persists

### Q: The application is running slowly. What can I do?
**A:**
1. Close other applications
2. Check available disk space
3. Optimize database: Run VACUUM command
4. Check for large data sets
5. Consider database maintenance

### Q: How do I backup my data?
**A:** 
1. Use the built-in backup feature: **Settings** → **Backup Database**
2. Or manually copy `data/hospital_system.db`
3. Backups are saved to `data/backups/`

### Q: How do I restore from a backup?
**A:**
1. Go to **Settings** → **Restore Database**
2. Select backup file
3. Confirm restoration
4. **Warning**: This will replace current database

### Q: Where are error logs stored?
**A:** Error logs are displayed in the console and may be saved to log files in the `logs/` directory (if configured).

---

## Data Management

### Q: Where is the data stored?
**A:** Data is stored in SQLite database file: `data/hospital_system.db`

### Q: Can I export data?
**A:** Yes, you can export data in various formats:
- **Reports**: Export to PDF, Excel, or CSV
- **Database**: Export to SQL file
- **Individual Tables**: Export to CSV

### Q: Can I import data from another system?
**A:** Yes, the system supports importing:
- CSV files (with proper format)
- SQL files
- JSON files (if supported)

### Q: How do I view the database directly?
**A:** You can use:
- Built-in database viewer: `python src/database/view_db.py`
- SQLite command line tool
- Database management tools (Navicat, DB Browser, etc.)

See [Viewing Database Guide](VIEWING_DATABASE.md) for details.

### Q: Is my data secure?
**A:** 
- Data is stored locally in SQLite database
- User passwords are hashed (not stored in plain text)
- Access is controlled through user roles
- Regular backups are recommended

### Q: Can I use the database with other tools?
**A:** Yes, SQLite databases can be opened with:
- DB Browser for SQLite
- Navicat
- SQLite command line
- VS Code extensions

---

## User Accounts and Permissions

### Q: How do I create a user account?
**A:** (Administrator only)
1. Go to **Users** → **New User**
2. Enter username and password
3. Select role
4. Set permissions
5. Click **Save**

### Q: What user roles are available?
**A:**
- **Administrator**: Full system access
- **Doctor**: Patient records and appointments
- **Receptionist**: Patient and queue management
- **Nurse**: Patient care and queue management
- **Viewer**: Read-only access

### Q: I forgot my password. What should I do?
**A:** Contact your system administrator to reset your password. Administrators can reset passwords through the user management interface.

### Q: Can I change my password?
**A:** Yes, go to **Settings** → **Change Password**. Enter current password and new password.

### Q: What permissions does each role have?
**A:**
- **Administrator**: All permissions
- **Doctor**: View/edit patients, view appointments, manage own schedule
- **Receptionist**: Register patients, manage queues, schedule appointments
- **Nurse**: View patients, manage queues, update patient status
- **Viewer**: View-only access to all features

### Q: Can I have multiple user accounts?
**A:** Yes, each user should have their own account. Sharing accounts is not recommended for security and audit purposes.

---

## Additional Questions

### Q: Where can I get more help?
**A:**
- Review the [User Manual](USER_MANUAL.md)
- Check the [Feature Walkthrough](FEATURE_WALKTHROUGH.md)
- Contact your system administrator
- Review technical documentation

### Q: How do I report a bug?
**A:** 
1. Document the issue:
   - What you were doing
   - What happened
   - Error messages
   - Steps to reproduce
2. Contact technical support
3. Include screenshots if possible

### Q: Can I suggest new features?
**A:** Yes, feature suggestions are welcome. Contact the development team or submit through the project repository.

### Q: Is there training available?
**A:** Training materials are available in the documentation. Contact your administrator for additional training sessions.

### Q: How often is the system updated?
**A:** Update frequency depends on the development schedule. Check the project repository for latest versions and release notes.

---

## Troubleshooting Quick Reference

| Problem | Quick Solution |
|---------|----------------|
| Can't login | Check username/password, verify account is active |
| Patient not found | Try partial name search, check spelling |
| Queue full | Process existing patients or increase capacity |
| Database error | Verify database file exists, check permissions |
| Application crashes | Restart application, check error logs |
| Slow performance | Close other apps, optimize database, check disk space |
| Can't save data | Check required fields, verify permissions |
| Search not working | Try different search terms, check filters |

---

## Contact Information

For additional support:
- **System Administrator**: Contact your local administrator
- **Technical Support**: See project repository
- **Documentation**: Review all documentation files in `docs/` directory

---

**Last Updated**: January 30, 2026  
**Version**: 1.0

*This FAQ is regularly updated. Check back for new questions and answers.*
