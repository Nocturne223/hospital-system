"""
Hospital Management System - Streamlit Application
Main entry point for the web-based GUI
"""

import streamlit as st
import sys
import os
from datetime import date, datetime

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
    
    # Sidebar navigation
    st.sidebar.title("🏥 Hospital Management")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Patient Management", "Specialization Management", "Queue Management", 
         "Doctor Management", "Appointments", "Reports & Analytics"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("**System Status:** ✅ Connected")
    
    # Main content area
    if page == "Patient Management":
        show_patient_management()
    elif page == "Specialization Management":
        show_specialization_management()
    elif page == "Queue Management":
        show_queue_management()
    elif page == "Doctor Management":
        show_placeholder("Doctor Management")
    elif page == "Appointments":
        show_placeholder("Appointments")
    elif page == "Reports & Analytics":
        show_placeholder("Reports & Analytics")


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
        selected_rows = edited_df[edited_df['Select'] == True]
        
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
            selected_rows = edited_df[edited_df['Select'] == True]
            
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
        selected_rows = edited_df[edited_df['Select'] == True]
        
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
        selected_rows = edited_df[edited_df['Select'] == True]
        
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
