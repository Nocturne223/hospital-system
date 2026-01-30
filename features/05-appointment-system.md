# Feature 5: Appointment System

## Overview
Implement a comprehensive appointment scheduling system that allows patients to book appointments with doctors, view calendars, and manage appointment history.

## Current State (POC)
- No appointment system in POC
- Only walk-in queue management

## Target State
- Full appointment scheduling
- Calendar view for appointments
- Appointment reminders
- Appointment history tracking
- Conflict detection and resolution

## Requirements

### Functional Requirements

#### 5.1 Appointment Scheduling
- **Create Appointment**:
  - Select patient (existing or new)
  - Select doctor
  - Select specialization
  - Select date and time
  - Appointment type (Regular/Follow-up/Emergency)
  - Reason/Notes
  - Duration (default: 30 minutes, configurable)
  - Status (Scheduled/Confirmed/Cancelled/Completed)

- **Validation Rules**:
  - Doctor must be available at selected time
  - No overlapping appointments
  - Time must be in future
  - Within doctor's working hours
  - Respect break times

#### 5.2 Appointment Management
- **View Appointments**:
  - List view (all/upcoming/past)
  - Calendar view (daily/weekly/monthly)
  - Filter by doctor, patient, date range
  - Search functionality

- **Update Appointment**:
  - Reschedule appointment
  - Change doctor assignment
  - Update notes/reason
  - Change status

- **Cancel Appointment**:
  - Cancel with reason
  - Automatic notification
  - Free up time slot

#### 5.3 Appointment Calendar
- **Calendar Views**:
  - Daily view (time slots)
  - Weekly view (grid)
  - Monthly view (overview)
  - Doctor-specific calendar
  - Specialization calendar

- **Calendar Features**:
  - Color coding by status
  - Drag-and-drop rescheduling
  - Quick add appointment
  - Time slot indicators

#### 5.4 Appointment Reminders
- **Reminder Types**:
  - 24 hours before appointment
  - 2 hours before appointment
  - Same-day reminder

- **Reminder Methods**:
  - In-app notification
  - Email notification (future)
  - SMS notification (future)

#### 5.5 Appointment History
- Track all appointment activities
- View patient appointment history
- View doctor appointment history
- Appointment statistics

## Technical Implementation

### Database Schema

```sql
CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    specialization_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration INTEGER DEFAULT 30, -- in minutes
    appointment_type TEXT DEFAULT 'Regular' CHECK(appointment_type IN ('Regular', 'Follow-up', 'Emergency')),
    reason TEXT,
    notes TEXT,
    status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Confirmed', 'Cancelled', 'Completed', 'No-Show')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id)
);

CREATE TABLE appointment_reminders (
    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    reminder_type TEXT CHECK(reminder_type IN ('24h', '2h', 'same-day')),
    reminder_time TIMESTAMP,
    sent_at TIMESTAMP,
    is_sent INTEGER DEFAULT 0,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

CREATE INDEX idx_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_appointment_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointment_patient ON appointments(patient_id);
CREATE INDEX idx_appointment_status ON appointments(status);
```

### Class Structure

```python
class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, ...):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        # ... other attributes
    
    @property
    def end_time(self):
        # Calculate end time based on duration
        pass
    
    @property
    def is_upcoming(self):
        # Check if appointment is in future
        pass
    
    @property
    def is_conflict(self):
        # Check for scheduling conflicts
        pass
```

### Service Layer

```python
class AppointmentService:
    def create_appointment(self, appointment_data):
        # Create new appointment with validation
        pass
    
    def get_appointment(self, appointment_id):
        # Get appointment by ID
        pass
    
    def get_appointments(self, filters=None):
        # Get appointments with filters
        pass
    
    def update_appointment(self, appointment_id, appointment_data):
        # Update appointment
        pass
    
    def cancel_appointment(self, appointment_id, reason):
        # Cancel appointment
        pass
    
    def check_availability(self, doctor_id, date, time, duration):
        # Check if time slot is available
        pass
    
    def get_doctor_calendar(self, doctor_id, start_date, end_date):
        # Get doctor's appointments for date range
        pass
    
    def get_available_slots(self, doctor_id, date):
        # Get available time slots for doctor on date
        pass
    
    def schedule_reminders(self, appointment_id):
        # Schedule appointment reminders
        pass
```

### UI Components

1. **Appointment Form**
   - Patient selection
   - Doctor selection
   - Date/time picker
   - Duration selection
   - Notes input
   - Validation feedback

2. **Appointment List View**
   - Table with all appointments
   - Status indicators
   - Filter and search
   - Quick actions

3. **Calendar View**
   - Daily calendar with time slots
   - Weekly grid view
   - Monthly overview
   - Color coding
   - Drag-and-drop (if supported)

4. **Appointment Details View**
   - Full appointment information
   - Patient details
   - Doctor details
   - History timeline
   - Action buttons

5. **Availability Selector**
   - Show available time slots
   - Highlight conflicts
   - Quick booking

## Implementation Steps

1. **Database Setup**
   - Create appointments table
   - Create appointment_reminders table
   - Set up indexes and relationships

2. **Model Implementation**
   - Create Appointment model
   - Add validation methods
   - Add conflict detection logic

3. **Service Layer**
   - Implement AppointmentService
   - Add CRUD operations
   - Implement availability checking
   - Add reminder scheduling

4. **UI Components**
   - Design appointment form
   - Create calendar views
   - Build list view
   - Implement availability selector

5. **Integration**
   - Connect to patient management
   - Connect to doctor management
   - Connect to queue system

6. **Testing**
   - Unit tests for Appointment model
   - Unit tests for AppointmentService
   - Conflict detection tests
   - UI tests

## Acceptance Criteria

- [ ] Can create appointment with all required fields
- [ ] Appointment validation works correctly
- [ ] Conflict detection prevents overlapping appointments
- [ ] Can view appointments in list and calendar
- [ ] Can update appointment details
- [ ] Can cancel appointment
- [ ] Calendar displays correctly (daily/weekly/monthly)
- [ ] Available time slots are shown correctly
- [ ] Appointment reminders are scheduled
- [ ] Appointment history is tracked
- [ ] Data persists to database

## Dependencies

- Patient Management (Feature 1)
- Doctor Management (Feature 4)
- Specialization Management (Feature 2)
- Database setup (Feature 8)

## Estimated Effort

- Database design: 3 hours
- Model implementation: 5 hours
- Service layer: 10 hours
- UI components: 18 hours
- Calendar implementation: 8 hours
- Testing: 5 hours
- **Total: 49 hours**

## Notes

- Consider recurring appointments feature
- Add appointment waitlist
- Implement automatic appointment confirmation
- Add appointment rating/feedback
- Consider integration with external calendar systems
- Add appointment export (iCal format)
