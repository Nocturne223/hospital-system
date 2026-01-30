# Feature Flows and Processes — User Manual

This document explains **how each feature and module works** in the Hospital Management System from an end-user perspective: the flow of actions, what you see on screen, and how to complete common tasks. Use it as the “how they work” reference for the User Manual.

**Application:** Web-based interface (Streamlit).  
**How to run:** `python -m streamlit run app.py` (or use `run_streamlit.bat`).

---

## Table of Contents

1. [Application Entry and Navigation](#1-application-entry-and-navigation)
2. [Patient Management](#2-patient-management)
3. [Specialization Management](#3-specialization-management)
4. [Queue Management](#4-queue-management)
5. [Doctor Management](#5-doctor-management)
6. [Appointments](#6-appointments)
7. [Reports & Analytics](#7-reports--analytics)

---

## 1. Application Entry and Navigation

### Flow

1. **Start the application**  
   Run the app (e.g. from command line or `run_streamlit.bat`). The browser opens to the main page.

2. **Database connection**  
   - If the database connects successfully, the main content and sidebar appear.  
   - If connection fails, an error message appears with hints (e.g. check MySQL/XAMPP, database name, credentials in `src/config.py`). Fix the issue and refresh or restart.

3. **Sidebar**  
   - **Navigation:** Buttons for each module: Patient Management, Specialization Management, Queue Management, Doctor Management, Appointments, Reports & Analytics.  
   - **System status:** Shows “Connected” when the database is available.  
   - **Quick stats:** Totals for Patients, Doctors, Appointments, and Active Queue.

4. **Using a module**  
   Click a navigation button to open that module. The main area shows that module’s page (statistics, filters, actions, and data table or report).

---

## 2. Patient Management

**Purpose:** Register and maintain patient records (demographics, contact, and priority status).

### Page layout

- **Top:** Patient statistics (e.g. total patients, counts by status).  
- **Search and filter:** Search by name/phone/email; filter by status (All, Normal, Urgent, Super-Urgent).  
- **Actions:** Add New Patient, Edit Patient, Delete Patient, Refresh.  
- **Table:** List of patients with a **selection column** (checkbox). You must select one row to Edit or Delete.

### Process: Add a new patient

1. Click **➕ Add New Patient**.  
2. A form appears. Enter:  
   - **Required:** Full Name, Date of Birth.  
   - **Optional:** Gender, Phone, Email, Address, Status (Normal, Urgent, Super-Urgent).  
3. Click **💾 Save Patient** to create the record, or **❌ Cancel** to close without saving.  
4. On success, the table refreshes and the new patient appears.

### Process: Edit a patient

1. In the table, **select the patient** using the checkbox (one row).  
2. Click **✏️ Edit Patient**.  
3. If a row is selected, the form opens with that patient’s data loaded. If not, you may need to enter Patient ID and click **Load Patient**.  
4. Change any fields (name, DOB, gender, contact, address, status).  
5. Click **💾 Update Patient** to save, or **❌ Cancel** to discard.  
6. The table refreshes with updated data.

### Process: Delete a patient

1. In the table, **select the patient** using the checkbox.  
2. Click **🗑️ Delete Patient**.  
3. A confirmation section shows the patient’s details.  
4. Click **✅ Confirm Delete** to remove the record, or **❌ Cancel** to abort.  
5. The table refreshes; the patient is no longer listed.

### How it works (summary)

- **Search:** Filters the table by the text you type (name, phone, email).  
- **Status filter:** Limits the table to Normal, Urgent, or Super-Urgent (or All).  
- **Selection:** Only one patient can be selected at a time for Edit/Delete.  
- **Refresh:** Reloads the list and statistics from the database.

---

## 3. Specialization Management

**Purpose:** Create and maintain medical specializations and set the maximum queue capacity per specialization.

### Page layout

- **Top:** Specialization statistics (e.g. total, active, capacity).  
- **Search:** Search by name or description.  
- **Actions:** Add New Specialization, Edit Specialization, Delete Specialization, Refresh.  
- **Filter:** All, Active Only, or Inactive Only.  
- **Table:** List of specializations with a **selection column**. Select one row to Edit or Delete.

### Process: Add a new specialization

1. Click **➕ Add New Specialization**.  
2. In the form, enter:  
   - **Name** (required), e.g. Cardiology, Pediatrics.  
   - **Description** (optional).  
   - **Maximum Queue Capacity** (required): max number of patients that can be in the queue for this specialization (e.g. 10).  
   - **Active:** Checked = active, unchecked = inactive.  
3. Click **💾 Save Specialization** or **❌ Cancel**.  
4. The table refreshes; the new specialization appears.

### Process: Edit a specialization

1. **Select the specialization** in the table (checkbox).  
2. Click **✏️ Edit Specialization**.  
3. Load the record if needed (same pattern as Patient: selection or enter ID and **Load Specialization**).  
4. Change name, description, max capacity, or active status.  
5. Click **💾 Update Specialization** or **❌ Cancel**.  
6. Table refreshes.

### Process: Delete a specialization

1. **Select the specialization** in the table.  
2. Click **🗑️ Delete Specialization**.  
3. Confirm in the confirmation section (**✅ Yes, Delete** or **❌ Cancel**).  
4. Table refreshes; the specialization is removed.

### How it works (summary)

- **Capacity:** Each specialization has a max queue size. Queue Management will not allow adding more patients than this limit.  
- **Active/Inactive:** Inactive specializations typically do not appear in queue selection for adding patients.  
- **Search and filter:** Narrow the list by text and by Active/Inactive.

---

## 4. Queue Management

**Purpose:** Manage patient queues per specialization: add patients, set priority, serve the next patient, change priority, remove from queue, and view analytics.

### Page layout

- **Top:** Queue statistics (e.g. total active, counts by priority, average wait time).  
- **Specialization selector:** Dropdown: “All Specializations” or a specific specialization (e.g. Cardiology).  
- **Actions:** Add to Queue, Serve Next Patient, Refresh Queue, View Analytics.  
- **Table:**  
  - If **All Specializations** is selected: queues for all specializations.  
  - If one specialization is selected: queue for that specialization only.  
  - Each queue row can have actions: **Change Priority**, **Serve Patient**, **Remove from Queue**.

### Process: Add a patient to the queue

1. In **Select Specialization**, choose a **specific specialization** (not “All Specializations”).  
2. Click **➕ Add to Queue**.  
3. In the dialog:  
   - **Select Patient:** Choose from the list (ID and name).  
   - **Priority Level:** Normal, Urgent, or Super-Urgent.  
   - Current queue size and capacity are shown; if the queue is full, you cannot add.  
4. Click **✅ Add to Queue** or **❌ Cancel**.  
5. The queue table refreshes; the patient appears in the selected specialization’s queue.

### Process: Serve the next patient

1. Select a **specific specialization** in the dropdown.  
2. Click **✅ Serve Next Patient**.  
3. The system takes the **next patient in line** (by priority and order) and marks that queue entry as “served.”  
4. A message confirms who was served. The queue table refreshes.

### Process: Change priority / Serve / Remove (from table)

- **Change Priority:** Select the queue entry (or use the row’s button), then in the dialog choose the new priority (Normal, Urgent, Super-Urgent) and confirm.  
- **Serve Patient:** Marks that specific queue entry as served (same effect as “Serve Next” for that entry).  
- **Remove from Queue:** Removes the patient from the queue without marking as served (e.g. if they left).

### Process: View queue analytics

1. Select a **specific specialization** (optional; some analytics may apply to all).  
2. Click **📊 View Analytics**.  
3. A panel or dialog shows metrics (e.g. active count, wait times, priority distribution).  
4. Close the analytics view to return to the queue table.

### How it works (summary)

- **Priority:** Normal (0), Urgent (1), Super-Urgent (2). Higher priority is served first; within the same priority, order is typically by time added.  
- **Capacity:** You cannot add more patients than the specialization’s maximum queue capacity.  
- **All Specializations view:** Read-only overview of all queues; add/serve/analytics require selecting one specialization.

---

## 5. Doctor Management

**Purpose:** Register and maintain doctors and assign them to specializations.

### Page layout

- **Top:** Doctor statistics (e.g. total, by status).  
- **Search and filter:** Search by name/license; filter by status (All, Active, Inactive, On Leave).  
- **Actions:** Add New Doctor, Edit Doctor, Delete Doctor, Refresh.  
- **Table:** List of doctors with a **selection column**. Select one row to Edit or Delete.

### Process: Add a new doctor

1. Click **➕ Add New Doctor**.  
2. In the form, enter:  
   - **Full Name**, **License Number** (required).  
   - **Phone**, **Email**, **Status** (Active, Inactive, On Leave).  
   - **Specializations:** Select one or more specializations to assign.  
3. Click **✅ Add Doctor** or **❌ Cancel**.  
4. The table refreshes; the new doctor appears.

### Process: Edit a doctor

1. **Select the doctor** in the table (checkbox).  
2. Click **✏️ Edit Doctor**.  
3. Load the doctor if needed (by selection or by ID and **Load Doctor**).  
4. Update name, license, contact, status, or specialization assignments.  
5. Click **✅ Update Doctor** or **❌ Cancel**.  
6. Table refreshes.

### Process: Delete a doctor

1. **Select the doctor** in the table.  
2. Click **🗑️ Delete Doctor**.  
3. Confirm (**✅ Yes, Delete** or **❌ Cancel**).  
4. Table refreshes; the doctor is removed.

### How it works (summary)

- **Specializations:** A doctor can be linked to multiple specializations; this is used when scheduling appointments and in reports.  
- **Status:** Active, Inactive, On Leave; filter the table by status as needed.  
- **Selection:** One doctor at a time for Edit/Delete, same pattern as Patient and Specialization.

---

## 6. Appointments

**Purpose:** Schedule, update, complete, and cancel appointments; view and filter the appointment list.

### Page layout

- **Top:** Appointment statistics (e.g. total, by status, upcoming).  
- **Search and filter:** Search by patient/doctor/reason; filter by **Status** (All, Scheduled, Confirmed, Cancelled, Completed, No-Show) and **Date** (All, Today, Upcoming, Past).  
- **Actions:** Schedule New Appointment, Edit Appointment, Mark Complete, Cancel Appointment, Refresh.  
- **Table:** List of appointments with a **selection column**. Select one row for Edit, Mark Complete, or Cancel Appointment.

### Process: Schedule a new appointment

1. Click **➕ Schedule New Appointment**.  
2. In the form:  
   - **Patient:** Select from dropdown (required).  
   - **Doctor:** Select from dropdown (required).  
   - **Specialization:** Select (required).  
   - **Date and Time:** Appointment date and time.  
   - **Type:** Regular, Follow-up, or Emergency.  
   - **Status:** Scheduled or Confirmed.  
   - **Reason/Notes** (optional).  
3. Click **✅ Schedule Appointment** or **❌ Cancel**.  
4. The system checks for **conflicts** (same doctor, overlapping time). If there is a conflict, an error is shown and you must change time or doctor.  
5. On success, the table refreshes and the new appointment appears.

### Process: Edit an appointment

1. **Select the appointment** in the table (checkbox).  
2. Click **✏️ Edit Appointment**.  
3. Load the appointment if needed (by selection or ID).  
4. Change patient, doctor, specialization, date/time, type, status, or notes.  
5. Click **✅ Update Appointment** or **❌ Cancel**.  
6. Conflict checks apply; the table refreshes on success.

### Process: Mark appointment complete

1. **Select the appointment** in the table.  
2. Click **✅ Mark Complete**.  
3. In the confirmation, optionally add notes, then confirm **✅ Mark as Complete** or **❌ Cancel**.  
4. The appointment status becomes **Completed**; the table refreshes.

### Process: Cancel an appointment

1. **Select the appointment** in the table.  
2. Click **❌ Cancel Appointment**.  
3. Confirm **✅ Confirm Cancellation** or **❌ Cancel**.  
4. The appointment status becomes **Cancelled**; the table refreshes.

### How it works (summary)

- **Conflict detection:** The system prevents double-booking the same doctor at the same time.  
- **Statuses:** Scheduled → Confirmed → Completed (or Cancelled / No-Show). Mark Complete sets status to Completed.  
- **Filters:** Use status and date filters to focus on today, upcoming, or past appointments.  
- **Selection:** One appointment at a time for Edit, Mark Complete, or Cancel.

---

## 7. Reports & Analytics

**Purpose:** View dashboard summary and run reports on patients, queue, appointments, doctors, and specializations; build a custom report.

### Page layout

- **Top:** Dashboard summary (Total Patients, Total Doctors, Active Queue, Total Appointments, Upcoming).  
- **Report type:** Dropdown to choose one of: Patient Statistics, Queue Analytics, Appointment Reports, Doctor Performance, Specialization Utilization, Custom Report.  
- **Date range:** Start Date and End Date (used by most reports).  
- **Content area:** Shows the selected report (metrics, charts, tables).

### Process: View a standard report

1. Choose **Report Type** from the dropdown (e.g. Patient Statistics, Queue Analytics, Appointment Reports, Doctor Performance, Specialization Utilization).  
2. Set **Start Date** and **End Date** as needed.  
3. The report loads automatically and shows:  
   - **Patient Statistics:** Totals, new registrations, status/gender/age distributions, charts.  
   - **Queue Analytics:** Active queue, wait times, priority distribution, specialization breakdown.  
   - **Appointment Reports:** Counts by status/type, completion/cancellation rates, doctor workload.  
   - **Doctor Performance:** Appointments per doctor, completion rates, specialization assignments.  
   - **Specialization Utilization:** Queue utilization, capacity, appointments per specialization.  
4. Scroll to see all metrics and charts; no extra button is required to “generate” once the type and date range are set.

### Process: Custom report

1. Select **Custom Report** from the dropdown.  
2. Set **Start Date** and **End Date**.  
3. Select the **metrics** you want (e.g. patient stats, queue stats, appointment stats).  
4. Click **🔍 Generate Custom Report**.  
5. The system combines the selected metrics into one view (tables and charts).  
6. Adjust date range or metrics and generate again if needed.

### How it works (summary)

- **Dashboard summary:** Always visible at the top; same numbers as in the sidebar Quick Stats.  
- **Date range:** Most reports filter data by the chosen start and end date.  
- **Charts and tables:** Reports show bar charts and tables; no export button is required for basic use.  
- **Custom report:** Combines multiple metric types in a single view for ad-hoc analysis.

---

## Quick Reference: Common Patterns

| Action           | Typical flow                                                                 |
|-----------------|-------------------------------------------------------------------------------|
| **Add new item**| Click “Add…” → Fill form → Save or Cancel.                                   |
| **Edit item**   | Select one row (checkbox) → Click “Edit…” → Change fields → Update or Cancel.|
| **Delete item** | Select one row → Click “Delete…” → Confirm or Cancel.                        |
| **Refresh list**| Click **🔄 Refresh** to reload data and statistics.                          |
| **Use filters** | Use search box and/or dropdown filters; the table updates automatically.    |
| **Queue actions**| Select a specialization (not “All”) for Add/Serve/Analytics.               |
| **Appointments**| Select one appointment for Edit, Mark Complete, or Cancel.                   |

---

**Document:** Feature Flows and Processes (User Manual)  
**Location:** `docs/documentation/FEATURE_FLOWS_AND_PROCESSES.md`  
**Last updated:** January 30, 2026
