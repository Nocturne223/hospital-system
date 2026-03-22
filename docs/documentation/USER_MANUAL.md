# Hospital Management System — User Manual

This manual describes the **Streamlit web application** (`app.py`). It focuses on **where to click**, **what to type or select**, and **the order of controls** on each screen.

---

## 1. Audience and purpose

The system is for **hospital staff** who manage patients, departments (specializations), queues, doctors, appointments, and reports.

---

## 2. Prerequisites and startup

- **Python 3**, dependencies from `requirements.txt`, database configured in **`src/config.py`** (MySQL via XAMPP or SQLite).

**Start the app** (project folder = folder containing `app.py`):

   ```bash
python -m streamlit run app.py
```

Or on Windows: run **`run_streamlit.bat`**.

If the database fails, the main area shows **Database Connection Failed** and troubleshooting text; the sidebar navigation does not load normal content until this is fixed.

---

## 3. How the interface behaves (Streamlit)

- The **left sidebar** is fixed: branding, **Navigation** buttons, **System status**, **Quick Stats**.
- The **main area** (right) shows the page for the current navigation choice.
- After many **button** clicks, the app **reruns** the page; forms and tables refresh. If something “jumps,” scroll back to the section you were using.
- **Tables** that support actions use a **Select** column (checkbox). Select **one** row, then use the **action buttons above the table** (not below), unless the on-screen instructions say otherwise.

---

## 4. Sidebar: global navigation (always visible)

Read the sidebar **from top to bottom**.

| Step | What you see | What to do |
|------|----------------|------------|
| 1 | Title area: **Hospital Management** / **Management System** | (Information only) |
| 2 | **Navigation** heading | — |
| 3 | Six **navigation buttons** (full width) | **Click one** to switch the main page. Only one page is active at a time; the active button is styled as the primary button. |

**Navigation button labels (click exactly these):**

| Button label | Opens |
|--------------|--------|
| **📊 Dashboard** | Reports & analytics |
| **👥 Patient Management** | Patients |
| **🏥 Specialization Management** | Specializations / departments |
| **📋 Queue Management** | Waiting queues |
| **👨‍⚕️ Doctor Management** | Doctors |
| **📅 Appointments** | Appointments |

Below the buttons:

| Element | Meaning |
|---------|---------|
| **System status** | Shows **Connected** when the database initialized successfully. |
| **📈 Quick Stats** | Metrics: **Patients**, **Doctors**, **Appointments**, **Queue** (two columns of numbers). |

---

## 5. General pattern: lists + Select checkbox + actions

On **Patient**, **Specialization**, **Doctor**, and **Appointment** pages:

1. **Statistics** and sometimes **search/filter** appear **at the top**.
2. **Action buttons** (Add / Edit / Delete / etc.) are in a **row below** the search row.
3. A horizontal rule (`---`) separates that from **forms** (Add/Edit/Delete) when they are open.
4. The **table** is **below** the forms area.

**Selecting a row**

1. Scroll to the subheading **… List - Click the checkbox in a row to select it** (wording is similar on each module).
2. In the table, tick **Select** on **one** row.
3. A green success line appears: **Selected: … — Click Edit/Delete button above to proceed** (wording varies slightly).
4. Click the desired action button **above** the table (e.g. **✏️ Edit Patient**).

---

## 6. Dashboard — click-by-click

**Open:** In the sidebar, click **📊 Dashboard**.

**Main area (top to bottom):**

1. **Title:** **📊 Dashboard**
2. **📈 Reports & Analytics Summary** — five metrics in one row: **Total Patients**, **Total Doctors**, **Active Queue**, **Total Appointments**, **Upcoming**.
3. **📋 Select Report Types (Select multiple to view all at once)** — **multiselect** dropdown. Click to add/remove report types. Options: **Patient Statistics**, **Queue Analytics**, **Appointment Reports**, **Doctor Performance**, **Specialization Utilization**, **Custom Report**. Default selection in code: **Patient Statistics** and **Appointment Reports**.
4. **Date range (two columns):**
   - **📅 Start Date** — date picker  
   - **📅 End Date** — date picker  
5. Below that, **each selected report type** renders its own blocks (metrics, subheadings, **bar charts**). Scroll to see all.
6. **Custom Report** only: after selecting **Custom Report** in the multiselect, scroll to **🔧 Custom Report Builder**:
   - **📊 Select Metrics** — multiselect: **Patient Statistics**, **Queue Statistics**, **Appointment Statistics**, **Doctor Statistics**, **Specialization Statistics**
   - Click **🔍 Generate Custom Report** (primary button) to build the combined view below.

**No separate Save** — changing dates or report selections updates what is shown on the next rerun.

---

## 7. Patient Management — navigation and controls

**Open:** Sidebar → **👥 Patient Management**.

### 7.1 Top of page (top to bottom)

1. **Title:** **👥 Patient Management**
2. **📊 Patient Statistics** — metrics: **Total Patients**, **Normal**, **Urgent**, **Super-Urgent**
3. **Row 1 (columns):**
   - **🔍 Search Patients** — text field; placeholder text: `Search by name, phone, or email...`
   - **Filter by Status** — dropdown: **All**, **Normal**, **Urgent**, **Super-Urgent**
   - **🔄 Refresh** — button (reloads)
4. **Row 2 (three buttons):**
   - **➕ Add New Patient** (primary)
   - **✏️ Edit Patient**
   - **🗑️ Delete Patient**
5. If you opened Add/Edit/Delete, the corresponding **form block** appears **next** (see below).
6. **📋 Patient List - Click the checkbox in a row to select it** — table with columns **Select**, **ID**, **Name**, **Age**, **Gender**, **Status**, **Phone**, **Email**

### 7.2 Add a new patient (procedure)

1. Click **➕ Add New Patient**.
2. Find the **➕ Add New Patient** subheading and the form below it.
3. Fill inputs:

   **Left column**

   - **Full Name** (required; the label in the app ends with an asterisk) — text  
   - **Date of Birth** (required) — date picker (cannot be after today)  
   - **Gender** — dropdown: empty, **Male**, **Female**, **Other**  
   - **Phone Number** — text  

   **Right column**

   - **Email** — text  
   - **Address** — multiline  
   - **Status** — dropdown: **Normal**, **Urgent**, **Super-Urgent** (triage / priority in this app)

4. Click **💾 Save Patient** to submit, or **❌ Cancel** to close without saving.
5. If required fields are empty, the form shows **Full Name and Date of Birth are required!**

### 7.3 Edit a patient (procedure)

**Option A — from table**

1. In **Patient List**, check **Select** on one row.
2. Click **✏️ Edit Patient** above the table.
3. You should see **📝 Editing Patient ID: …** and the form **Edit Patient** with fields pre-filled: **Full Name**, **Date of Birth**, **Gender**, **Phone Number**, **Email**, **Address**, **Status** (required fields match the add form).
4. Click **💾 Update Patient** or **❌ Cancel**.

**Option B — by ID**

1. Click **✏️ Edit Patient** without selecting a row.
2. Use **Enter Patient ID to Edit (or select a row from the table above)** — number stepper (minimum 1).
3. Click **Load Patient**.
4. After **Patient loaded!**, use the same form as Option A.

### 7.4 Delete a patient (procedure)

1. Select a row in **Patient List** (or open delete and use ID path similar to edit).
2. Click **🗑️ Delete Patient**.
3. On **🗑️ Delete Patient**, read the warning and patient summary.
4. Click **✅ Confirm Delete** or **❌ Cancel**.

---

## 8. Specialization Management — navigation and controls

**Open:** Sidebar → **🏥 Specialization Management**.

### 8.1 Top of page (top to bottom)

1. **Title:** **🏥 Specialization Management**
2. **📊 Specialization Statistics** — **Total Specializations**, **Active**, **Inactive**, **Total Capacity**
3. **Row 1:** **🔍 Search Specializations** (placeholder *Search by name or description...*) | **🔄 Refresh**
4. **Row 2 (four controls):**
   - **➕ Add New Specialization** (primary)
   - **✏️ Edit Specialization**
   - **🗑️ Delete Specialization**
   - **Filter** — dropdown: **All**, **Active Only**, **Inactive Only**
5. Add/Edit/Delete blocks when open.
6. **📋 Specialization List - Click the checkbox in a row to select it** — table: **Select**, **ID**, **Name**, **Max Capacity**, **Current Queue**, **Utilization**, **Doctors**, **Status**

### 8.2 Add specialization (procedure)

1. Click **➕ Add New Specialization**.
2. Under **➕ Add New Specialization**:
   - **Specialization Name** (required) — text  
   - **Description** — multiline  
   - **Maximum Queue Capacity** (required) — number (1–1000, default 10)  
   - **Active** — checkbox (default on)  
3. **💾 Save Specialization** or **❌ Cancel**.

### 8.3 Edit specialization (procedure)

1. Select one row in the list, then **✏️ Edit Specialization**, **or** enter ID and **Load Specialization**.
2. Form fields: **Specialization Name**, **Description**, **Maximum Queue Capacity**, **Active** (required fields show an asterisk in the app).
3. **💾 Update Specialization** or **❌ Cancel**.

### 8.4 Delete specialization (procedure)

1. Select a row, then **🗑️ Delete Specialization**.
2. Read **Are you sure…** and **✅ Yes, Delete** / **❌ Cancel**.  
   Success message may say the item was **deactivated** depending on backend rules.

---

## 9. Queue Management — navigation and controls

**Open:** Sidebar → **📋 Queue Management**.

### 9.1 Top of page (top to bottom)

1. **Title:** **📋 Queue Management**
2. **📊 Queue Statistics** — **Total Active**, **Normal**, **Urgent**, **Super-Urgent**, **Avg Wait Time**
3. **🏥 Select Specialization** — dropdown:
   - First option: **📋 All Specializations** (combined view)
   - Then each active department, e.g. **Cardiology (ID: 1)**
4. **Row of four buttons:**
   - **➕ Add to Queue** (primary) — **requires a specific specialization** (not “All”); otherwise a **⚠️ Please select a specific specialization…** warning appears
   - **✅ Serve Next Patient** — also **requires a specific specialization**
   - **🔄 Refresh Queue**
   - **📊 View Analytics** — for **one** specialization; if **All** is selected, you may see a message to pick a specific department first

### 9.2 Add to queue (procedure)

1. In **🏥 Select Specialization**, choose a **named** department (not **All**).
2. Click **➕ Add to Queue**.
3. Under **➕ Add Patient to Queue**:
   - Banner **Adding to: …** shows the department  
   - **👤 Select Patient** — dropdown of all patients  
   - **⚡ Priority Level** — **Normal (0)**, **Urgent (1)**, **Super-Urgent (2)**  
   - Metrics: **Current Queue Size** (e.g. `3/10`), **Capacity Usage** (%)  
4. **✅ Add to Queue** or **❌ Cancel**.  
   If full, you see **⚠️ Queue is at maximum capacity!** and add may fail with an error message.

### 9.3 Serve next (procedure)

1. Select a **specific** specialization.
2. Click **✅ Serve Next Patient**.  
   Success: **✅ Patient … has been served!** Empty queue: **📭 Queue is empty. No patients to serve.**

### 9.4 View analytics (procedure)

1. Select a **specific** specialization.
2. Click **📊 View Analytics**.
3. **📊 Queue Analytics** shows metrics and wait times.
4. Click **Close Analytics** to leave.

### 9.5 Queue table — row actions (procedure)

1. With **All Specializations** or one department selected, scroll to **📋 All Queues** or **📋 Current Queue**.
2. Tick **Select** on **one** row.
3. Three buttons appear **below** the selection area:
   - **⚡ Change Priority** → **⚡ Change Patient Priority**: **New Priority Level** dropdown, then **✅ Update Priority** or **❌ Cancel**
   - **✅ Serve Patient** — immediate serve for that entry  
   - **🗑️ Remove from Queue** → **🗑️ Remove Patient from Queue**: optional **Removal Reason (optional)**, then **✅ Yes, Remove** or **❌ Cancel**

---

## 10. Doctor Management — navigation and controls

**Open:** Sidebar → **👨‍⚕️ Doctor Management**.

### 10.1 Top of page (top to bottom)

1. **Title:** **👨‍⚕️ Doctor Management**
2. **📊 Doctor Statistics** — **Total Doctors**, **Active**, **Inactive**, **On Leave**
3. **🔍 Search Doctors** | **Filter by Status** (**All**, **Active**, **Inactive**, **On Leave**) | **🔄 Refresh**
4. **➕ Add New Doctor** | **✏️ Edit Doctor** | **🗑️ Delete Doctor**
5. Forms when open.
6. **📋 Doctor List - Click the checkbox in a row to select it** — **Select**, **ID**, **Name**, **License**, **Status**, **Phone**, **Email**, **Experience**

### 10.2 Add doctor (procedure)

1. Click **➕ Add New Doctor**.
2. **Left column:** **Full Name** (required), **Title (e.g., Dr., Prof.)**, **License Number** (required), **Phone Number**, **Email**, **Office Address**  
3. **Right column:** **Medical Degree**, **Years of Experience** (0–100), **Certifications**, **Status** (**Active**, **Inactive**, **On Leave**), **Hire Date**, **Bio/Description**  
4. **Specializations** heading → **Select Specializations** — multiselect (only **active** specializations listed)  
5. **✅ Add Doctor** or **❌ Cancel**

### 10.3 Edit / Delete doctor

Same selection pattern as patients: select row → **✏️ Edit Doctor** or **🗑️ Delete Doctor**, or load by ID where offered.

- Edit form mirrors add fields; use **✅** submit / **❌ Cancel** as shown on screen.  
- Delete: confirmation notes **soft delete** → **Inactive**; **✅ Yes, Delete** / **❌ Cancel**.

---

## 11. Appointment Management — navigation and controls

**Open:** Sidebar → **📅 Appointments**.

### 11.1 Top of page (top to bottom)

1. **Title:** **📅 Appointment Management**
2. **📊 Appointment Statistics** — **Total**, **Scheduled**, **Confirmed**, **Upcoming**, **Today**, **Completed**, then **Cancelled**, **No-Show**
3. **🔍 Search Appointments** | **Filter by Status** | **Filter by Date** | **🔄 Refresh**  
   - **Filter by Status:** **All**, **Scheduled**, **Confirmed**, **Cancelled**, **Completed**, **No-Show**  
   - **Filter by Date:** **All**, **Today**, **Upcoming**, **Past**
4. **➕ Schedule New Appointment** | **✏️ Edit Appointment** | **✅ Mark Complete** | **❌ Cancel Appointment**
5. Forms when open.
6. **📋 Appointment List - Click the checkbox in a row to select it** — **Select**, **ID**, **Date**, **Time**, **Patient**, **Doctor**, **Specialization**, **Type**, **Status**, **Duration**

### 11.2 Schedule new appointment (procedure)

1. Click **➕ Schedule New Appointment**.
2. Under **➕ Schedule New Appointment**, fill the form:
   - **👤 Patient** (required) — dropdown  
   - **👨‍⚕️ Doctor** (required) — dropdown (active doctors)  
   - **🏥 Specialization** (required) — dropdown (active specializations)  
   - **📅 Appointment Date** (required) — not before today  
   - **🕐 Appointment Time** (required) — time picker  
   - **⏱️ Duration (minutes)** (required) — 15–240, step 15  
   - **📋 Appointment Type** (required) — **Regular**, **Follow-up**, **Emergency**  
   - **📝 Reason for Visit**, **📄 Additional Notes**  
   - **📊 Status** — **Scheduled** or **Confirmed**
3. Click **✅ Schedule Appointment** or **❌ Cancel**.
4. Overlap error example: **❌ Time slot conflicts with existing appointment(s). Please choose a different time.**

If dropdowns are empty, the form shows messages such as **No active patients**, **No active doctors**, or **No active specializations** (see §12).

### 11.3 Edit appointment (procedure)

1. Select **one** row in **Appointment List**.
2. Click **✏️ Edit Appointment**.
3. Same fields as schedule, plus **📊 Status** may include **Cancelled**, **Completed**, **No-Show**.
4. **✅ Update Appointment** or **❌ Cancel**.

### 11.4 Mark complete / Cancel (procedure)

1. Select one appointment row.
2. **✅ Mark Complete** → **✅ Mark Appointment as Complete** — optional **📝 Completion Notes (Optional)** → **✅ Mark as Complete** or **❌ Cancel**. If already completed, a warning and **❌ Close** appear.
3. **❌ Cancel Appointment** → **📝 Cancellation Reason** → **✅ Confirm Cancellation** or **❌ Cancel**.

---

## 12. Patient dropdown on appointments (important)

The **Schedule** and **Edit** appointment forms only list patients where the code filters **`patient.status == 1`**. In this project, **Patient.status** is **triage**: **0 = Normal**, **1 = Urgent**, **2 = Super-Urgent**.

So the **Patient** dropdown (required field) effectively shows **Urgent** patients only. To make a patient appear there, set **Status** to **Urgent** on **Patient Management**, or change the code to use all patients.

---

## 13. Quick troubleshooting

| Issue | Check |
|--------|--------|
| Cannot connect | MySQL/XAMPP, database name, `src/config.py` |
| Add to queue blocked | Capacity; duplicate patient in same department queue |
| No patients in appointment form | §12 — try **Urgent** status |
| Wrong row targeted | Exactly **one** **Select** checkbox ticked before Edit/Delete |

---

## 14. Reference paths

| Item | Location |
|------|----------|
| App entry | `app.py` |
| Configuration | `src/config.py` |
| Services | `src/services/` |

For service behavior details, see **API_DOCUMENTATION.md** in the same folder.
