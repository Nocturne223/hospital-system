# How to Run the Hospital Management System

## 🚀 Quick Start - Run the Streamlit Web Application

### Step 1: Make sure MySQL is running
- Open XAMPP Control Panel
- Start MySQL service (should be green)

### Step 2: Run the Application

**Option 1: Using the launcher (Recommended)**
```bash
python run_app.py
```

**Option 2: Direct Streamlit command**
```bash
python -m streamlit run app.py
```

**Option 3: Using batch file (Windows)**
```bash
run_app.bat
```

**That's it!** The application will open in your web browser at `http://localhost:8501`

---

## 📱 What You'll See

### Web Application Features

1. **Sidebar Navigation**:
   - Patient Management (working)
   - Queue Management (coming soon)
   - Doctor Management (coming soon)
   - Appointments (coming soon)
   - Reports & Analytics (coming soon)

2. **Patient Management Page**:
   - **Search Bar**: Search patients by name, phone, or email
   - **Filter**: Filter by status (Normal/Urgent/Super-Urgent)
   - **Tabs**:
     - View Patients: Browse and search all patients
     - Add New Patient: Create new patient records
     - Edit Patient: Modify existing patient information
     - Delete Patient: Remove patient records
   - **Data Table**: Shows all patients with:
     - ID, Name, Age, Status, Phone, Email, Registration Date
   - **Statistics**: Real-time patient count by status

3. **Actions**:
   - **Search**: Type in search box to filter patients
   - **Filter**: Use dropdown to filter by status
   - **Add**: Fill form and click "Save Patient"
   - **Edit**: Enter Patient ID, load patient, modify, and save
   - **Delete**: Enter Patient ID and confirm deletion

---

## 🎯 How to Use the Interface

### View All Patients
1. Application opens showing all patients
2. Scroll through the table
3. Click "Refresh" to reload

### Search Patients
1. Type in the search box
2. Results update automatically
3. Clear search to see all patients

### Add New Patient
1. Go to "Add New Patient" tab
2. Fill in the form:
   - Full Name * (required)
   - Date of Birth * (required)
   - Gender (optional)
   - Phone Number (optional)
   - Email (optional)
   - Address (optional)
   - Status (Normal/Urgent/Super-Urgent)
3. Click "💾 Save Patient" button
4. Success message appears and patient is added to database
5. Switch to "View Patients" tab to see the new patient

### Edit Patient
1. Go to "Edit Patient" tab
2. Enter the Patient ID
3. Click "Load Patient" button
4. Modify information in the form
5. Click "💾 Update Patient" button
6. Success message appears and patient is updated

### Delete Patient
1. Go to "Delete Patient" tab
2. Enter the Patient ID
3. Click "🗑️ Delete Patient" button
4. Confirm deletion in the confirmation dialog
5. Patient is removed from database

---

## 🖥️ System Requirements

- ✅ Python 3.8+
- ✅ Streamlit installed (`python -m pip install streamlit`)
- ✅ MySQL running (XAMPP)
- ✅ Database `hospital_system` exists
- ✅ All dependencies: `python -m pip install -r requirements.txt`

---

## 🐛 Troubleshooting

### Application Won't Start

**Error**: "ModuleNotFoundError: No module named 'streamlit'"
```bash
python -m pip install streamlit
```

**Error**: "streamlit: command not found"
Use: `python -m streamlit run app.py` instead of `streamlit run app.py`

**Error**: "Can't connect to MySQL"
- Check XAMPP MySQL is running
- Verify database exists
- Check `src/config.py` for correct credentials

**Error**: "No patients shown"
- Run: `python src/database/add_sample_patients.py`
- Refresh the browser page

### Browser Doesn't Open
- Manually go to: `http://localhost:8501`
- Check if port 8501 is already in use
- Try: `python -m streamlit run app.py --server.port 8502`

---

## 📋 Quick Commands

```bash
# Run the Streamlit web application
python run_app.py
# OR
python -m streamlit run app.py

# Add sample data (if needed)
python src/database/add_sample_patients.py

# Test backend (without GUI)
python tests/test_patient_service.py

# Interactive console test
python interactive_test.py
```

---

## 🎨 Interface Preview

When you run the application, you'll see:

```
┌─────────────────────────────────────────────────────┐
│  Hospital Management System                          │
├─────────────────────────────────────────────────────┤
│ [Patient Management] [Queue] [Doctors] [Appts] ... │
├─────────────────────────────────────────────────────┤
│ Search: [________________] [Search]                 │
│ [Add] [Edit] [Delete] [Refresh]                     │
├─────────────────────────────────────────────────────┤
│ ID │ Name        │ Age │ Status      │ Phone │ ... │
├────┼─────────────┼─────┼─────────────┼───────┼─────┤
│ 1  │ John Doe    │ 36  │ Normal      │ 555-  │ ... │
│ 2  │ Jane Smith  │ 33  │ Urgent      │ 555-  │ ... │
│ 3  │ Bob Johnson │ 45  │ Normal      │ 555-  │ ... │
└─────────────────────────────────────────────────────┘
```

---

## ✨ Features Available

### ✅ Working Now
- View all patients
- Search patients
- Add new patient
- Edit patient
- Delete patient
- Real-time updates

### ⏳ Coming Soon
- Queue Management interface
- Doctor Management interface
- Appointment System interface
- Reports and Analytics
- Dashboard

---

## 💡 Tips

1. **Double-click** a row to quickly edit
2. **Search** updates as you type
3. **Refresh** to reload from database
4. **Status colors** (can be added later for visual feedback)

---

**Ready to run?** Just type: `python run_app.py`
