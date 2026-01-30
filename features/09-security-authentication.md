# Feature 9: Security & Authentication

## Overview
Implement user authentication, authorization, and security features to protect the Hospital Management System and ensure proper access control.

## Current State (POC)
- No authentication
- No user management
- No access control

## Target State
- User authentication system
- Role-based access control
- Password security
- Session management
- Audit logging

## Requirements

### Functional Requirements

#### 9.1 User Management
- **User Registration**:
  - Username (unique)
  - Email (unique)
  - Password (encrypted)
  - Full name
  - Role assignment
  - Status (Active/Inactive)

- **User Roles**:
  - Administrator (full access)
  - Doctor (patient/queue/appointment access)
  - Receptionist (patient/queue/appointment management)
  - Nurse (queue/patient viewing)
  - Viewer (read-only access)

#### 9.2 Authentication
- **Login System**:
  - Username/email and password login
  - Remember me option
  - Session management
  - Auto-logout after inactivity

- **Password Management**:
  - Password hashing (bcrypt/argon2)
  - Password strength requirements
  - Password reset functionality
  - Password change functionality

#### 9.3 Authorization
- **Role-Based Access Control (RBAC)**:
  - Permission system per role
  - Feature access based on role
  - Data access restrictions

- **Permissions**:
  - View patients
  - Create/edit patients
  - Delete patients
  - View doctors
  - Manage doctors
  - View queues
  - Manage queues
  - View appointments
  - Manage appointments
  - View reports
  - System administration

#### 9.4 Security Features
- **Data Protection**:
  - Encrypt sensitive data
  - Secure password storage
  - SQL injection prevention
  - Input validation and sanitization

- **Audit Logging**:
  - Log user actions
  - Log login attempts
  - Log data changes
  - Log access attempts

#### 9.5 Session Management
- **Session Control**:
  - Session timeout
  - Concurrent session limits
  - Session invalidation on logout
  - Secure session storage

## Technical Implementation

### Database Schema

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Administrator', 'Doctor', 'Receptionist', 'Nurse', 'Viewer')),
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id INTEGER,
    details TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
```

### Authentication Service

```python
# services/auth_service.py
import bcrypt
from datetime import datetime, timedelta
import secrets

class AuthService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.session_timeout = timedelta(hours=8)
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    
    def register_user(self, username: str, email: str, password: str, 
                     full_name: str, role: str) -> bool:
        """Register new user"""
        # Validate input
        # Check if username/email exists
        # Hash password
        # Insert into database
        pass
    
    def login(self, username: str, password: str) -> dict:
        """Authenticate user and create session"""
        # Get user from database
        # Verify password
        # Create session token
        # Update last_login
        # Return user info and token
        pass
    
    def logout(self, session_token: str):
        """Invalidate session"""
        pass
    
    def verify_session(self, session_token: str) -> dict:
        """Verify session token and return user info"""
        pass
    
    def change_password(self, user_id: int, old_password: str, 
                       new_password: str) -> bool:
        """Change user password"""
        pass
    
    def reset_password(self, email: str) -> bool:
        """Initiate password reset"""
        pass
```

### Authorization Service

```python
# services/authorization_service.py

class Permission:
    VIEW_PATIENTS = "view_patients"
    CREATE_PATIENTS = "create_patients"
    EDIT_PATIENTS = "edit_patients"
    DELETE_PATIENTS = "delete_patients"
    VIEW_DOCTORS = "view_doctors"
    MANAGE_DOCTORS = "manage_doctors"
    VIEW_QUEUES = "view_queues"
    MANAGE_QUEUES = "manage_queues"
    VIEW_APPOINTMENTS = "view_appointments"
    MANAGE_APPOINTMENTS = "manage_appointments"
    VIEW_REPORTS = "view_reports"
    SYSTEM_ADMIN = "system_admin"

class RolePermissions:
    PERMISSIONS = {
        'Administrator': [
            Permission.VIEW_PATIENTS,
            Permission.CREATE_PATIENTS,
            Permission.EDIT_PATIENTS,
            Permission.DELETE_PATIENTS,
            Permission.VIEW_DOCTORS,
            Permission.MANAGE_DOCTORS,
            Permission.VIEW_QUEUES,
            Permission.MANAGE_QUEUES,
            Permission.VIEW_APPOINTMENTS,
            Permission.MANAGE_APPOINTMENTS,
            Permission.VIEW_REPORTS,
            Permission.SYSTEM_ADMIN
        ],
        'Doctor': [
            Permission.VIEW_PATIENTS,
            Permission.VIEW_QUEUES,
            Permission.MANAGE_QUEUES,
            Permission.VIEW_APPOINTMENTS,
            Permission.MANAGE_APPOINTMENTS
        ],
        'Receptionist': [
            Permission.VIEW_PATIENTS,
            Permission.CREATE_PATIENTS,
            Permission.EDIT_PATIENTS,
            Permission.VIEW_QUEUES,
            Permission.MANAGE_QUEUES,
            Permission.VIEW_APPOINTMENTS,
            Permission.MANAGE_APPOINTMENTS
        ],
        'Nurse': [
            Permission.VIEW_PATIENTS,
            Permission.VIEW_QUEUES
        ],
        'Viewer': [
            Permission.VIEW_PATIENTS,
            Permission.VIEW_QUEUES,
            Permission.VIEW_APPOINTMENTS,
            Permission.VIEW_REPORTS
        ]
    }

class AuthorizationService:
    def __init__(self):
        self.role_permissions = RolePermissions.PERMISSIONS
    
    def has_permission(self, user_role: str, permission: str) -> bool:
        """Check if user role has permission"""
        return permission in self.role_permissions.get(user_role, [])
    
    def check_access(self, user, permission: str) -> bool:
        """Check if user has access to perform action"""
        if not user or user.status != 'Active':
            return False
        return self.has_permission(user.role, permission)
```

### Audit Logging

```python
# services/audit_service.py

class AuditService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def log_action(self, user_id: int, action: str, 
                  resource_type: str = None, resource_id: int = None,
                  details: str = None, ip_address: str = None):
        """Log user action"""
        query = """
            INSERT INTO audit_logs 
            (user_id, action, resource_type, resource_id, details, ip_address)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db_manager.execute_update(
            query, 
            (user_id, action, resource_type, resource_id, details, ip_address)
        )
    
    def get_audit_logs(self, user_id: int = None, 
                      start_date: datetime = None,
                      end_date: datetime = None):
        """Get audit logs with filters"""
        # Implementation
        pass
```

### UI Components

1. **Login Window**
   - Username/email input
   - Password input (masked)
   - Remember me checkbox
   - Login button
   - Error messages

2. **User Management**
   - User list view
   - Create user form
   - Edit user form
   - Role assignment
   - Status management

3. **Password Change Dialog**
   - Current password
   - New password
   - Confirm password
   - Validation feedback

4. **Permission Checks in UI**
   - Hide/show features based on permissions
   - Disable buttons for unauthorized actions
   - Show appropriate error messages

## Implementation Steps

1. **Database Setup**
   - Create users table
   - Create audit_logs table
   - Add indexes

2. **Authentication Service**
   - Implement password hashing
   - Implement login/logout
   - Implement session management

3. **Authorization Service**
   - Define permissions
   - Implement role-based access
   - Add permission checks

4. **Audit Logging**
   - Implement audit service
   - Add logging to key operations
   - Create audit log viewer

5. **UI Components**
   - Create login window
   - Add user management UI
   - Integrate permission checks
   - Add password change UI

6. **Security Hardening**
   - Input validation
   - SQL injection prevention
   - XSS prevention
   - Secure session storage

7. **Testing**
   - Test authentication
   - Test authorization
   - Test password security
   - Test audit logging

## Security Best Practices

1. **Password Security**
   - Minimum 8 characters
   - Require complexity (uppercase, lowercase, numbers)
   - Hash with bcrypt or argon2
   - Never store plain text passwords

2. **Session Security**
   - Use secure session tokens
   - Implement session timeout
   - Invalidate on logout
   - Prevent session fixation

3. **Input Validation**
   - Validate all user inputs
   - Sanitize data
   - Use parameterized queries
   - Prevent SQL injection

4. **Access Control**
   - Principle of least privilege
   - Check permissions on every action
   - Log access attempts
   - Monitor suspicious activity

## Acceptance Criteria

- [ ] Users can register with secure passwords
- [ ] Users can login with username/email and password
- [ ] Passwords are hashed and never stored in plain text
- [ ] Sessions are managed securely
- [ ] Role-based access control works correctly
- [ ] Permissions are enforced throughout application
- [ ] Audit logs record important actions
- [ ] Password reset functionality works
- [ ] Users can change their passwords
- [ ] Inactive users cannot login
- [ ] UI respects permission settings

## Dependencies

- Database setup (Feature 8: Data Management)

## Estimated Effort

- Database design: 2 hours
- Authentication service: 8 hours
- Authorization service: 6 hours
- Audit logging: 4 hours
- UI components: 10 hours
- Security hardening: 6 hours
- Testing: 4 hours
- **Total: 40 hours**

## Notes

- Consider two-factor authentication (future)
- Add password expiration policy
- Implement account lockout after failed attempts
- Add email verification for registration
- Consider OAuth integration (future)
- Add security settings configuration
- Implement data encryption at rest (optional)
