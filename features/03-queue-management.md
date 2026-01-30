# Feature 3: Enhanced Queue Management

## Overview
Enhance the queue management system from the POC to provide real-time queue visualization, advanced priority management, and comprehensive queue analytics.

## Current State (POC)
- Basic queue with priority-based sorting (status: 0, 1, 2)
- Fixed capacity per specialization
- Simple add/remove operations
- No real-time visualization

## Target State
- Real-time queue visualization
- Advanced priority management
- Queue analytics and reporting
- Wait time estimation
- Queue notifications
- Multi-queue management

## Requirements

### Functional Requirements

#### 3.1 Queue Operations
- **Add Patient to Queue**:
  - Select specialization
  - Select patient (or create new)
  - Set priority/status
  - Validate capacity
  - Auto-sort by priority

- **Remove Patient from Queue**:
  - Remove by patient selection
  - Remove next patient (for doctor)
  - Remove with reason tracking

- **Queue Reordering**:
  - Manual priority adjustment
  - Emergency priority override
  - Automatic sorting on status change

#### 3.2 Queue Visualization
- **Real-time Queue Display**:
  - List view of all patients in queue
  - Priority indicators (color-coded)
  - Position in queue
  - Estimated wait time
  - Time in queue

- **Queue Status Indicators**:
  - Current queue size
  - Capacity utilization
  - Average wait time
  - Longest wait time

#### 3.3 Priority Management
- **Priority Levels**:
  - Normal (0) - Green
  - Urgent (1) - Yellow
  - Super-Urgent (2) - Red
  - Emergency (3) - Red flashing (optional)

- **Priority Rules**:
  - Higher priority always first
  - Same priority: FIFO (First In First Out)
  - Emergency cases can jump queue

#### 3.4 Queue Analytics
- **Statistics**:
  - Average wait time per specialization
  - Peak hours analysis
  - Queue length trends
  - Patient throughput
  - Priority distribution

- **Reports**:
  - Daily queue report
  - Weekly queue summary
  - Specialization comparison

## Technical Implementation

### Database Schema

```sql
CREATE TABLE queue_entries (
    queue_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    specialization_id INTEGER NOT NULL,
    status INTEGER DEFAULT 0 CHECK(status IN (0, 1, 2, 3)),
    position INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    served_at TIMESTAMP,
    removed_at TIMESTAMP,
    removal_reason TEXT,
    estimated_wait_time INTEGER, -- in minutes
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id)
);

CREATE INDEX idx_queue_specialization ON queue_entries(specialization_id);
CREATE INDEX idx_queue_status ON queue_entries(status);
CREATE INDEX idx_queue_joined ON queue_entries(joined_at);
```

### Class Structure

```python
class QueueEntry:
    def __init__(self, queue_entry_id, patient_id, specialization_id, status, ...):
        self.queue_entry_id = queue_entry_id
        self.patient_id = patient_id
        self.specialization_id = specialization_id
        self.status = status
        self.joined_at = joined_at
    
    @property
    def wait_time(self):
        # Calculate time in queue
        pass
    
    @property
    def estimated_wait_time(self):
        # Estimate based on queue position and average service time
        pass
```

### Service Layer

```python
class QueueService:
    def add_patient_to_queue(self, patient_id, specialization_id, status):
        # Add patient to queue with validation
        pass
    
    def remove_patient_from_queue(self, queue_entry_id, reason=None):
        # Remove patient from queue
        pass
    
    def get_next_patient(self, specialization_id):
        # Get and remove next patient (highest priority)
        pass
    
    def get_queue(self, specialization_id):
        # Get all patients in queue, sorted by priority
        pass
    
    def update_patient_priority(self, queue_entry_id, new_status):
        # Update patient priority and reorder queue
        pass
    
    def reorder_queue(self, specialization_id, new_order):
        # Manually reorder queue (admin function)
        pass
    
    def calculate_wait_time(self, queue_entry_id):
        # Calculate estimated wait time
        pass
    
    def get_queue_statistics(self, specialization_id, date_range=None):
        # Get queue statistics
        pass
```

### UI Components

1. **Queue Dashboard**
   - Overview of all specializations
   - Queue status indicators
   - Quick statistics

2. **Queue View (Per Specialization)**
   - Real-time patient list
   - Priority color coding
   - Position numbers
   - Wait time display
   - Action buttons

3. **Add to Queue Dialog**
   - Patient selection/search
   - Specialization selection
   - Priority selection
   - Capacity warning

4. **Queue Analytics View**
   - Charts and graphs
   - Statistics tables
   - Time-based analysis
   - Export options

5. **Queue Management Panel**
   - Reorder controls
   - Priority adjustment
   - Bulk operations

## Implementation Steps

1. **Database Setup**
   - Create queue_entries table
   - Set up indexes
   - Create triggers for auto-positioning

2. **Model Implementation**
   - Create QueueEntry model
   - Add wait time calculations
   - Add priority management

3. **Service Layer**
   - Implement QueueService
   - Add queue operations
   - Implement sorting logic
   - Add statistics calculations

4. **UI Components**
   - Design queue dashboard
   - Create queue view widget
   - Build analytics view
   - Implement real-time updates

5. **Real-time Updates**
   - Implement queue refresh mechanism
   - Add notifications for queue changes
   - Update wait time estimates

6. **Testing**
   - Unit tests for queue operations
   - Test priority sorting
   - Test capacity limits
   - Integration tests

## Acceptance Criteria

- [ ] Can add patient to queue with validation
- [ ] Queue automatically sorts by priority
- [ ] Can remove patient from queue
- [ ] Can get next patient (highest priority)
- [ ] Queue view updates in real-time
- [ ] Wait time estimates are calculated
- [ ] Capacity limits are enforced
- [ ] Priority can be updated
- [ ] Queue statistics are accurate
- [ ] UI is responsive and intuitive

## Dependencies

- Patient Management (Feature 1)
- Specialization Management (Feature 2)
- Database setup (Feature 8)

## Estimated Effort

- Database design: 3 hours
- Model implementation: 4 hours
- Service layer: 8 hours
- UI components: 14 hours
- Real-time updates: 4 hours
- Testing: 4 hours
- **Total: 37 hours**

## Notes

- Consider implementing queue notifications
- Add sound alerts for high-priority patients
- Implement queue history tracking
- Consider multi-queue support (e.g., walk-in vs appointment)
- Add queue export functionality
