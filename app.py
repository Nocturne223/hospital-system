"""
Hospital Management System - Streamlit Application
Main entry point for the web-based GUI
"""

import streamlit as st
import sys
import os
from datetime import date, datetime, timedelta, time

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(project_root, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import backend components
from database import DatabaseManager
from services.patient_service import PatientService
from services.specialization_service import SpecializationService
from services.queue_service import QueueService
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from services.report_service import ReportService
from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG

# Page configuration
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = None
if 'patient_service' not in st.session_state:
    st.session_state.patient_service = None
if 'specialization_service' not in st.session_state:
    st.session_state.specialization_service = None
if 'queue_service' not in st.session_state:
    st.session_state.queue_service = None
if 'doctor_service' not in st.session_state:
    st.session_state.doctor_service = None
if 'appointment_service' not in st.session_state:
    st.session_state.appointment_service = None
if 'report_service' not in st.session_state:
    st.session_state.report_service = None
if 'db_error' not in st.session_state:
    st.session_state.db_error = None


def init_database():
    """Initialize database connection"""
    if st.session_state.db_manager is None:
        try:
            if USE_MYSQL:
                st.session_state.db_manager = DatabaseManager(  # type: ignore
                    host=MYSQL_CONFIG['host'],
                    port=MYSQL_CONFIG['port'],
                    user=MYSQL_CONFIG['user'],
                    password=MYSQL_CONFIG['password'],
                    database=MYSQL_CONFIG['database']
                )
            else:
                st.session_state.db_manager = DatabaseManager(  # type: ignore
                    db_path=SQLITE_CONFIG['db_path']
                )
            
            st.session_state.patient_service = PatientService(st.session_state.db_manager)
            st.session_state.specialization_service = SpecializationService(st.session_state.db_manager)
            st.session_state.queue_service = QueueService(st.session_state.db_manager)
            st.session_state.doctor_service = DoctorService(st.session_state.db_manager)
            st.session_state.appointment_service = AppointmentService(st.session_state.db_manager)
            st.session_state.report_service = ReportService(st.session_state.db_manager)
            st.session_state.db_error = None
            return True
        except Exception as e:
            st.session_state.db_error = str(e)
            return False
    return True


def main():
    """Main application"""
    # Initialize database
    if not init_database():
        st.error("❌ **Database Connection Failed**")
        st.error(f"Error: {st.session_state.db_error}")
        st.info("""
        **Please check:**
        1. XAMPP MySQL is running (if using MySQL)
        2. Database 'hospital_system' exists
        3. Credentials in `src/config.py` are correct
        """)
        st.stop()
    
    # Sidebar navigation with modern button design
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 15px 0; border-bottom: 2px solid #e0e0e0; margin-bottom: 20px;'>
        <h1 style='margin: 0; font-size: 26px; color: #1f77b4;'>🏥 Hospital Management</h1>
        <p style='margin: 5px 0; color: #666; font-size: 13px;'>Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu items (Dashboard first, then other features)
    nav_items = [
        ("📊", "Dashboard"),
        ("👥", "Patient Management"),
        ("🏥", "Specialization Management"),
        ("📋", "Queue Management"),
        ("👨‍⚕️", "Doctor Management"),
        ("📅", "Appointments")
    ]
    
    # Get current page from session state or default to Reports & Analytics (Dashboard)
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    # Create navigation buttons
    st.sidebar.markdown("### 🧭 Navigation")
    st.sidebar.markdown("")
    
    # Check if any navigation button was clicked
    page = st.session_state.current_page
    
    for icon, page_name in nav_items:
        # Determine button style based on current page
        button_type = "primary" if page_name == st.session_state.current_page else "secondary"
        
        if st.sidebar.button(
            f"{icon} {page_name}",
            use_container_width=True,
            type=button_type,
            key=f"nav_{page_name}"
        ):
            st.session_state.current_page = page_name
            st.rerun()
    
    # Use the current page from session state
    page = st.session_state.current_page
    
    st.sidebar.markdown("---")
    
    # System status
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                padding: 12px; border-radius: 8px; margin: 15px 0; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <p style='margin: 0; text-align: center; font-size: 14px;'>
            <strong style='color: #1b5e20;'>System Status</strong><br>
            <span style='color: #2e7d32; font-weight: bold; font-size: 16px;'>✅ Connected</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats in sidebar
    try:
        report_service = st.session_state.report_service
        dashboard_summary = report_service.get_dashboard_summary()
        
        st.sidebar.markdown("### 📈 Quick Stats")
        
        # Use columns for better layout
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Patients", dashboard_summary['total_patients'], delta=None)
            st.metric("Doctors", dashboard_summary['total_doctors'], delta=None)
        with col2:
            st.metric("Appointments", dashboard_summary['total_appointments'], delta=None)
            st.metric("Queue", dashboard_summary['active_queue'], delta=None)
    except:
        pass
    
    # Main content area
    if page == "Dashboard":
        show_reports_analytics()
    elif page == "Patient Management":
        show_patient_management()
    elif page == "Specialization Management":
        show_specialization_management()
    elif page == "Queue Management":
        show_queue_management()
    elif page == "Doctor Management":
        show_doctor_management()
    elif page == "Appointments":
        show_appointment_management()


def show_patient_management():
    """Patient Management page"""
    st.title("👥 Patient Management")
    st.markdown("---")
    
    service = st.session_state.patient_service
    
    # Display statistics at the top (always visible)
    display_patient_statistics(service)
    
    st.markdown("---")
    
    # Search and filter section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search Patients",
            placeholder="Search by name, phone, or email...",
            key="patient_search"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Normal", "Urgent", "Super-Urgent"],
            key="status_filter"
        )
    
    with col3:
        st.write("")  # Spacing
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Patient", use_container_width=True, type="primary"):
            st.session_state.show_add_patient = True
            st.rerun()
    
    with col2:
        if st.button("✏️ Edit Patient", use_container_width=True):
            # Check if patient is selected
            if 'selected_patient_id' in st.session_state and st.session_state.selected_patient_id:
                st.session_state.edit_patient_id = st.session_state.selected_patient_id
            st.session_state.show_edit_patient = True
            st.rerun()
    
    with col3:
        if st.button("🗑️ Delete Patient", use_container_width=True):
            # Check if patient is selected
            if 'selected_patient_id' in st.session_state and st.session_state.selected_patient_id:
                st.session_state.delete_patient_id = st.session_state.selected_patient_id
            st.session_state.show_delete_patient = True
            st.rerun()
    
    st.markdown("---")
    
    # Handle modals/dialogs
    if st.session_state.get('show_add_patient', False):
        show_add_patient_dialog(service)
    
    if st.session_state.get('show_edit_patient', False):
        show_edit_patient_dialog(service)
    
    if st.session_state.get('show_delete_patient', False):
        show_delete_patient_dialog(service)
    
    # Display patients table
    display_patients_table(service, search_query, status_filter)


def show_add_patient_dialog(service: PatientService):
    """Show add patient form"""
    st.subheader("➕ Add New Patient")
    
    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="Enter full name")
            date_of_birth = st.date_input(
                "Date of Birth *",
                value=date.today().replace(year=date.today().year - 30),
                max_value=date.today()
            )
            gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
            phone_number = st.text_input("Phone Number", placeholder="555-1234")
        
        with col2:
            email = st.text_input("Email", placeholder="email@example.com")
            address = st.text_area("Address", height=100)
            status = st.selectbox(
                "Status",
                ["Normal", "Urgent", "Super-Urgent"],
                index=0
            )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("💾 Save Patient", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            if not full_name or not date_of_birth:
                st.error("Full Name and Date of Birth are required!")
            else:
                try:
                    patient_data = {
                        'full_name': full_name,
                        'date_of_birth': date_of_birth.isoformat(),
                        'gender': gender if gender else None,
                        'phone_number': phone_number if phone_number else None,
                        'email': email if email else None,
                        'address': address if address else None,
                        'status': ["Normal", "Urgent", "Super-Urgent"].index(status)
                    }
                    
                    patient_id = service.create_patient(patient_data)
                    st.success(f"✅ Patient added successfully! (ID: {patient_id})")
                    st.session_state.show_add_patient = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to add patient: {e}")
        
        if cancel:
            st.session_state.show_add_patient = False
            st.rerun()
    
    st.markdown("---")


def show_edit_patient_dialog(service: PatientService):
    """Show edit patient form"""
    st.subheader("✏️ Edit Patient")
    
    # Get patient ID from selection (priority) or manual input
    selected_id = st.session_state.get('selected_patient_id')
    
    if selected_id:
        # Auto-load selected patient
        patient_id = selected_id
        st.info(f"📝 Editing Patient ID: {selected_id} (selected from table)")
        try:
            patient = service.get_patient(patient_id)
            if patient:
                st.session_state.edit_patient_data = patient.to_dict()
                st.session_state.patient_loaded = True
            else:
                st.error("❌ Patient not found!")
                st.session_state.patient_loaded = False
        except Exception as e:
            st.error(f"❌ Error loading patient: {e}")
            st.session_state.patient_loaded = False
    else:
        # Manual ID entry if no selection
        patient_id = st.number_input(
            "Enter Patient ID to Edit (or select a row from the table above)",
            min_value=1,
            step=1,
            value=st.session_state.get('edit_patient_id', 1),
            key="edit_patient_id_input"
        )
        
        if st.button("Load Patient", use_container_width=True):
            try:
                patient = service.get_patient(patient_id)
                if patient:
                    st.session_state.edit_patient_data = patient.to_dict()
                    st.session_state.patient_loaded = True
                    st.success("✅ Patient loaded!")
                else:
                    st.error("❌ Patient not found!")
                    st.session_state.patient_loaded = False
            except Exception as e:
                st.error(f"❌ Error loading patient: {e}")
                st.session_state.patient_loaded = False
    
    if st.session_state.get('patient_loaded', False) and st.session_state.get('edit_patient_data'):
        patient_data = st.session_state.edit_patient_data
        
        with st.form("edit_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input(
                    "Full Name *",
                    value=patient_data.get('full_name', ''),
                    key="edit_name"
                )
                # Parse date of birth safely
                dob_value = date.today()
                if patient_data.get('date_of_birth'):
                    try:
                        if isinstance(patient_data['date_of_birth'], str):
                            dob_value = datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d').date()
                        else:
                            dob_value = patient_data['date_of_birth']
                    except:
                        dob_value = date.today()
                
                date_of_birth = st.date_input(
                    "Date of Birth *",
                    value=dob_value,
                    max_value=date.today(),
                    key="edit_dob"
                )
                
                # Gender selectbox
                gender_options = ["", "Male", "Female", "Other"]
                gender_index = 0
                if patient_data.get('gender'):
                    try:
                        gender_index = gender_options.index(patient_data.get('gender'))
                    except:
                        gender_index = 0
                
                gender = st.selectbox(
                    "Gender",
                    gender_options,
                    index=gender_index,
                    key="edit_gender"
                )
                phone_number = st.text_input(
                    "Phone Number",
                    value=patient_data.get('phone_number', ''),
                    key="edit_phone"
                )
            
            with col2:
                email = st.text_input(
                    "Email",
                    value=patient_data.get('email', ''),
                    key="edit_email"
                )
                address = st.text_area(
                    "Address",
                    value=patient_data.get('address', ''),
                    height=100,
                    key="edit_address"
                )
                status = st.selectbox(
                    "Status",
                    ["Normal", "Urgent", "Super-Urgent"],
                    index=patient_data.get('status', 0),
                    key="edit_status"
                )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submit = st.form_submit_button("💾 Update Patient", use_container_width=True, type="primary")
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if not full_name or not date_of_birth:
                    st.error("Full Name and Date of Birth are required!")
                else:
                    try:
                        update_data = {
                            'full_name': full_name,
                            'date_of_birth': date_of_birth.isoformat(),
                            'gender': gender if gender else None,
                            'phone_number': phone_number if phone_number else None,
                            'email': email if email else None,
                            'address': address if address else None,
                            'status': ["Normal", "Urgent", "Super-Urgent"].index(status)
                        }
                        
                        service.update_patient(patient_id, update_data)
                        st.success(f"✅ Patient updated successfully!")
                        st.session_state.show_edit_patient = False
                        st.session_state.patient_loaded = False
                        st.session_state.edit_patient_data = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to update patient: {e}")
            
            if cancel:
                st.session_state.show_edit_patient = False
                st.session_state.patient_loaded = False
                st.session_state.edit_patient_data = None
                st.rerun()
    
    st.markdown("---")


def show_delete_patient_dialog(service: PatientService):
    """Show delete patient confirmation"""
    st.subheader("🗑️ Delete Patient")
    
    # Get patient ID from selection (priority) or manual input
    selected_id = st.session_state.get('selected_patient_id')
    
    if selected_id:
        # Auto-load selected patient
        patient_id = selected_id
        st.info(f"🗑️ Deleting Patient ID: {selected_id} (selected from table)")
        try:
            patient = service.get_patient(patient_id)
            if patient:
                st.session_state.delete_patient_data = patient.to_dict()
                st.session_state.delete_patient_loaded = True
            else:
                st.error("❌ Patient not found!")
                st.session_state.delete_patient_loaded = False
        except Exception as e:
            st.error(f"❌ Error loading patient: {e}")
            st.session_state.delete_patient_loaded = False
    else:
        # Manual ID entry if no selection
        patient_id = st.number_input(
            "Enter Patient ID to Delete (or select a row from the table above)",
            min_value=1,
            step=1,
            value=st.session_state.get('delete_patient_id', 1),
            key="delete_patient_id_input"
        )
        
        if st.button("Load Patient", use_container_width=True):
            try:
                patient = service.get_patient(patient_id)
                if patient:
                    st.session_state.delete_patient_data = patient.to_dict()
                    st.session_state.delete_patient_loaded = True
                else:
                    st.error("❌ Patient not found!")
                    st.session_state.delete_patient_loaded = False
            except Exception as e:
                st.error(f"❌ Error loading patient: {e}")
                st.session_state.delete_patient_loaded = False
    
    if st.session_state.get('delete_patient_loaded', False) and st.session_state.get('delete_patient_data'):
        patient_data = st.session_state.delete_patient_data
        
        st.warning("⚠️ **Are you sure you want to delete this patient?**")
        st.info(f"**Name:** {patient_data.get('full_name')}\n\n**ID:** {patient_data.get('patient_id')}")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✅ Confirm Delete", use_container_width=True, type="primary"):
                try:
                    service.delete_patient(patient_id)
                    st.success("✅ Patient deleted successfully!")
                    st.session_state.show_delete_patient = False
                    st.session_state.delete_patient_loaded = False
                    st.session_state.delete_patient_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to delete patient: {e}")
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_delete_patient = False
                st.session_state.delete_patient_loaded = False
                st.session_state.delete_patient_data = None
                st.rerun()
    
    st.markdown("---")


def display_patient_statistics(service: PatientService):
    """Display patient statistics (always visible at top)"""
    st.subheader("📊 Patient Statistics")
    
    try:
        all_patients = service.get_all_patients()
        
        if not all_patients:
            col1 = st.columns(1)[0]
            with col1:
                st.metric("Total Patients", 0)
            return
        
        total = len(all_patients)
        normal = sum(1 for p in all_patients if p.status == 0)
        urgent = sum(1 for p in all_patients if p.status == 1)
        super_urgent = sum(1 for p in all_patients if p.status == 2)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Patients", total)
        
        with col2:
            st.metric("Normal", normal)
        
        with col3:
            st.metric("Urgent", urgent)
        
        with col4:
            st.metric("Super-Urgent", super_urgent)
    
    except Exception as e:
        st.error(f"❌ Error loading statistics: {e}")


def display_patients_table(service: PatientService, search_query: str = "", status_filter: str = "All"):
    """Display patients in a table with selection"""
    try:
        # Get patients
        if search_query:
            patients = service.search_patients(search_query)
        else:
            patients = service.get_all_patients()
        
        # Filter by status
        if status_filter != "All":
            status_map = {"Normal": 0, "Urgent": 1, "Super-Urgent": 2}
            patients = [p for p in patients if p.status == status_map[status_filter]]
        
        if not patients:
            st.info("No patients found.")
            return
        
        # Convert to display format
        import pandas as pd
        
        data = []
        for patient in patients:
            data.append({
                'ID': patient.patient_id,
                'Name': patient.full_name,
                'Age': patient.age,
                'Gender': patient.gender or 'N/A',
                'Status': patient.status_text,
                'Phone': patient.phone_number or 'N/A',
                'Email': patient.email or 'N/A'
            })
        
        df = pd.DataFrame(data)
        
        # Add a selection checkbox column
        # Initialize selection state if not exists
        if 'patient_selection_state' not in st.session_state:
            st.session_state.patient_selection_state = {}
        
        # Add Select column with checkboxes (False by default)
        df['Select'] = [st.session_state.patient_selection_state.get(patient.patient_id, False) for patient in patients]
        
        # Reorder columns to show Select first
        column_order = ['Select', 'ID', 'Name', 'Age', 'Gender', 'Status', 'Phone', 'Email']
        df = df[column_order]
        
        st.subheader("📋 Patient List - Click the checkbox in a row to select it")
        
        # Display interactive table with selection column
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select", width="small", help="Check to select this row"),
                "ID": st.column_config.NumberColumn("ID", width="small", disabled=True),
                "Name": st.column_config.TextColumn("Name", width="medium", disabled=True),
                "Age": st.column_config.NumberColumn("Age", width="small", disabled=True),
                "Gender": st.column_config.TextColumn("Gender", width="small", disabled=True),
                "Status": st.column_config.TextColumn("Status", width="small", disabled=True),
                "Phone": st.column_config.TextColumn("Phone", width="medium", disabled=True),
                "Email": st.column_config.TextColumn("Email", width="large", disabled=True)
            },
            key="patients_table_editor",
            num_rows="fixed"
        )
        
        # Find selected row(s) - only one should be selected
        selected_rows: pd.DataFrame = edited_df[edited_df['Select'] == True]  # type: ignore
        
        if len(selected_rows) > 0:
            # Get the first selected row (in case multiple are selected)
            selected_row = selected_rows.iloc[0]
            selected_id = int(selected_row['ID'])
            st.session_state.selected_patient_id = selected_id
            
            # Update selection state - uncheck all others
            for idx, patient in enumerate(patients):
                if patient.patient_id == selected_id:
                    st.session_state.patient_selection_state[patient.patient_id] = True
                else:
                    st.session_state.patient_selection_state[patient.patient_id] = False
            
            st.success(f"✅ Selected: {selected_row['Name']} (ID: {selected_id}) - Click Edit/Delete button above to proceed")
        else:
            # No row selected - clear selection state
            st.session_state.selected_patient_id = None
            for patient in patients:
                st.session_state.patient_selection_state[patient.patient_id] = False
        
        st.caption(f"Showing {len(patients)} patient(s) - Check a row's checkbox to select it, then click Edit/Delete button")
    
    except Exception as e:
        st.error(f"❌ Error loading patients: {e}")


def show_specialization_management():
    """Specialization Management page"""
    st.title("🏥 Specialization Management")
    st.markdown("---")
    
    service = st.session_state.specialization_service
    
    # Display statistics at the top (always visible)
    display_specialization_statistics(service)
    
    st.markdown("---")
    
    # Search section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search Specializations",
            placeholder="Search by name or description...",
            key="specialization_search"
        )
    
    with col2:
        st.write("")  # Spacing
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add New Specialization", use_container_width=True, type="primary"):
            st.session_state.show_add_specialization = True
            st.rerun()
    
    with col2:
        if st.button("✏️ Edit Specialization", use_container_width=True):
            # Check if specialization is selected
            if 'selected_specialization_id' in st.session_state and st.session_state.selected_specialization_id:
                st.session_state.edit_specialization_id = st.session_state.selected_specialization_id
            st.session_state.show_edit_specialization = True
            st.rerun()
    
    with col3:
        if st.button("🗑️ Delete Specialization", use_container_width=True):
            # Check if specialization is selected
            if 'selected_specialization_id' in st.session_state and st.session_state.selected_specialization_id:
                st.session_state.delete_specialization_id = st.session_state.selected_specialization_id
            st.session_state.show_delete_specialization = True
            st.rerun()
    
    with col4:
        active_filter = st.selectbox(
            "Filter",
            ["All", "Active Only", "Inactive Only"],
            key="specialization_filter"
        )
    
    st.markdown("---")
    
    # Handle modals/dialogs
    if st.session_state.get('show_add_specialization', False):
        show_add_specialization_dialog(service)
    
    if st.session_state.get('show_edit_specialization', False):
        show_edit_specialization_dialog(service)
    
    if st.session_state.get('show_delete_specialization', False):
        show_delete_specialization_dialog(service)
    
    # Display specializations table
    display_specializations_table(service, search_query, active_filter)


def show_add_specialization_dialog(service: SpecializationService):
    """Show add specialization form"""
    st.subheader("➕ Add New Specialization")
    
    with st.form("add_specialization_form", clear_on_submit=True):
        name = st.text_input("Specialization Name *", placeholder="e.g., Cardiology, Pediatrics")
        description = st.text_area("Description", placeholder="Brief description of the specialization")
        max_capacity = st.number_input(
            "Maximum Queue Capacity *",
            min_value=1,
            max_value=1000,
            value=10,
            step=1
        )
        is_active = st.checkbox("Active", value=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("💾 Save Specialization", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            if not name or not name.strip():
                st.error("Specialization name is required!")
            else:
                try:
                    specialization_data = {
                        'name': name.strip(),
                        'description': description if description else None,
                        'max_capacity': max_capacity,
                        'is_active': is_active
                    }
                    
                    specialization_id = service.create_specialization(specialization_data)
                    st.success(f"✅ Specialization added successfully! (ID: {specialization_id})")
                    st.session_state.show_add_specialization = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to add specialization: {e}")
        
        if cancel:
            st.session_state.show_add_specialization = False
            st.rerun()
    
    st.markdown("---")


def show_edit_specialization_dialog(service: SpecializationService):
    """Show edit specialization form"""
    st.subheader("✏️ Edit Specialization")
    
    # Get specialization ID from selection (priority) or manual input
    selected_id = st.session_state.get('selected_specialization_id')
    
    if selected_id:
        # Auto-load selected specialization
        specialization_id = selected_id
        st.info(f"📝 Editing Specialization ID: {selected_id} (selected from table)")
        try:
            specialization = service.get_specialization(specialization_id)
            if specialization:
                st.session_state.edit_specialization_data = specialization.to_dict()
                st.session_state.specialization_loaded = True
            else:
                st.error("❌ Specialization not found!")
                st.session_state.specialization_loaded = False
        except Exception as e:
            st.error(f"❌ Error loading specialization: {e}")
            st.session_state.specialization_loaded = False
    else:
        # Manual ID entry if no selection
        specialization_id = st.number_input(
            "Enter Specialization ID to Edit (or select a row from the table above)",
            min_value=1,
            step=1,
            value=st.session_state.get('edit_specialization_id', 1),
            key="edit_specialization_id_input"
        )
        
        if st.button("Load Specialization", use_container_width=True):
            try:
                specialization = service.get_specialization(specialization_id)
                if specialization:
                    st.session_state.edit_specialization_data = specialization.to_dict()
                    st.session_state.specialization_loaded = True
                    st.success("✅ Specialization loaded!")
                else:
                    st.error("❌ Specialization not found!")
                    st.session_state.specialization_loaded = False
            except Exception as e:
                st.error(f"❌ Error loading specialization: {e}")
                st.session_state.specialization_loaded = False
    
    if st.session_state.get('specialization_loaded', False) and st.session_state.get('edit_specialization_data'):
        specialization_data = st.session_state.edit_specialization_data
        
        with st.form("edit_specialization_form"):
            name = st.text_input(
                "Specialization Name *",
                value=specialization_data.get('name', ''),
                key="edit_spec_name"
            )
            description = st.text_area(
                "Description",
                value=specialization_data.get('description', '') or '',
                key="edit_spec_description"
            )
            max_capacity = st.number_input(
                "Maximum Queue Capacity *",
                min_value=1,
                max_value=1000,
                value=specialization_data.get('max_capacity', 10),
                step=1,
                key="edit_spec_capacity"
            )
            is_active = st.checkbox(
                "Active",
                value=specialization_data.get('is_active', True),
                key="edit_spec_active"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submit = st.form_submit_button("💾 Update Specialization", use_container_width=True, type="primary")
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if not name or not name.strip():
                    st.error("Specialization name is required!")
                else:
                    try:
                        update_data = {
                            'name': name.strip(),
                            'description': description if description else None,
                            'max_capacity': max_capacity,
                            'is_active': is_active
                        }
                        
                        service.update_specialization(specialization_id, update_data)
                        st.success(f"✅ Specialization updated successfully!")
                        st.session_state.show_edit_specialization = False
                        st.session_state.specialization_loaded = False
                        st.session_state.edit_specialization_data = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to update specialization: {e}")
            
            if cancel:
                st.session_state.show_edit_specialization = False
                st.session_state.specialization_loaded = False
                st.session_state.edit_specialization_data = None
                st.rerun()
    
    st.markdown("---")


def show_delete_specialization_dialog(service: SpecializationService):
    """Show delete specialization dialog"""
    st.subheader("🗑️ Delete Specialization")
    
    # Get specialization ID from selection (priority) or manual input
    selected_id = st.session_state.get('selected_specialization_id')
    
    if selected_id:
        # Auto-load selected specialization
        specialization_id = selected_id
        st.info(f"🗑️ Deleting Specialization ID: {selected_id} (selected from table)")
        try:
            specialization = service.get_specialization(specialization_id)
            if not specialization:
                st.error("❌ Specialization not found!")
            else:
                st.session_state.delete_specialization_data = specialization.to_dict()
                st.session_state.delete_specialization_loaded = True
        except Exception as e:
            st.error(f"❌ Error loading specialization: {e}")
            st.session_state.delete_specialization_loaded = False
    else:
        # Manual ID entry if no selection
        specialization_id = st.number_input(
            "Enter Specialization ID to Delete (or select a row from the table above)",
            min_value=1,
            step=1,
            value=st.session_state.get('delete_specialization_id', 1),
            key="delete_specialization_id_input"
        )
        
        if st.button("Load Specialization", use_container_width=True):
            try:
                specialization = service.get_specialization(specialization_id)
                if not specialization:
                    st.error("❌ Specialization not found!")
                    st.session_state.delete_specialization_loaded = False
                else:
                    st.session_state.delete_specialization_data = specialization.to_dict()
                    st.session_state.delete_specialization_loaded = True
            except Exception as e:
                st.error(f"❌ Error loading specialization: {e}")
                st.session_state.delete_specialization_loaded = False
    
    # Show confirmation if specialization is loaded
    if st.session_state.get('delete_specialization_loaded', False) and st.session_state.get('delete_specialization_data'):
        specialization_data = st.session_state.delete_specialization_data
        specialization = service.get_specialization(specialization_id)
        
        if specialization:
            # Show confirmation
            st.warning(f"⚠️ Are you sure you want to delete **{specialization.name}**?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                    try:
                        service.delete_specialization(specialization_id, force=False)
                        st.success(f"✅ Specialization '{specialization.name}' deactivated successfully!")
                        st.session_state.show_delete_specialization = False
                        st.session_state.delete_specialization_loaded = False
                        st.session_state.delete_specialization_data = None
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ Cannot delete: {e}")
                    except Exception as e:
                        st.error(f"❌ Failed to delete: {e}")
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_delete_specialization = False
                    st.session_state.delete_specialization_loaded = False
                    st.session_state.delete_specialization_data = None
                    st.rerun()
    
    st.markdown("---")


def display_specializations_table(service: SpecializationService, search_query: str, active_filter: str):
    """Display specializations in a table"""
    try:
        # Get specializations
        if search_query:
            specializations = service.search_specializations(search_query)
        else:
            active_only = active_filter == "Active Only"
            inactive_only = active_filter == "Inactive Only"
            
            if inactive_only:
                all_specs = service.get_all_specializations(active_only=False)
                specializations = [s for s in all_specs if not s.is_active]
            else:
                specializations = service.get_all_specializations(active_only=active_only)
        
        if specializations:
            # Convert to list of dicts for DataFrame
            import pandas as pd
            specializations_data = []
            for spec in specializations:
                stats = service.get_specialization_statistics(spec.specialization_id)
                spec_dict = spec.to_dict()
                spec_dict['current_queue_size'] = stats.get('current_queue_size', 0)
                spec_dict['utilization_percentage'] = stats.get('utilization_percentage', 0)
                spec_dict['assigned_doctors_count'] = stats.get('assigned_doctors_count', 0)
                specializations_data.append(spec_dict)
            
            df = pd.DataFrame(specializations_data)
            
            # Select columns to display
            display_cols = [
                'specialization_id', 'name', 'max_capacity', 'current_queue_size',
                'utilization_percentage', 'assigned_doctors_count', 'is_active_text'
            ]
            
            # Format the dataframe
            if 'utilization_percentage' in df.columns:
                df['utilization_percentage'] = df['utilization_percentage'].apply(lambda x: f"{x:.1f}%")
            
            # Add a selection checkbox column
            # Initialize selection state if not exists
            if 'specialization_selection_state' not in st.session_state:
                st.session_state.specialization_selection_state = {}
            
            # Add Select column with checkboxes (False by default)
            df['Select'] = [st.session_state.specialization_selection_state.get(spec.specialization_id, False) for spec in specializations]
            
            st.subheader("📋 Specialization List - Click the checkbox in a row to select it")
            
            # Display interactive table with selection column
            edited_df = st.data_editor(
                df[['Select'] + display_cols],
                use_container_width=True,
                hide_index=True,
                height=400,
                column_config={
                    "Select": st.column_config.CheckboxColumn("Select", width="small", help="Check to select this row"),
                    "specialization_id": st.column_config.NumberColumn("ID", width="small", disabled=True),
                    "name": st.column_config.TextColumn("Name", width="medium", disabled=True),
                    "max_capacity": st.column_config.NumberColumn("Max Capacity", width="small", disabled=True),
                    "current_queue_size": st.column_config.NumberColumn("Current Queue", width="small", disabled=True),
                    "utilization_percentage": st.column_config.TextColumn("Utilization", width="small", disabled=True),
                    "assigned_doctors_count": st.column_config.NumberColumn("Doctors", width="small", disabled=True),
                    "is_active_text": st.column_config.TextColumn("Status", width="small", disabled=True)
                },
                key="specializations_table_editor",
                num_rows="fixed"
            )
            
            # Find selected row(s) - only one should be selected
            selected_rows: pd.DataFrame = edited_df[edited_df['Select'] == True]  # type: ignore
            
            if len(selected_rows) > 0:
                # Get the first selected row (in case multiple are selected)
                selected_row = selected_rows.iloc[0]
                selected_id = int(selected_row['specialization_id'])
                st.session_state.selected_specialization_id = selected_id
                
                # Update selection state - uncheck all others
                for idx, spec in enumerate(specializations):
                    if spec.specialization_id == selected_id:
                        st.session_state.specialization_selection_state[spec.specialization_id] = True
                    else:
                        st.session_state.specialization_selection_state[spec.specialization_id] = False
                
                st.success(f"✅ Selected: {selected_row['name']} (ID: {selected_id}) - Click Edit/Delete button above to proceed")
            else:
                # No row selected - clear selection state
                st.session_state.selected_specialization_id = None
                for spec in specializations:
                    st.session_state.specialization_selection_state[spec.specialization_id] = False
            
            st.caption(f"Showing {len(specializations)} specialization(s) - Check a row's checkbox to select it, then click Edit/Delete button")
        else:
            st.info("No specializations found matching your criteria.")
    
    except Exception as e:
        st.error(f"❌ Error loading specializations: {e}")


def display_specialization_statistics(service: SpecializationService):
    """Display specialization statistics (always visible at top)"""
    st.subheader("📊 Specialization Statistics")
    
    try:
        all_specializations = service.get_all_specializations(active_only=False)
        
        if not all_specializations:
            col1 = st.columns(1)[0]
            with col1:
                st.metric("Total Specializations", 0)
            return
        
        total = len(all_specializations)
        active = len([s for s in all_specializations if s.is_active])
        inactive = total - active
        total_capacity = sum(s.max_capacity for s in all_specializations if s.is_active)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Specializations", total)
        
        with col2:
            st.metric("Active", active)
        
        with col3:
            st.metric("Inactive", inactive)
        
        with col4:
            st.metric("Total Capacity", total_capacity)
    
    except Exception as e:
        st.error(f"❌ Error loading statistics: {e}")


def show_queue_management():
    """Queue Management page"""
    st.title("📋 Queue Management")
    st.markdown("---")
    
    queue_service = st.session_state.queue_service
    patient_service = st.session_state.patient_service
    specialization_service = st.session_state.specialization_service
    
    # Display statistics at the top (always visible)
    display_queue_statistics(queue_service)
    
    st.markdown("---")
    
    # Specialization selector with "All" option
    specializations = specialization_service.get_all_specializations(active_only=True)
    if not specializations:
        st.warning("⚠️ No active specializations found. Please add specializations first.")
        return
    
    spec_options = {"📋 All Specializations": None}
    spec_options.update({f"{s.name} (ID: {s.specialization_id})": s.specialization_id for s in specializations})
    
    selected_spec_display = st.selectbox(
        "🏥 Select Specialization",
        options=list(spec_options.keys()),
        key="queue_specialization_select"
    )
    selected_spec_id = spec_options[selected_spec_display]
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add to Queue", use_container_width=True, type="primary"):
            if selected_spec_id is None:
                st.warning("⚠️ Please select a specific specialization to add patients to the queue.")
            else:
                st.session_state.show_add_to_queue = True
                st.session_state.add_queue_specialization_id = selected_spec_id
                st.rerun()
    
    with col2:
        if st.button("✅ Serve Next Patient", use_container_width=True):
            if selected_spec_id is None:
                st.warning("⚠️ Please select a specific specialization to serve patients.")
            else:
                st.session_state.serve_next_specialization_id = selected_spec_id
                st.rerun()
    
    with col3:
        if st.button("🔄 Refresh Queue", use_container_width=True):
            st.rerun()
    
    with col4:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.show_queue_analytics = True
            st.session_state.analytics_specialization_id = selected_spec_id
            st.rerun()
    
    st.markdown("---")
    
    # Handle modals/dialogs
    if st.session_state.get('show_add_to_queue', False):
        show_add_to_queue_dialog(queue_service, patient_service, specialization_service)
    
    if st.session_state.get('show_queue_analytics', False):
        if selected_spec_id is not None:
            show_queue_analytics(queue_service, selected_spec_id)
        else:
            st.info("📊 Select a specific specialization to view detailed analytics.")
    
    # Handle serve next patient
    if st.session_state.get('serve_next_specialization_id'):
        serve_next_patient(queue_service, st.session_state.serve_next_specialization_id)
        st.session_state.serve_next_specialization_id = None
        st.rerun()
    
    # Display queue table
    if selected_spec_id is None:
        # Show all queues
        display_all_queues_table(queue_service, patient_service, specialization_service)
    else:
        # Show single specialization queue
        display_queue_table(queue_service, patient_service, selected_spec_id)


def display_queue_statistics(service: QueueService):
    """Display queue statistics (always visible at top)"""
    st.subheader("📊 Queue Statistics")
    
    try:
        stats = service.get_queue_statistics()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Active", stats['total_active'])
        
        with col2:
            st.metric("Normal", stats['normal_count'])
        
        with col3:
            st.metric("Urgent", stats['urgent_count'])
        
        with col4:
            st.metric("Super-Urgent", stats['super_urgent_count'])
        
        with col5:
            avg_wait = stats.get('average_wait_time', 0)
            st.metric("Avg Wait Time", f"{avg_wait} min" if avg_wait > 0 else "N/A")
    
    except Exception as e:
        st.error(f"❌ Error loading statistics: {e}")


def show_add_to_queue_dialog(queue_service: QueueService, patient_service: PatientService, 
                            specialization_service: SpecializationService):
    """Show add patient to queue form"""
    st.subheader("➕ Add Patient to Queue")
    
    specialization_id = st.session_state.get('add_queue_specialization_id')
    if specialization_id:
        spec = specialization_service.get_specialization(specialization_id)
        if spec:
            st.info(f"📋 Adding to: **{spec.name}**")
    
    # Get all patients
    all_patients = patient_service.get_all_patients()
    if not all_patients:
        st.warning("⚠️ No patients found. Please add patients first.")
        if st.button("Close"):
            st.session_state.show_add_to_queue = False
            st.rerun()
        return
    
    # Patient selection
    patient_options = {f"{p.patient_id} - {p.full_name}": p.patient_id for p in all_patients}
    selected_patient_display = st.selectbox(
        "👤 Select Patient",
        options=list(patient_options.keys()),
        key="add_queue_patient_select"
    )
    selected_patient_id = patient_options[selected_patient_display]
    
    # Priority selection
    priority_options = {
        "Normal (0)": 0,
        "Urgent (1)": 1,
        "Super-Urgent (2)": 2
    }
    selected_priority_display = st.selectbox(
        "⚡ Priority Level",
        options=list(priority_options.keys()),
        index=0,
        key="add_queue_priority_select"
    )
    selected_priority = priority_options[selected_priority_display]
    
    # Show capacity info
    if specialization_id:
        spec = specialization_service.get_specialization(specialization_id)
        if spec:
            queue = queue_service.get_queue(specialization_id, active_only=True)
            current_size = len(queue)
            capacity_usage = (current_size / spec.max_capacity * 100) if spec.max_capacity > 0 else 0
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Queue Size", f"{current_size}/{spec.max_capacity}")
            with col2:
                st.metric("Capacity Usage", f"{capacity_usage:.1f}%")
            
            if current_size >= spec.max_capacity:
                st.error("⚠️ Queue is at maximum capacity!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Add to Queue", use_container_width=True, type="primary"):
            try:
                queue_entry_id = queue_service.add_patient_to_queue(
                    selected_patient_id,
                    specialization_id,
                    selected_priority
                )
                st.success(f"✅ Patient added to queue successfully! (Queue Entry ID: {queue_entry_id})")
                st.session_state.show_add_to_queue = False
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ Failed to add patient to queue: {e}")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_add_to_queue = False
            st.rerun()
    
    st.markdown("---")


def display_all_queues_table(queue_service: QueueService, patient_service: PatientService,
                            specialization_service: SpecializationService):
    """Display all queues across all specializations"""
    try:
        all_queues = queue_service.get_all_queues(active_only=True)
        
        if not all_queues:
            st.info("📭 No active queues found. Add patients to get started.")
            return
        
        # Get patient details for each queue entry
        import pandas as pd
        
        data = []
        for spec_id, queue in all_queues.items():
            spec = specialization_service.get_specialization(spec_id)
            spec_name = spec.name if spec else f"Specialization {spec_id}"
            
            for entry in queue:
                patient = patient_service.get_patient(entry.patient_id)
                if patient:
                    data.append({
                        'Specialization': spec_name,
                        'Position': entry.position,
                        'Patient ID': entry.patient_id,
                        'Name': patient.full_name,
                        'Priority': entry.status_text,
                        'Wait Time': entry.wait_time_formatted,
                        'Joined At': entry.joined_at.strftime("%H:%M:%S") if entry.joined_at else "N/A",
                        'Queue Entry ID': entry.queue_entry_id
                    })
        
        if not data:
            st.info("📭 No active queue entries found.")
            return
        
        df = pd.DataFrame(data)
        
        # Add selection column
        if 'queue_selection_state' not in st.session_state:
            st.session_state.queue_selection_state = {}
        
        # Create a unique key for selection state
        df['Select'] = [st.session_state.queue_selection_state.get(row['Queue Entry ID'], False) 
                        for _, row in df.iterrows()]
        
        # Reorder columns
        column_order = ['Select', 'Specialization', 'Position', 'Patient ID', 'Name', 'Priority', 'Wait Time', 'Joined At', 'Queue Entry ID']
        df = df[column_order]
        
        st.subheader("📋 All Queues (All Specializations)")
        
        # Display interactive table
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            height=600,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select", width="small"),
                "Specialization": st.column_config.TextColumn("Specialization", width="medium", disabled=True),
                "Position": st.column_config.NumberColumn("Pos", width="small", disabled=True),
                "Patient ID": st.column_config.NumberColumn("Patient ID", width="small", disabled=True),
                "Name": st.column_config.TextColumn("Name", width="medium", disabled=True),
                "Priority": st.column_config.TextColumn("Priority", width="small", disabled=True),
                "Wait Time": st.column_config.TextColumn("Wait Time", width="small", disabled=True),
                "Joined At": st.column_config.TextColumn("Joined", width="small", disabled=True),
                "Queue Entry ID": st.column_config.NumberColumn("Entry ID", width="small", disabled=True)
            },
            key="all_queues_table_editor",
            num_rows="fixed"
        )
        
        # Find selected row(s)
        selected_rows: pd.DataFrame = edited_df[edited_df['Select'] == True]  # type: ignore
        
        if len(selected_rows) > 0:
            selected_row = selected_rows.iloc[0]
            selected_entry_id = int(selected_row['Queue Entry ID'])
            st.session_state.selected_queue_entry_id = selected_entry_id
            
            # Update selection state
            for entry_id in df['Queue Entry ID']:
                if entry_id == selected_entry_id:
                    st.session_state.queue_selection_state[entry_id] = True
                else:
                    st.session_state.queue_selection_state[entry_id] = False
            
            # Action buttons for selected entry
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⚡ Change Priority", use_container_width=True):
                    st.session_state.show_change_priority = True
                    st.session_state.change_priority_entry_id = selected_entry_id
                    st.rerun()
            
            with col2:
                if st.button("✅ Serve Patient", use_container_width=True):
                    try:
                        queue_service.serve_patient(selected_entry_id)
                        st.success("✅ Patient served successfully!")
                        st.session_state.selected_queue_entry_id = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to serve patient: {e}")
            
            with col3:
                if st.button("🗑️ Remove from Queue", use_container_width=True):
                    st.session_state.show_remove_from_queue = True
                    st.session_state.remove_queue_entry_id = selected_entry_id
                    st.rerun()
        else:
            st.session_state.selected_queue_entry_id = None
            for entry_id in df['Queue Entry ID']:
                st.session_state.queue_selection_state[entry_id] = False
        
        # Handle change priority dialog
        if st.session_state.get('show_change_priority', False):
            show_change_priority_dialog(queue_service)
        
        # Handle remove from queue dialog
        if st.session_state.get('show_remove_from_queue', False):
            show_remove_from_queue_dialog(queue_service)
        
        st.caption(f"Showing {len(data)} patient(s) across all specializations - Select a row to perform actions")
    
    except Exception as e:
        st.error(f"❌ Error loading queues: {e}")


def display_queue_table(queue_service: QueueService, patient_service: PatientService, 
                       specialization_id: int):
    """Display queue table with patient information"""
    try:
        queue = queue_service.get_queue(specialization_id, active_only=True)
        
        if not queue:
            st.info("📭 Queue is empty. Add patients to get started.")
            return
        
        # Get patient details for each queue entry
        import pandas as pd
        
        data = []
        for entry in queue:
            patient = patient_service.get_patient(entry.patient_id)
            if patient:
                data.append({
                    'Position': entry.position,
                    'Patient ID': entry.patient_id,
                    'Name': patient.full_name,
                    'Priority': entry.status_text,
                    'Wait Time': entry.wait_time_formatted,
                    'Joined At': entry.joined_at.strftime("%H:%M:%S") if entry.joined_at else "N/A",
                    'Queue Entry ID': entry.queue_entry_id
                })
        
        df = pd.DataFrame(data)
        
        # Add selection column
        if 'queue_selection_state' not in st.session_state:
            st.session_state.queue_selection_state = {}
        
        df['Select'] = [st.session_state.queue_selection_state.get(entry.queue_entry_id, False) 
                        for entry in queue]
        
        # Reorder columns
        column_order = ['Select', 'Position', 'Patient ID', 'Name', 'Priority', 'Wait Time', 'Joined At', 'Queue Entry ID']
        df = df[column_order]
        
        st.subheader("📋 Current Queue")
        
        # Display interactive table
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select", width="small"),
                "Position": st.column_config.NumberColumn("Pos", width="small", disabled=True),
                "Patient ID": st.column_config.NumberColumn("Patient ID", width="small", disabled=True),
                "Name": st.column_config.TextColumn("Name", width="medium", disabled=True),
                "Priority": st.column_config.TextColumn("Priority", width="small", disabled=True),
                "Wait Time": st.column_config.TextColumn("Wait Time", width="small", disabled=True),
                "Joined At": st.column_config.TextColumn("Joined", width="small", disabled=True),
                "Queue Entry ID": st.column_config.NumberColumn("Entry ID", width="small", disabled=True)
            },
            key="queue_table_editor",
            num_rows="fixed"
        )
        
        # Find selected row(s)
        selected_rows: pd.DataFrame = edited_df[edited_df['Select'] == True]  # type: ignore
        
        if len(selected_rows) > 0:
            selected_row = selected_rows.iloc[0]
            selected_entry_id = int(selected_row['Queue Entry ID'])
            st.session_state.selected_queue_entry_id = selected_entry_id
            
            # Update selection state
            for entry in queue:
                if entry.queue_entry_id == selected_entry_id:
                    st.session_state.queue_selection_state[entry.queue_entry_id] = True
                else:
                    st.session_state.queue_selection_state[entry.queue_entry_id] = False
            
            # Action buttons for selected entry
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⚡ Change Priority", use_container_width=True):
                    st.session_state.show_change_priority = True
                    st.session_state.change_priority_entry_id = selected_entry_id
                    st.rerun()
            
            with col2:
                if st.button("✅ Serve Patient", use_container_width=True):
                    try:
                        queue_service.serve_patient(selected_entry_id)
                        st.success("✅ Patient served successfully!")
                        st.session_state.selected_queue_entry_id = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to serve patient: {e}")
            
            with col3:
                if st.button("🗑️ Remove from Queue", use_container_width=True):
                    st.session_state.show_remove_from_queue = True
                    st.session_state.remove_queue_entry_id = selected_entry_id
                    st.rerun()
        else:
            st.session_state.selected_queue_entry_id = None
            for entry in queue:
                st.session_state.queue_selection_state[entry.queue_entry_id] = False
        
        # Handle change priority dialog
        if st.session_state.get('show_change_priority', False):
            show_change_priority_dialog(queue_service)
        
        # Handle remove from queue dialog
        if st.session_state.get('show_remove_from_queue', False):
            show_remove_from_queue_dialog(queue_service)
        
        st.caption(f"Showing {len(queue)} patient(s) in queue - Select a row to perform actions")
    
    except Exception as e:
        st.error(f"❌ Error loading queue: {e}")


def serve_next_patient(queue_service: QueueService, specialization_id: int):
    """Serve the next patient in queue"""
    try:
        next_patient = queue_service.get_next_patient(specialization_id)
        if next_patient:
            st.success(f"✅ Patient {next_patient.patient_id} has been served!")
        else:
            st.info("📭 Queue is empty. No patients to serve.")
    except Exception as e:
        st.error(f"❌ Failed to serve next patient: {e}")


def show_change_priority_dialog(queue_service: QueueService):
    """Show change priority form"""
    st.subheader("⚡ Change Patient Priority")
    
    entry_id = st.session_state.get('change_priority_entry_id')
    if not entry_id:
        st.error("No queue entry selected")
        return
    
    entry = queue_service.get_queue_entry(entry_id)
    if not entry:
        st.error("Queue entry not found")
        return
    
    st.info(f"Current Priority: **{entry.status_text}**")
    
    priority_options = {
        "Normal (0)": 0,
        "Urgent (1)": 1,
        "Super-Urgent (2)": 2
    }
    selected_priority_display = st.selectbox(
        "New Priority Level",
        options=list(priority_options.keys()),
        index=entry.status,
        key="change_priority_select"
    )
    new_priority = priority_options[selected_priority_display]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Update Priority", use_container_width=True, type="primary"):
            try:
                queue_service.update_patient_priority(entry_id, new_priority)
                st.success("✅ Priority updated successfully!")
                st.session_state.show_change_priority = False
                st.session_state.change_priority_entry_id = None
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to update priority: {e}")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_change_priority = False
            st.session_state.change_priority_entry_id = None
            st.rerun()
    
    st.markdown("---")


def show_remove_from_queue_dialog(queue_service: QueueService):
    """Show remove from queue form"""
    st.subheader("🗑️ Remove Patient from Queue")
    
    entry_id = st.session_state.get('remove_queue_entry_id')
    if not entry_id:
        st.error("No queue entry selected")
        return
    
    entry = queue_service.get_queue_entry(entry_id)
    if not entry:
        st.error("Queue entry not found")
        return
    
    st.warning(f"⚠️ Are you sure you want to remove this patient from the queue?")
    
    removal_reason = st.text_area(
        "Removal Reason (optional)",
        key="removal_reason_input",
        placeholder="Enter reason for removal..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, Remove", use_container_width=True, type="primary"):
            try:
                queue_service.remove_patient_from_queue(entry_id, removal_reason if removal_reason else None)
                st.success("✅ Patient removed from queue successfully!")
                st.session_state.show_remove_from_queue = False
                st.session_state.remove_queue_entry_id = None
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to remove patient: {e}")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_remove_from_queue = False
            st.session_state.remove_queue_entry_id = None
            st.rerun()
    
    st.markdown("---")


def show_queue_analytics(queue_service: QueueService, specialization_id: int):
    """Show queue analytics"""
    st.subheader("📊 Queue Analytics")
    
    try:
        stats = queue_service.get_queue_statistics(specialization_id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Active", stats['total_active'])
        
        with col2:
            st.metric("Normal", stats['normal_count'])
        
        with col3:
            st.metric("Urgent", stats['urgent_count'])
        
        with col4:
            st.metric("Super-Urgent", stats['super_urgent_count'])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_wait = stats.get('average_wait_time', 0)
            st.metric("Average Wait Time", f"{avg_wait} minutes" if avg_wait > 0 else "N/A")
        
        with col2:
            longest_wait = stats.get('longest_wait_time', 0)
            st.metric("Longest Wait Time", f"{longest_wait} minutes" if longest_wait > 0 else "N/A")
        
        if st.button("Close Analytics"):
            st.session_state.show_queue_analytics = False
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
    
    st.markdown("---")


def show_doctor_management():
    """Doctor Management page"""
    st.title("👨‍⚕️ Doctor Management")
    st.markdown("---")
    
    doctor_service = st.session_state.doctor_service
    specialization_service = st.session_state.specialization_service
    
    # Display statistics at the top (always visible)
    display_doctor_statistics(doctor_service)
    
    st.markdown("---")
    
    # Search and filter section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search Doctors",
            placeholder="Search by name, license, or email...",
            key="doctor_search"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Active", "Inactive", "On Leave"],
            key="doctor_status_filter"
        )
    
    with col3:
        st.write("")  # Spacing
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Doctor", use_container_width=True, type="primary"):
            st.session_state.show_add_doctor = True
            st.rerun()
    
    with col2:
        if st.button("✏️ Edit Doctor", use_container_width=True):
            # Check if doctor is selected
            if 'selected_doctor_id' in st.session_state and st.session_state.selected_doctor_id:
                st.session_state.edit_doctor_id = st.session_state.selected_doctor_id
            st.session_state.show_edit_doctor = True
            st.rerun()
    
    with col3:
        if st.button("🗑️ Delete Doctor", use_container_width=True):
            # Check if doctor is selected
            if 'selected_doctor_id' in st.session_state and st.session_state.selected_doctor_id:
                st.session_state.delete_doctor_id = st.session_state.selected_doctor_id
            st.session_state.show_delete_doctor = True
            st.rerun()
    
    st.markdown("---")
    
    # Handle modals/dialogs
    if st.session_state.get('show_add_doctor', False):
        show_add_doctor_dialog(doctor_service, specialization_service)
    
    if st.session_state.get('show_edit_doctor', False):
        show_edit_doctor_dialog(doctor_service, specialization_service)
    
    if st.session_state.get('show_delete_doctor', False):
        show_delete_doctor_dialog(doctor_service)
    
    # Display doctors table
    display_doctors_table(doctor_service, search_query, status_filter)


def display_doctor_statistics(service: DoctorService):
    """Display doctor statistics (always visible at top)"""
    st.subheader("📊 Doctor Statistics")
    
    try:
        all_doctors = service.get_all_doctors(active_only=False)
        
        if not all_doctors:
            col1 = st.columns(1)[0]
            with col1:
                st.metric("Total Doctors", 0)
            return
        
        total = len(all_doctors)
        active = len([d for d in all_doctors if d.status == 'Active'])
        inactive = len([d for d in all_doctors if d.status == 'Inactive'])
        on_leave = len([d for d in all_doctors if d.status == 'On Leave'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Doctors", total)
        
        with col2:
            st.metric("Active", active)
        
        with col3:
            st.metric("Inactive", inactive)
        
        with col4:
            st.metric("On Leave", on_leave)
    
    except Exception as e:
        st.error(f"❌ Error loading statistics: {e}")


def display_doctors_table(service: DoctorService, search_query: str = "", status_filter: str = "All"):
    """Display doctors in a table with selection"""
    try:
        # Get doctors
        if search_query:
            doctors = service.search_doctors(search_query)
        else:
            doctors = service.get_all_doctors(active_only=False)
        
        # Filter by status
        if status_filter != "All":
            doctors = [d for d in doctors if d.status == status_filter]
        
        if not doctors:
            st.info("No doctors found.")
            return
        
        # Convert to display format
        import pandas as pd
        
        data = []
        for doctor in doctors:
            data.append({
                'ID': doctor.doctor_id,
                'Name': doctor.display_name,
                'License': doctor.license_number,
                'Status': doctor.status,
                'Phone': doctor.phone_number or 'N/A',
                'Email': doctor.email or 'N/A',
                'Experience': f"{doctor.years_of_experience} years" if doctor.years_of_experience else 'N/A'
            })
        
        df = pd.DataFrame(data)
        
        # Add a selection checkbox column
        if 'doctor_selection_state' not in st.session_state:
            st.session_state.doctor_selection_state = {}
        
        # Add Select column with checkboxes (False by default)
        df['Select'] = [st.session_state.doctor_selection_state.get(doctor.doctor_id, False) for doctor in doctors]
        
        # Reorder columns to show Select first
        column_order = ['Select', 'ID', 'Name', 'License', 'Status', 'Phone', 'Email', 'Experience']
        df = df[column_order]
        
        st.subheader("📋 Doctor List - Click the checkbox in a row to select it")
        
        # Display interactive table with selection column
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select", width="small", help="Check to select this row"),
                "ID": st.column_config.NumberColumn("ID", width="small", disabled=True),
                "Name": st.column_config.TextColumn("Name", width="medium", disabled=True),
                "License": st.column_config.TextColumn("License", width="medium", disabled=True),
                "Status": st.column_config.TextColumn("Status", width="small", disabled=True),
                "Phone": st.column_config.TextColumn("Phone", width="medium", disabled=True),
                "Email": st.column_config.TextColumn("Email", width="large", disabled=True),
                "Experience": st.column_config.TextColumn("Experience", width="small", disabled=True)
            },
            key="doctors_table_editor",
            num_rows="fixed"
        )
        
        # Find selected row(s) - only one should be selected
        selected_rows: pd.DataFrame = edited_df[edited_df['Select'] == True]  # type: ignore
        
        if len(selected_rows) > 0:
            # Get the first selected row (in case multiple are selected)
            selected_row = selected_rows.iloc[0]
            selected_id = int(selected_row['ID'])
            st.session_state.selected_doctor_id = selected_id
            
            # Update selection state - uncheck all others
            for idx, doctor in enumerate(doctors):
                if doctor.doctor_id == selected_id:
                    st.session_state.doctor_selection_state[doctor.doctor_id] = True
                else:
                    st.session_state.doctor_selection_state[doctor.doctor_id] = False
            
            st.success(f"✅ Selected: {selected_row['Name']} (ID: {selected_id}) - Click Edit/Delete button above to proceed")
        else:
            # No row selected - clear selection state
            st.session_state.selected_doctor_id = None
            for doctor in doctors:
                st.session_state.doctor_selection_state[doctor.doctor_id] = False
        
        st.caption(f"Showing {len(doctors)} doctor(s) - Check a row's checkbox to select it, then click Edit/Delete button")
    
    except Exception as e:
        st.error(f"❌ Error loading doctors: {e}")


def show_add_doctor_dialog(doctor_service: DoctorService, specialization_service: SpecializationService):
    """Show add doctor form"""
    st.subheader("➕ Add New Doctor")
    
    with st.form("add_doctor_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", key="add_doctor_name")
            title = st.text_input("Title (e.g., Dr., Prof.)", key="add_doctor_title", placeholder="Dr.")
            license_number = st.text_input("License Number *", key="add_doctor_license")
            phone_number = st.text_input("Phone Number", key="add_doctor_phone")
            email = st.text_input("Email", key="add_doctor_email")
            office_address = st.text_area("Office Address", key="add_doctor_address")
        
        with col2:
            medical_degree = st.text_input("Medical Degree", key="add_doctor_degree")
            years_of_experience = st.number_input("Years of Experience", min_value=0, max_value=100, value=0, key="add_doctor_experience")
            certifications = st.text_area("Certifications", key="add_doctor_certifications")
            status = st.selectbox("Status", ["Active", "Inactive", "On Leave"], index=0, key="add_doctor_status")
            hire_date = st.date_input("Hire Date", key="add_doctor_hire_date")
            bio = st.text_area("Bio/Description", key="add_doctor_bio")
        
        # Specialization selection
        st.markdown("**Specializations**")
        all_specializations = specialization_service.get_all_specializations(active_only=True)
        specialization_options = {f"{s.name} (ID: {s.specialization_id})": s.specialization_id for s in all_specializations}
        selected_specializations = st.multiselect(
            "Select Specializations",
            options=list(specialization_options.keys()),
            key="add_doctor_specializations"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit = st.form_submit_button("✅ Add Doctor", use_container_width=True, type="primary")
        
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            if not full_name or not license_number:
                st.error("❌ Full name and license number are required!")
            else:
                try:
                    doctor_data = {
                        'full_name': full_name,
                        'title': title if title else None,
                        'license_number': license_number,
                        'phone_number': phone_number if phone_number else None,
                        'email': email if email else None,
                        'office_address': office_address if office_address else None,
                        'medical_degree': medical_degree if medical_degree else None,
                        'years_of_experience': years_of_experience if years_of_experience > 0 else None,
                        'certifications': certifications if certifications else None,
                        'status': status,
                        'bio': bio if bio else None,
                        'hire_date': hire_date.isoformat() if hire_date else None,
                        'specialization_ids': [specialization_options[s] for s in selected_specializations]
                    }
                    
                    doctor_id = doctor_service.create_doctor(doctor_data)
                    st.success(f"✅ Doctor added successfully! (ID: {doctor_id})")
                    st.session_state.show_add_doctor = False
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ {str(e)}")
                except Exception as e:
                    st.error(f"❌ Failed to add doctor: {e}")
        
        if cancel:
            st.session_state.show_add_doctor = False
            st.rerun()
    
    st.markdown("---")


def show_edit_doctor_dialog(doctor_service: DoctorService, specialization_service: SpecializationService):
    """Show edit doctor form"""
    st.subheader("✏️ Edit Doctor")
    
    # Get doctor ID from selection (priority) or manual input
    selected_id = st.session_state.get('selected_doctor_id')
    
    if selected_id:
        # Auto-load selected doctor
        doctor_id = selected_id
        st.info(f"📝 Editing Doctor ID: {selected_id} (selected from table)")
        try:
            doctor = doctor_service.get_doctor(doctor_id)
            if doctor:
                st.session_state.edit_doctor_data = doctor.to_dict()
                st.session_state.doctor_loaded = True
            else:
                st.error("❌ Doctor not found!")
                st.session_state.doctor_loaded = False
        except Exception as e:
            st.error(f"❌ Error loading doctor: {e}")
            st.session_state.doctor_loaded = False
    else:
        # Manual ID input
        doctor_id = st.number_input(
            "Enter Doctor ID to Edit (or select a row from the table above)",
            min_value=1,
            step=1,
            value=st.session_state.get('edit_doctor_id', 1),
            key="edit_doctor_id_input"
        )
        
        if st.button("Load Doctor", use_container_width=True):
            try:
                doctor = doctor_service.get_doctor(doctor_id)
                if not doctor:
                    st.error("❌ Doctor not found!")
                    st.session_state.doctor_loaded = False
                else:
                    st.session_state.edit_doctor_data = doctor.to_dict()
                    st.session_state.doctor_loaded = True
            except Exception as e:
                st.error(f"❌ Error loading doctor: {e}")
                st.session_state.doctor_loaded = False
    
    # Show edit form if doctor is loaded
    if st.session_state.get('doctor_loaded', False) and st.session_state.get('edit_doctor_data'):
        doctor_data = st.session_state.edit_doctor_data
        
        with st.form("edit_doctor_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input(
                    "Full Name *",
                    value=doctor_data.get('full_name', ''),
                    key="edit_doctor_name"
                )
                title = st.text_input(
                    "Title",
                    value=doctor_data.get('title', ''),
                    key="edit_doctor_title"
                )
                license_number = st.text_input(
                    "License Number *",
                    value=doctor_data.get('license_number', ''),
                    key="edit_doctor_license"
                )
                phone_number = st.text_input(
                    "Phone Number",
                    value=doctor_data.get('phone_number', ''),
                    key="edit_doctor_phone"
                )
                email = st.text_input(
                    "Email",
                    value=doctor_data.get('email', ''),
                    key="edit_doctor_email"
                )
                office_address = st.text_area(
                    "Office Address",
                    value=doctor_data.get('office_address', ''),
                    key="edit_doctor_address"
                )
            
            with col2:
                medical_degree = st.text_input(
                    "Medical Degree",
                    value=doctor_data.get('medical_degree', ''),
                    key="edit_doctor_degree"
                )
                years_of_experience = st.number_input(
                    "Years of Experience",
                    min_value=0,
                    max_value=100,
                    value=doctor_data.get('years_of_experience', 0),
                    key="edit_doctor_experience"
                )
                certifications = st.text_area(
                    "Certifications",
                    value=doctor_data.get('certifications', ''),
                    key="edit_doctor_certifications"
                )
                
                # Status selectbox
                status_options = ["Active", "Inactive", "On Leave"]
                status_index = 0
                if doctor_data.get('status'):
                    try:
                        status_index = status_options.index(doctor_data.get('status'))
                    except:
                        status_index = 0
                
                status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_index,
                    key="edit_doctor_status"
                )
                
                hire_date_str = doctor_data.get('hire_date')
                hire_date = None
                if hire_date_str:
                    try:
                        hire_date = date.fromisoformat(hire_date_str)
                    except:
                        pass
                
                hire_date = st.date_input(
                    "Hire Date",
                    value=hire_date,
                    key="edit_doctor_hire_date"
                )
                
                bio = st.text_area(
                    "Bio/Description",
                    value=doctor_data.get('bio', ''),
                    key="edit_doctor_bio"
                )
            
            # Specialization selection
            st.markdown("**Specializations**")
            all_specializations = specialization_service.get_all_specializations(active_only=True)
            current_spec_ids = doctor_service.get_doctor_specializations(doctor_id)
            specialization_options = {f"{s.name} (ID: {s.specialization_id})": s.specialization_id for s in all_specializations}
            
            # Pre-select current specializations
            current_spec_names = [name for name, spec_id in specialization_options.items() if spec_id in current_spec_ids]
            
            selected_specializations = st.multiselect(
                "Select Specializations",
                options=list(specialization_options.keys()),
                default=current_spec_names,
                key="edit_doctor_specializations"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("✅ Update Doctor", use_container_width=True, type="primary")
            
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if not full_name or not license_number:
                    st.error("❌ Full name and license number are required!")
                else:
                    try:
                        update_data = {
                            'full_name': full_name,
                            'title': title if title else None,
                            'license_number': license_number,
                            'phone_number': phone_number if phone_number else None,
                            'email': email if email else None,
                            'office_address': office_address if office_address else None,
                            'medical_degree': medical_degree if medical_degree else None,
                            'years_of_experience': years_of_experience if years_of_experience > 0 else None,
                            'certifications': certifications if certifications else None,
                            'status': status,
                            'bio': bio if bio else None,
                            'hire_date': hire_date.isoformat() if hire_date else None
                        }
                        
                        doctor_service.update_doctor(doctor_id, update_data)
                        
                        # Update specializations
                        new_spec_ids = [specialization_options[s] for s in selected_specializations]
                        current_spec_ids = doctor_service.get_doctor_specializations(doctor_id)
                        
                        # Remove unselected specializations
                        for spec_id in current_spec_ids:
                            if spec_id not in new_spec_ids:
                                doctor_service.remove_specialization(doctor_id, spec_id)
                        
                        # Add new specializations
                        for spec_id in new_spec_ids:
                            if spec_id not in current_spec_ids:
                                doctor_service.assign_specialization(doctor_id, spec_id)
                        
                        st.success("✅ Doctor updated successfully!")
                        st.session_state.show_edit_doctor = False
                        st.session_state.doctor_loaded = False
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Failed to update doctor: {e}")
            
            if cancel:
                st.session_state.show_edit_doctor = False
                st.session_state.doctor_loaded = False
                st.rerun()
    
    st.markdown("---")


def show_delete_doctor_dialog(doctor_service: DoctorService):
    """Show delete doctor form"""
    st.subheader("🗑️ Delete Doctor")
    
    # Get doctor ID from selection (priority) or manual input
    selected_id = st.session_state.get('selected_doctor_id')
    
    if selected_id:
        doctor_id = selected_id
        st.info(f"📝 Deleting Doctor ID: {selected_id} (selected from table)")
    else:
        doctor_id = st.number_input(
            "Enter Doctor ID to Delete (or select a row from the table above)",
            min_value=1,
            step=1,
            value=st.session_state.get('delete_doctor_id', 1),
            key="delete_doctor_id_input"
        )
        
        if st.button("Load Doctor", use_container_width=True):
            try:
                doctor = doctor_service.get_doctor(doctor_id)
                if not doctor:
                    st.error("❌ Doctor not found!")
                    st.session_state.delete_doctor_loaded = False
                else:
                    st.session_state.delete_doctor_data = doctor.to_dict()
                    st.session_state.delete_doctor_loaded = True
            except Exception as e:
                st.error(f"❌ Error loading doctor: {e}")
                st.session_state.delete_doctor_loaded = False
    
    # Show confirmation if doctor is loaded
    if st.session_state.get('delete_doctor_loaded', False) and st.session_state.get('delete_doctor_data'):
        doctor_data = st.session_state.delete_doctor_data
        doctor = doctor_service.get_doctor(doctor_id)
        
        if doctor:
            # Show confirmation
            st.warning(f"⚠️ Are you sure you want to delete **{doctor.display_name}**?")
            st.info("Note: This will set the doctor's status to 'Inactive' (soft delete).")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                    try:
                        doctor_service.delete_doctor(doctor_id, force=False)
                        st.success("✅ Doctor deleted successfully!")
                        st.session_state.show_delete_doctor = False
                        st.session_state.delete_doctor_loaded = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to delete doctor: {e}")
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_delete_doctor = False
                    st.session_state.delete_doctor_loaded = False
                    st.rerun()
    else:
        # Try to load doctor for confirmation
        doctor = doctor_service.get_doctor(doctor_id)
        if doctor:
            st.warning(f"⚠️ Are you sure you want to delete **{doctor.display_name}**?")
            st.info("Note: This will set the doctor's status to 'Inactive' (soft delete).")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                    try:
                        doctor_service.delete_doctor(doctor_id, force=False)
                        st.success("✅ Doctor deleted successfully!")
                        st.session_state.show_delete_doctor = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to delete doctor: {e}")
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_delete_doctor = False
                    st.rerun()
        else:
            st.error("❌ Doctor not found!")
    
    st.markdown("---")


def show_appointment_management():
    """Appointment Management page"""
    st.title("📅 Appointment Management")
    st.markdown("---")
    
    appointment_service = st.session_state.appointment_service
    patient_service = st.session_state.patient_service
    doctor_service = st.session_state.doctor_service
    specialization_service = st.session_state.specialization_service
    
    # Display statistics at the top (always visible)
    display_appointment_statistics(appointment_service)
    
    st.markdown("---")
    
    # Search and filter section
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search Appointments",
            placeholder="Search by patient name, doctor name, or reason...",
            key="appointment_search"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Scheduled", "Confirmed", "Cancelled", "Completed", "No-Show"],
            key="appointment_status_filter"
        )
    
    with col3:
        date_filter = st.selectbox(
            "Filter by Date",
            ["All", "Today", "Upcoming", "Past"],
            key="appointment_date_filter"
        )
    
    with col4:
        st.write("")  # Spacing
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Schedule New Appointment", use_container_width=True, type="primary"):
            st.session_state.show_add_appointment = True
            st.rerun()
    
    with col2:
        if st.button("✏️ Edit Appointment", use_container_width=True):
            # Check if appointment is selected
            if 'selected_appointment_id' in st.session_state and st.session_state.selected_appointment_id:
                st.session_state.edit_appointment_id = st.session_state.selected_appointment_id
            st.session_state.show_edit_appointment = True
            st.rerun()
    
    with col3:
        if st.button("✅ Mark Complete", use_container_width=True):
            # Check if appointment is selected
            if 'selected_appointment_id' in st.session_state and st.session_state.selected_appointment_id:
                st.session_state.complete_appointment_id = st.session_state.selected_appointment_id
            st.session_state.show_complete_appointment = True
            st.rerun()
    
    with col4:
        if st.button("❌ Cancel Appointment", use_container_width=True):
            # Check if appointment is selected
            if 'selected_appointment_id' in st.session_state and st.session_state.selected_appointment_id:
                st.session_state.cancel_appointment_id = st.session_state.selected_appointment_id
            st.session_state.show_cancel_appointment = True
            st.rerun()
    
    st.markdown("---")
    
    # Handle modals/dialogs
    if st.session_state.get('show_add_appointment', False):
        show_add_appointment_dialog(appointment_service, patient_service, doctor_service, specialization_service)
    
    if st.session_state.get('show_edit_appointment', False):
        show_edit_appointment_dialog(appointment_service, patient_service, doctor_service, specialization_service)
    
    if st.session_state.get('show_complete_appointment', False):
        show_complete_appointment_dialog(appointment_service)
    
    if st.session_state.get('show_cancel_appointment', False):
        show_cancel_appointment_dialog(appointment_service)
    
    # Display appointments table
    display_appointments_table(appointment_service, patient_service, doctor_service, specialization_service, search_query, status_filter, date_filter)


def display_appointment_statistics(service: AppointmentService):
    """Display appointment statistics (always visible at top)"""
    st.subheader("📊 Appointment Statistics")
    
    try:
        stats = service.get_appointment_statistics()
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total", stats['total'])
        
        with col2:
            st.metric("Scheduled", stats['scheduled'])
        
        with col3:
            st.metric("Confirmed", stats['confirmed'])
        
        with col4:
            st.metric("Upcoming", stats['upcoming'])
        
        with col5:
            st.metric("Today", stats['today'])
        
        with col6:
            st.metric("Completed", stats['completed'])
        
        # Additional row for cancelled and no-show
        col7, col8 = st.columns(2)
        with col7:
            st.metric("Cancelled", stats['cancelled'])
        with col8:
            st.metric("No-Show", stats['no_show'])
    
    except Exception as e:
        st.error(f"❌ Error loading statistics: {e}")


def display_appointments_table(service: AppointmentService, patient_service: PatientService, 
                               doctor_service: DoctorService, specialization_service: SpecializationService,
                               search_query: str = "", status_filter: str = "All", date_filter: str = "All"):
    """Display appointments in a table with selection"""
    try:
        import pandas as pd
        
        # Build filters
        filters = {}
        if status_filter != "All":
            filters['status'] = status_filter
        
        if date_filter == "Today":
            filters['start_date'] = date.today()
            filters['end_date'] = date.today()
        elif date_filter == "Upcoming":
            filters['upcoming_only'] = True
        elif date_filter == "Past":
            # We'll filter in Python after fetching
            pass
        
        # Get appointments
        appointments = service.get_all_appointments(filters if filters else None)
        
        # Filter for past if needed
        if date_filter == "Past":
            appointments = [a for a in appointments if a.is_past]
        
        # Apply search filter
        if search_query:
            filtered_appointments = []
            search_lower = search_query.lower()
            for apt in appointments:
                # Get patient and doctor names
                patient = patient_service.get_patient(apt.patient_id)
                doctor = doctor_service.get_doctor(apt.doctor_id)
                
                patient_name = patient.full_name.lower() if patient else ""
                doctor_name = doctor.full_name.lower() if doctor else ""
                reason = (apt.reason or "").lower()
                
                if (search_lower in patient_name or 
                    search_lower in doctor_name or 
                    search_lower in reason):
                    filtered_appointments.append(apt)
            appointments = filtered_appointments
        
        if not appointments:
            st.info("📭 No appointments found.")
            return
        
        # Prepare data for table
        data = []
        for apt in appointments:
            patient = patient_service.get_patient(apt.patient_id)
            doctor = doctor_service.get_doctor(apt.doctor_id)
            specialization = specialization_service.get_specialization(apt.specialization_id)
            
            data.append({
                'ID': apt.appointment_id,
                'Date': apt.appointment_date.strftime('%Y-%m-%d') if apt.appointment_date else 'N/A',
                'Time': apt.appointment_time.strftime('%H:%M') if apt.appointment_time else 'N/A',
                'Patient': patient.full_name if patient else f"ID: {apt.patient_id}",
                'Doctor': doctor.display_name if doctor else f"ID: {apt.doctor_id}",
                'Specialization': specialization.name if specialization else 'N/A',
                'Type': apt.appointment_type,
                'Status': apt.status,
                'Duration': f"{apt.duration} min"
            })
        
        df = pd.DataFrame(data)
        
        # Add a selection checkbox column
        if 'appointment_selection_state' not in st.session_state:
            st.session_state.appointment_selection_state = {}
        
        df['Select'] = [st.session_state.appointment_selection_state.get(apt.appointment_id, False) for apt in appointments]
        
        # Reorder columns to show Select first
        column_order = ['Select', 'ID', 'Date', 'Time', 'Patient', 'Doctor', 'Specialization', 'Type', 'Status', 'Duration']
        df = df[column_order]
        
        st.subheader("📋 Appointment List - Click the checkbox in a row to select it")
        
        # Display interactive table with selection column
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select", width="small", help="Check to select this row"),
                "ID": st.column_config.NumberColumn("ID", width="small", disabled=True),
                "Date": st.column_config.TextColumn("Date", width="small", disabled=True),
                "Time": st.column_config.TextColumn("Time", width="small", disabled=True),
                "Patient": st.column_config.TextColumn("Patient", width="medium", disabled=True),
                "Doctor": st.column_config.TextColumn("Doctor", width="medium", disabled=True),
                "Specialization": st.column_config.TextColumn("Specialization", width="medium", disabled=True),
                "Type": st.column_config.TextColumn("Type", width="small", disabled=True),
                "Status": st.column_config.TextColumn("Status", width="small", disabled=True),
                "Duration": st.column_config.TextColumn("Duration", width="small", disabled=True)
            },
            key="appointments_table_editor",
            num_rows="fixed"
        )
        
        # Find selected row(s) - only one should be selected
        selected_rows: pd.DataFrame = edited_df[edited_df['Select'] == True]  # type: ignore
        
        if len(selected_rows) > 0:
            selected_row = selected_rows.iloc[0]
            selected_id = int(selected_row['ID'])
            st.session_state.selected_appointment_id = selected_id
            
            # Update selection state - uncheck all others
            for idx, apt in enumerate(appointments):
                if apt.appointment_id == selected_id:
                    st.session_state.appointment_selection_state[apt.appointment_id] = True
                else:
                    st.session_state.appointment_selection_state[apt.appointment_id] = False
            
            st.success(f"✅ Selected: Appointment ID {selected_id} - Click Edit/Cancel button above to proceed")
        else:
            # No row selected - clear selection state
            st.session_state.selected_appointment_id = None
            for apt in appointments:
                st.session_state.appointment_selection_state[apt.appointment_id] = False
        
        st.caption(f"Showing {len(appointments)} appointment(s) - Check a row's checkbox to select it, then click Edit/Cancel button")
    
    except Exception as e:
        st.error(f"❌ Error loading appointments: {e}")


def show_add_appointment_dialog(appointment_service: AppointmentService, patient_service: PatientService,
                                doctor_service: DoctorService, specialization_service: SpecializationService):
    """Show add appointment dialog"""
    st.subheader("➕ Schedule New Appointment")
    st.markdown("---")
    
    with st.form("add_appointment_form", clear_on_submit=True):
        # Get all patients, doctors, and specializations
        all_patients = patient_service.get_all_patients()
        patients = [p for p in all_patients if p.status == 1]  # Filter active patients (status 1 = Active)
        doctors = doctor_service.get_all_doctors(active_only=True)
        specializations = specialization_service.get_all_specializations(active_only=True)
        
        if not patients:
            st.error("❌ No active patients found. Please add patients first.")
            if st.form_submit_button("❌ Cancel"):
                st.session_state.show_add_appointment = False
                st.rerun()
            return
        
        if not doctors:
            st.error("❌ No active doctors found. Please add doctors first.")
            if st.form_submit_button("❌ Cancel"):
                st.session_state.show_add_appointment = False
                st.rerun()
            return
        
        if not specializations:
            st.error("❌ No active specializations found. Please add specializations first.")
            if st.form_submit_button("❌ Cancel"):
                st.session_state.show_add_appointment = False
                st.rerun()
            return
        
        # Patient selection
        patient_options = {f"{p.full_name} (ID: {p.patient_id})": p.patient_id for p in patients}
        selected_patient = st.selectbox("👤 Patient *", list(patient_options.keys()))
        patient_id = patient_options[selected_patient]
        
        # Doctor selection
        doctor_options = {f"{d.display_name} (ID: {d.doctor_id})": d.doctor_id for d in doctors}
        selected_doctor = st.selectbox("👨‍⚕️ Doctor *", list(doctor_options.keys()))
        doctor_id = doctor_options[selected_doctor]
        
        # Specialization selection
        spec_options = {f"{s.name}": s.specialization_id for s in specializations}
        selected_spec = st.selectbox("🏥 Specialization *", list(spec_options.keys()))
        specialization_id = spec_options[selected_spec]
        
        # Date and time
        col1, col2 = st.columns(2)
        with col1:
            appointment_date = st.date_input("📅 Appointment Date *", min_value=date.today())
        with col2:
            appointment_time = st.time_input("🕐 Appointment Time *", value=time(9, 0))
        
        # Duration and type
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("⏱️ Duration (minutes) *", min_value=15, max_value=240, value=30, step=15)
        with col2:
            appointment_type = st.selectbox("📋 Appointment Type *", ["Regular", "Follow-up", "Emergency"])
        
        # Reason and notes
        reason = st.text_area("📝 Reason for Visit", placeholder="Enter the reason for this appointment...")
        notes = st.text_area("📄 Additional Notes", placeholder="Any additional notes or information...")
        
        # Status
        status = st.selectbox("📊 Status", ["Scheduled", "Confirmed"], index=0)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Schedule Appointment", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            try:
                # Check for conflicts
                conflicts = appointment_service.check_conflicts(doctor_id, appointment_date, appointment_time, duration)
                if conflicts:
                    st.error(f"❌ Time slot conflicts with existing appointment(s). Please choose a different time.")
                else:
                    appointment_data = {
                        'patient_id': patient_id,
                        'doctor_id': doctor_id,
                        'specialization_id': specialization_id,
                        'appointment_date': appointment_date.isoformat(),
                        'appointment_time': appointment_time.strftime('%H:%M:%S'),
                        'duration': duration,
                        'appointment_type': appointment_type,
                        'reason': reason if reason else None,
                        'notes': notes if notes else None,
                        'status': status
                    }
                    
                    appointment_id = appointment_service.create_appointment(appointment_data)
                    st.success(f"✅ Appointment scheduled successfully! (ID: {appointment_id})")
                    st.session_state.show_add_appointment = False
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to schedule appointment: {e}")
        
        if cancel:
            st.session_state.show_add_appointment = False
            st.rerun()


def show_edit_appointment_dialog(appointment_service: AppointmentService, patient_service: PatientService,
                                 doctor_service: DoctorService, specialization_service: SpecializationService):
    """Show edit appointment dialog"""
    st.subheader("✏️ Edit Appointment")
    st.markdown("---")
    
    appointment_id = st.session_state.get('edit_appointment_id')
    
    if not appointment_id:
        st.error("❌ No appointment selected. Please select an appointment from the table.")
        if st.button("❌ Close"):
            st.session_state.show_edit_appointment = False
            st.rerun()
        return
    
    appointment = appointment_service.get_appointment(appointment_id)
    
    if not appointment:
        st.error("❌ Appointment not found!")
        if st.button("❌ Close"):
            st.session_state.show_edit_appointment = False
            st.rerun()
        return
    
    with st.form("edit_appointment_form"):
        # Get all patients, doctors, and specializations
        all_patients = patient_service.get_all_patients()
        patients = [p for p in all_patients if p.status == 1]  # Filter active patients (status 1 = Active)
        doctors = doctor_service.get_all_doctors(active_only=True)
        specializations = specialization_service.get_all_specializations(active_only=True)
        
        # Patient selection
        patient_options = {f"{p.full_name} (ID: {p.patient_id})": p.patient_id for p in patients}
        current_patient = next((p for p in patients if p.patient_id == appointment.patient_id), None)
        current_patient_key = f"{current_patient.full_name} (ID: {current_patient.patient_id})" if current_patient else list(patient_options.keys())[0]
        selected_patient = st.selectbox("👤 Patient *", list(patient_options.keys()), index=list(patient_options.keys()).index(current_patient_key) if current_patient_key in patient_options else 0)
        patient_id = patient_options[selected_patient]
        
        # Doctor selection
        doctor_options = {f"{d.display_name} (ID: {d.doctor_id})": d.doctor_id for d in doctors}
        current_doctor = next((d for d in doctors if d.doctor_id == appointment.doctor_id), None)
        current_doctor_key = f"{current_doctor.display_name} (ID: {current_doctor.doctor_id})" if current_doctor else list(doctor_options.keys())[0]
        selected_doctor = st.selectbox("👨‍⚕️ Doctor *", list(doctor_options.keys()), index=list(doctor_options.keys()).index(current_doctor_key) if current_doctor_key in doctor_options else 0)
        doctor_id = doctor_options[selected_doctor]
        
        # Specialization selection
        spec_options = {f"{s.name}": s.specialization_id for s in specializations}
        current_spec = next((s for s in specializations if s.specialization_id == appointment.specialization_id), None)
        current_spec_key = current_spec.name if current_spec else list(spec_options.keys())[0]
        selected_spec = st.selectbox("🏥 Specialization *", list(spec_options.keys()), index=list(spec_options.keys()).index(current_spec_key) if current_spec_key in spec_options else 0)
        specialization_id = spec_options[selected_spec]
        
        # Date and time
        col1, col2 = st.columns(2)
        with col1:
            appointment_date = st.date_input("📅 Appointment Date *", value=appointment.appointment_date if appointment.appointment_date else date.today(), min_value=date.today())
        with col2:
            appointment_time = st.time_input("🕐 Appointment Time *", value=appointment.appointment_time if appointment.appointment_time else time(9, 0))
        
        # Duration and type
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("⏱️ Duration (minutes) *", min_value=15, max_value=240, value=appointment.duration, step=15)
        with col2:
            appointment_type = st.selectbox("📋 Appointment Type *", ["Regular", "Follow-up", "Emergency"], index=["Regular", "Follow-up", "Emergency"].index(appointment.appointment_type) if appointment.appointment_type in ["Regular", "Follow-up", "Emergency"] else 0)
        
        # Reason and notes
        reason = st.text_area("📝 Reason for Visit", value=appointment.reason or "", placeholder="Enter the reason for this appointment...")
        notes = st.text_area("📄 Additional Notes", value=appointment.notes or "", placeholder="Any additional notes or information...")
        
        # Status
        status_options = ["Scheduled", "Confirmed", "Cancelled", "Completed", "No-Show"]
        status = st.selectbox("📊 Status", status_options, index=status_options.index(appointment.status) if appointment.status in status_options else 0)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Update Appointment", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            try:
                appointment_data = {
                    'patient_id': patient_id,
                    'doctor_id': doctor_id,
                    'specialization_id': specialization_id,
                    'appointment_date': appointment_date.isoformat(),
                    'appointment_time': appointment_time.strftime('%H:%M:%S'),
                    'duration': duration,
                    'appointment_type': appointment_type,
                    'reason': reason if reason else None,
                    'notes': notes if notes else None,
                    'status': status
                }
                
                success = appointment_service.update_appointment(appointment_id, appointment_data)
                if success:
                    st.success(f"✅ Appointment updated successfully!")
                    st.session_state.show_edit_appointment = False
                    st.session_state.edit_appointment_id = None
                    st.rerun()
                else:
                    st.error("❌ Failed to update appointment.")
            except Exception as e:
                st.error(f"❌ Failed to update appointment: {e}")
        
        if cancel:
            st.session_state.show_edit_appointment = False
            st.session_state.edit_appointment_id = None
            st.rerun()


def show_complete_appointment_dialog(appointment_service: AppointmentService):
    """Show mark appointment as complete dialog"""
    st.subheader("✅ Mark Appointment as Complete")
    st.markdown("---")
    
    appointment_id = st.session_state.get('complete_appointment_id')
    
    if not appointment_id:
        st.error("❌ No appointment selected. Please select an appointment from the table.")
        if st.button("❌ Close"):
            st.session_state.show_complete_appointment = False
            st.rerun()
        return
    
    appointment = appointment_service.get_appointment(appointment_id)
    
    if not appointment:
        st.error("❌ Appointment not found!")
        if st.button("❌ Close"):
            st.session_state.show_complete_appointment = False
            st.rerun()
        return
    
    # Check if appointment is already completed
    if appointment.status == 'Completed':
        st.warning("⚠️ This appointment is already marked as completed.")
        if st.button("❌ Close"):
            st.session_state.show_complete_appointment = False
            st.rerun()
        return
    
    # Show appointment details
    st.info(f"""
    **Appointment Details:**
    - **ID:** {appointment.appointment_id}
    - **Date:** {appointment.appointment_date.strftime('%Y-%m-%d') if appointment.appointment_date else 'N/A'}
    - **Time:** {appointment.appointment_time.strftime('%H:%M') if appointment.appointment_time else 'N/A'}
    - **Current Status:** {appointment.status}
    """)
    
    with st.form("complete_appointment_form"):
        notes = st.text_area("📝 Completion Notes (Optional)", placeholder="Add any notes about the appointment completion...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Mark as Complete", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            try:
                # Update appointment status to Completed
                appointment_data = {
                    'status': 'Completed'
                }
                # Add notes if provided
                if notes:
                    current_notes = appointment.notes or ""
                    if current_notes:
                        appointment_data['notes'] = f"{current_notes}\n[Completed] {notes}"
                    else:
                        appointment_data['notes'] = f"[Completed] {notes}"
                
                success = appointment_service.update_appointment(appointment_id, appointment_data)
                if success:
                    st.success("✅ Appointment marked as completed successfully!")
                    st.session_state.show_complete_appointment = False
                    st.session_state.complete_appointment_id = None
                    st.rerun()
                else:
                    st.error("❌ Failed to mark appointment as complete.")
            except Exception as e:
                st.error(f"❌ Failed to mark appointment as complete: {e}")
        
        if cancel:
            st.session_state.show_complete_appointment = False
            st.session_state.complete_appointment_id = None
            st.rerun()


def show_cancel_appointment_dialog(appointment_service: AppointmentService):
    """Show cancel appointment dialog"""
    st.subheader("❌ Cancel Appointment")
    st.markdown("---")
    
    appointment_id = st.session_state.get('cancel_appointment_id')
    
    if not appointment_id:
        st.error("❌ No appointment selected. Please select an appointment from the table.")
        if st.button("❌ Close"):
            st.session_state.show_cancel_appointment = False
            st.rerun()
        return
    
    appointment = appointment_service.get_appointment(appointment_id)
    
    if not appointment:
        st.error("❌ Appointment not found!")
        if st.button("❌ Close"):
            st.session_state.show_cancel_appointment = False
            st.rerun()
        return
    
    # Show appointment details
    st.info(f"""
    **Appointment Details:**
    - **ID:** {appointment.appointment_id}
    - **Date:** {appointment.appointment_date.strftime('%Y-%m-%d') if appointment.appointment_date else 'N/A'}
    - **Time:** {appointment.appointment_time.strftime('%H:%M') if appointment.appointment_time else 'N/A'}
    - **Status:** {appointment.status}
    """)
    
    with st.form("cancel_appointment_form"):
        cancellation_reason = st.text_area("📝 Cancellation Reason", placeholder="Enter the reason for cancellation...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Confirm Cancellation", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit:
            try:
                success = appointment_service.cancel_appointment(appointment_id, cancellation_reason if cancellation_reason else None)
                if success:
                    st.success("✅ Appointment cancelled successfully!")
                    st.session_state.show_cancel_appointment = False
                    st.session_state.cancel_appointment_id = None
                    st.rerun()
                else:
                    st.error("❌ Failed to cancel appointment.")
            except Exception as e:
                st.error(f"❌ Failed to cancel appointment: {e}")
        
        if cancel:
            st.session_state.show_cancel_appointment = False
            st.session_state.cancel_appointment_id = None
            st.rerun()


def show_reports_analytics():
    """Dashboard page (Reports & Analytics)"""
    st.title("📊 Dashboard")
    st.markdown("---")
    
    report_service = st.session_state.report_service
    
    # Dashboard Summary
    st.subheader("📈 Reports & Analytics Summary")
    dashboard_summary = report_service.get_dashboard_summary()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Patients", dashboard_summary['total_patients'])
    with col2:
        st.metric("Total Doctors", dashboard_summary['total_doctors'])
    with col3:
        st.metric("Active Queue", dashboard_summary['active_queue'])
    with col4:
        st.metric("Total Appointments", dashboard_summary['total_appointments'])
    with col5:
        st.metric("Upcoming", dashboard_summary['upcoming_appointments'])
    
    st.markdown("---")
    
    # Report Type Selection - Allow multiple selections
    selected_reports = st.multiselect(
        "📋 Select Report Types (Select multiple to view all at once)",
        ["Patient Statistics", "Queue Analytics", "Appointment Reports", 
         "Doctor Performance", "Specialization Utilization", "Custom Report"],
        default=["Patient Statistics", "Appointment Reports"],
        key="report_types"
    )
    
    # Date Range Selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("📅 Start Date", value=date.today() - timedelta(days=30), key="report_start_date")
    with col2:
        end_date = st.date_input("📅 End Date", value=date.today(), key="report_end_date")
    
    date_range = (start_date, end_date)
    
    st.markdown("---")
    
    # Generate and display reports based on selection (can show multiple)
    if not selected_reports:
        st.info("👆 Please select at least one report type to view analytics.")
    else:
        # Show all selected reports
        for report_type in selected_reports:
            if report_type == "Patient Statistics":
                show_patient_reports(report_service, date_range)
                st.markdown("---")
            elif report_type == "Queue Analytics":
                show_queue_reports(report_service, date_range)
                st.markdown("---")
            elif report_type == "Appointment Reports":
                show_appointment_reports(report_service, date_range)
                st.markdown("---")
            elif report_type == "Doctor Performance":
                show_doctor_reports(report_service, date_range)
                st.markdown("---")
            elif report_type == "Specialization Utilization":
                show_specialization_reports(report_service)
                st.markdown("---")
            elif report_type == "Custom Report":
                show_custom_report(report_service, date_range)
                st.markdown("---")


def show_patient_reports(report_service: ReportService, date_range: tuple):
    """Display patient statistics reports"""
    st.subheader("👥 Patient Statistics Report")
    
    stats = report_service.get_patient_statistics(date_range)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", stats['total'])
    with col2:
        st.metric("New Today", stats['new_today'])
    with col3:
        st.metric("New This Week", stats['new_this_week'])
    with col4:
        st.metric("New This Month", stats['new_this_month'])
    
    st.markdown("---")
    
    # Status Distribution Chart
    st.subheader("📊 Status Distribution")
    status_data = {
        'Normal': stats['status_distribution'].get(0, 0),
        'Urgent': stats['status_distribution'].get(1, 0),
        'Super-Urgent': stats['status_distribution'].get(2, 0)
    }
    st.bar_chart(status_data)
    
    # Gender Distribution
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👤 Gender Distribution")
        st.bar_chart(stats['gender_distribution'])
    
    with col2:
        st.subheader("🎂 Age Groups")
        st.bar_chart(stats['age_groups'])


def show_queue_reports(report_service: ReportService, date_range: tuple):
    """Display queue analytics reports"""
    st.subheader("📋 Queue Analytics Report")
    
    stats = report_service.get_queue_statistics(date_range=date_range)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Queue", stats['total_active'])
    with col2:
        st.metric("Average Wait Time", f"{stats['average_wait_time_minutes']:.1f} min")
    with col3:
        st.metric("Patients Served", stats['served_count'])
    
    st.markdown("---")
    
    # Priority Distribution
    st.subheader("🚨 Priority Distribution")
    priority_data = {
        'Normal': stats['priority_distribution'].get(0, 0),
        'Urgent': stats['priority_distribution'].get(1, 0),
        'Super-Urgent': stats['priority_distribution'].get(2, 0)
    }
    st.bar_chart(priority_data)
    
    # Specialization Breakdown
    if stats['specialization_breakdown']:
        st.subheader("🏥 Queue by Specialization")
        spec_service = st.session_state.specialization_service
        spec_data = {}
        for spec_id, count in stats['specialization_breakdown'].items():
            spec = spec_service.get_specialization(spec_id)
            if spec:
                spec_data[spec.name] = count
        if spec_data:
            st.bar_chart(spec_data)


def show_appointment_reports(report_service: ReportService, date_range: tuple):
    """Display appointment reports"""
    st.subheader("📅 Appointment Reports")
    
    stats = report_service.get_appointment_statistics(date_range)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total", stats['total'])
    with col2:
        st.metric("Scheduled", stats['status_distribution']['Scheduled'])
    with col3:
        st.metric("Completed", stats['status_distribution']['Completed'])
    with col4:
        st.metric("Cancelled", stats['status_distribution']['Cancelled'])
    with col5:
        st.metric("No-Show", stats['status_distribution']['No-Show'])
    
    st.markdown("---")
    
    # Rates
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completion Rate", f"{stats['completion_rate']:.1f}%")
    with col2:
        st.metric("Cancellation Rate", f"{stats['cancellation_rate']:.1f}%")
    with col3:
        st.metric("No-Show Rate", f"{stats['no_show_rate']:.1f}%")
    
    st.markdown("---")
    
    # Status Distribution
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Status Distribution")
        st.bar_chart(stats['status_distribution'])
    
    with col2:
        st.subheader("📋 Type Distribution")
        st.bar_chart(stats['type_distribution'])
    
    # Doctor Distribution
    if stats['doctor_distribution']:
        st.subheader("👨‍⚕️ Appointments by Doctor")
        doctor_service = st.session_state.doctor_service
        doctor_data = {}
        for doctor_id, count in list(stats['doctor_distribution'].items())[:10]:  # Top 10
            doctor = doctor_service.get_doctor(doctor_id)
            if doctor:
                doctor_data[doctor.display_name] = count
        if doctor_data:
            st.bar_chart(doctor_data)


def show_doctor_reports(report_service: ReportService, date_range: tuple):
    """Display doctor performance reports"""
    st.subheader("👨‍⚕️ Doctor Performance Report")
    
    stats = report_service.get_doctor_statistics(date_range=date_range)
    
    st.metric("Total Doctors", stats['total_doctors'])
    st.metric("Active Doctors", stats['active_doctors'])
    
    st.markdown("---")
    
    # Doctor Performance Table
    if stats['doctors']:
        import pandas as pd
        
        df_data = []
        for doc_stat in stats['doctors']:
            df_data.append({
                'Doctor': doc_stat['doctor_name'],
                'Total Appointments': doc_stat['total_appointments'],
                'Completed': doc_stat['completed_appointments'],
                'Cancelled': doc_stat['cancelled_appointments'],
                'Specializations': doc_stat['specialization_count'],
                'Status': doc_stat['status']
            })
        
        df = pd.DataFrame(df_data)
        df = df.sort_values('Total Appointments', ascending=False)
        
        st.subheader("📊 Doctor Performance Summary")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Top Doctors Chart
        if len(df) > 0:
            st.subheader("🏆 Top Doctors by Appointments")
            top_doctors = df.head(10)
            chart_data = top_doctors.set_index('Doctor')['Total Appointments']
            st.bar_chart(chart_data)


def show_specialization_reports(report_service: ReportService):
    """Display specialization utilization reports"""
    st.subheader("🏥 Specialization Utilization Report")
    
    stats = report_service.get_specialization_statistics()
    
    st.metric("Total Specializations", stats['total_specializations'])
    st.metric("Active Specializations", stats['active_specializations'])
    
    st.markdown("---")
    
    # Specialization Utilization Table
    if stats['specializations']:
        import pandas as pd
        
        df_data = []
        for spec_stat in stats['specializations']:
            df_data.append({
                'Specialization': spec_stat['specialization_name'],
                'Current Queue': spec_stat['current_queue_size'],
                'Max Capacity': spec_stat['max_capacity'],
                'Utilization %': f"{spec_stat['utilization_percentage']:.1f}%",
                'Total Appointments': spec_stat['total_appointments'],
                'Assigned Doctors': spec_stat['assigned_doctors'],
                'Status': 'Active' if spec_stat['is_active'] else 'Inactive'
            })
        
        df = pd.DataFrame(df_data)
        # Sort by utilization percentage (convert string to float for sorting)
        df['Utilization_Num'] = df['Utilization %'].str.rstrip('%').astype('float')
        df = df.sort_values('Utilization_Num', ascending=False)
        df = df.drop('Utilization_Num', axis=1)
        
        st.subheader("📊 Specialization Utilization Summary")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Utilization Chart
        if len(df) > 0:
            st.subheader("📈 Utilization by Specialization")
            chart_data = df.set_index('Specialization')['Current Queue']
            st.bar_chart(chart_data)


def show_custom_report(report_service: ReportService, date_range: tuple):
    """Display custom report builder"""
    st.subheader("🔧 Custom Report Builder")
    
    st.info("Select metrics and filters to generate a custom report with visualizations.")
    
    # Metric Selection
    selected_metrics = st.multiselect(
        "📊 Select Metrics",
        ["Patient Statistics", "Queue Statistics", "Appointment Statistics", 
         "Doctor Statistics", "Specialization Statistics"],
        default=["Patient Statistics", "Appointment Statistics"]
    )
    
    if st.button("🔍 Generate Custom Report", type="primary"):
        st.markdown("---")
        
        if "Patient Statistics" in selected_metrics:
            st.subheader("👥 Patient Statistics")
            patient_stats = report_service.get_patient_statistics(date_range)
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Patients", patient_stats['total'])
            with col2:
                st.metric("New Today", patient_stats['new_today'])
            with col3:
                st.metric("New This Week", patient_stats['new_this_week'])
            with col4:
                st.metric("New This Month", patient_stats['new_this_month'])
            
            # Charts
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Status Distribution**")
                status_data = {
                    'Normal': patient_stats['status_distribution'].get(0, 0),
                    'Urgent': patient_stats['status_distribution'].get(1, 0),
                    'Super-Urgent': patient_stats['status_distribution'].get(2, 0)
                }
                st.bar_chart(status_data)
            
            with col2:
                st.markdown("**Gender Distribution**")
                st.bar_chart(patient_stats['gender_distribution'])
            
            st.markdown("**Age Groups**")
            st.bar_chart(patient_stats['age_groups'])
            
            st.markdown("---")
        
        if "Queue Statistics" in selected_metrics:
            st.subheader("📋 Queue Statistics")
            queue_stats = report_service.get_queue_statistics(date_range=date_range)
            
            # Key Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Queue", queue_stats['total_active'])
            with col2:
                st.metric("Average Wait Time", f"{queue_stats['average_wait_time_minutes']:.1f} min")
            with col3:
                st.metric("Patients Served", queue_stats['served_count'])
            
            # Priority Distribution
            st.markdown("**Priority Distribution**")
            priority_data = {
                'Normal': queue_stats['priority_distribution'].get(0, 0),
                'Urgent': queue_stats['priority_distribution'].get(1, 0),
                'Super-Urgent': queue_stats['priority_distribution'].get(2, 0)
            }
            st.bar_chart(priority_data)
            
            # Specialization Breakdown
            if queue_stats['specialization_breakdown']:
                st.markdown("**Queue by Specialization**")
                spec_service = st.session_state.specialization_service
                spec_data = {}
                for spec_id, count in queue_stats['specialization_breakdown'].items():
                    spec = spec_service.get_specialization(spec_id)
                    if spec:
                        spec_data[spec.name] = count
                if spec_data:
                    st.bar_chart(spec_data)
            
            st.markdown("---")
        
        if "Appointment Statistics" in selected_metrics:
            st.subheader("📅 Appointment Statistics")
            appointment_stats = report_service.get_appointment_statistics(date_range)
            
            # Key Metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total", appointment_stats['total'])
            with col2:
                st.metric("Scheduled", appointment_stats['status_distribution']['Scheduled'])
            with col3:
                st.metric("Completed", appointment_stats['status_distribution']['Completed'])
            with col4:
                st.metric("Cancelled", appointment_stats['status_distribution']['Cancelled'])
            with col5:
                st.metric("No-Show", appointment_stats['status_distribution']['No-Show'])
            
            # Rates
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Completion Rate", f"{appointment_stats['completion_rate']:.1f}%")
            with col2:
                st.metric("Cancellation Rate", f"{appointment_stats['cancellation_rate']:.1f}%")
            with col3:
                st.metric("No-Show Rate", f"{appointment_stats['no_show_rate']:.1f}%")
            
            # Charts
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Status Distribution**")
                st.bar_chart(appointment_stats['status_distribution'])
            
            with col2:
                st.markdown("**Type Distribution**")
                st.bar_chart(appointment_stats['type_distribution'])
            
            # Doctor Distribution
            if appointment_stats['doctor_distribution']:
                st.markdown("**Appointments by Doctor (Top 10)**")
                doctor_service = st.session_state.doctor_service
                doctor_data = {}
                for doctor_id, count in list(appointment_stats['doctor_distribution'].items())[:10]:
                    doctor = doctor_service.get_doctor(doctor_id)
                    if doctor:
                        doctor_data[doctor.display_name] = count
                if doctor_data:
                    st.bar_chart(doctor_data)
            
            st.markdown("---")
        
        if "Doctor Statistics" in selected_metrics:
            st.subheader("👨‍⚕️ Doctor Statistics")
            doctor_stats = report_service.get_doctor_statistics(date_range=date_range)
            
            st.metric("Total Doctors", doctor_stats['total_doctors'])
            st.metric("Active Doctors", doctor_stats['active_doctors'])
            
            # Doctor Performance Table
            if doctor_stats['doctors']:
                import pandas as pd
                
                df_data = []
                for doc_stat in doctor_stats['doctors']:
                    df_data.append({
                        'Doctor': doc_stat['doctor_name'],
                        'Total Appointments': doc_stat['total_appointments'],
                        'Completed': doc_stat['completed_appointments'],
                        'Cancelled': doc_stat['cancelled_appointments'],
                        'Specializations': doc_stat['specialization_count'],
                        'Status': doc_stat['status']
                    })
                
                df = pd.DataFrame(df_data)
                df = df.sort_values('Total Appointments', ascending=False)
                
                st.markdown("**Doctor Performance Summary**")
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Top Doctors Chart
                if len(df) > 0:
                    st.markdown("**Top Doctors by Appointments**")
                    top_doctors = df.head(10)
                    chart_data = top_doctors.set_index('Doctor')['Total Appointments']
                    st.bar_chart(chart_data)
            
            st.markdown("---")
        
        if "Specialization Statistics" in selected_metrics:
            st.subheader("🏥 Specialization Statistics")
            spec_stats = report_service.get_specialization_statistics()
            
            st.metric("Total Specializations", spec_stats['total_specializations'])
            st.metric("Active Specializations", spec_stats['active_specializations'])
            
            # Specialization Utilization Table
            if spec_stats['specializations']:
                import pandas as pd
                
                df_data = []
                for spec_stat in spec_stats['specializations']:
                    df_data.append({
                        'Specialization': spec_stat['specialization_name'],
                        'Current Queue': spec_stat['current_queue_size'],
                        'Max Capacity': spec_stat['max_capacity'],
                        'Utilization %': f"{spec_stat['utilization_percentage']:.1f}%",
                        'Total Appointments': spec_stat['total_appointments'],
                        'Assigned Doctors': spec_stat['assigned_doctors'],
                        'Status': 'Active' if spec_stat['is_active'] else 'Inactive'
                    })
                
                df = pd.DataFrame(df_data)
                df['Utilization_Num'] = df['Utilization %'].str.rstrip('%').astype('float')
                df = df.sort_values('Utilization_Num', ascending=False)
                df = df.drop('Utilization_Num', axis=1)
                
                st.markdown("**Specialization Utilization Summary**")
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Utilization Chart
                if len(df) > 0:
                    st.markdown("**Utilization by Specialization**")
                    chart_data = df.set_index('Specialization')['Current Queue']
                    st.bar_chart(chart_data)
            
            st.markdown("---")
        
        st.success("✅ Custom report generated successfully!")


def show_placeholder(page_name: str):
    """Show placeholder for unimplemented pages"""
    st.title(f"📋 {page_name}")
    st.markdown("---")
    st.info(f"🚧 **{page_name}** feature is coming soon!")
    st.markdown("""
    This feature will be implemented in future updates.
    
    **Planned features:**
    - Full queue management system
    - Doctor scheduling
    - Appointment booking
    - Comprehensive reporting and analytics
    """)


if __name__ == "__main__":
    main()
