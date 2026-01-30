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
        show_placeholder("Queue Management")
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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add New Patient", use_container_width=True, type="primary"):
            st.session_state.show_add_patient = True
            st.rerun()
    
    with col2:
        if st.button("✏️ Edit Patient", use_container_width=True):
            st.session_state.show_edit_patient = True
            st.rerun()
    
    with col3:
        if st.button("🗑️ Delete Patient", use_container_width=True):
            st.session_state.show_delete_patient = True
            st.rerun()
    
    with col4:
        if st.button("📊 View Statistics", use_container_width=True):
            st.session_state.show_stats = True
            st.rerun()
    
    st.markdown("---")
    
    # Handle modals/dialogs
    if st.session_state.get('show_add_patient', False):
        show_add_patient_dialog(service)
    
    if st.session_state.get('show_edit_patient', False):
        show_edit_patient_dialog(service)
    
    if st.session_state.get('show_delete_patient', False):
        show_delete_patient_dialog(service)
    
    if st.session_state.get('show_stats', False):
        show_patient_statistics(service)
    
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
    
    # Get patient ID
    patient_id = st.number_input(
        "Enter Patient ID to Edit",
        min_value=1,
        step=1,
        key="edit_patient_id"
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
        except Exception as e:
            st.error(f"❌ Error loading patient: {e}")
    
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
    
    patient_id = st.number_input(
        "Enter Patient ID to Delete",
        min_value=1,
        step=1,
        key="delete_patient_id"
    )
    
    if st.button("Load Patient", use_container_width=True):
        try:
            patient = service.get_patient(patient_id)
            if patient:
                st.session_state.delete_patient_data = patient.to_dict()
                st.session_state.delete_patient_loaded = True
            else:
                st.error("❌ Patient not found!")
        except Exception as e:
            st.error(f"❌ Error loading patient: {e}")
    
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


def show_patient_statistics(service: PatientService):
    """Show patient statistics"""
    st.subheader("📊 Patient Statistics")
    
    try:
        all_patients = service.get_all_patients()
        
        if not all_patients:
            st.info("No patients in the database.")
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
        
        st.markdown("---")
        
        if st.button("Close Statistics"):
            st.session_state.show_stats = False
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error loading statistics: {e}")
    
    st.markdown("---")


def display_patients_table(service: PatientService, search_query: str = "", status_filter: str = "All"):
    """Display patients in a table"""
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
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        st.caption(f"Showing {len(patients)} patient(s)")
    
    except Exception as e:
        st.error(f"❌ Error loading patients: {e}")


def show_specialization_management():
    """Specialization Management page"""
    st.title("🏥 Specialization Management")
    st.markdown("---")
    
    service = st.session_state.specialization_service
    
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
            st.session_state.show_edit_specialization = True
            st.rerun()
    
    with col3:
        if st.button("🗑️ Delete Specialization", use_container_width=True):
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
    
    # Get specialization ID
    specialization_id = st.number_input(
        "Enter Specialization ID to Edit",
        min_value=1,
        step=1,
        key="edit_specialization_id"
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
        except Exception as e:
            st.error(f"❌ Error loading specialization: {e}")
    
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
    
    specialization_id = st.number_input(
        "Enter Specialization ID to Delete",
        min_value=1,
        step=1,
        key="delete_specialization_id"
    )
    
    if st.button("🗑️ Delete Specialization", use_container_width=True, type="primary"):
        try:
            specialization = service.get_specialization(specialization_id)
            if not specialization:
                st.error("❌ Specialization not found!")
            else:
                # Show confirmation
                st.warning(f"⚠️ Are you sure you want to delete **{specialization.name}**?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                        try:
                            service.delete_specialization(specialization_id, force=False)
                            st.success(f"✅ Specialization '{specialization.name}' deactivated successfully!")
                            st.session_state.show_delete_specialization = False
                            st.rerun()
                        except ValueError as e:
                            st.error(f"❌ Cannot delete: {e}")
                        except Exception as e:
                            st.error(f"❌ Failed to delete: {e}")
                
                with col2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.show_delete_specialization = False
                        st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
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
            
            st.dataframe(
                df[display_cols],
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            st.caption(f"Showing {len(specializations)} specialization(s)")
            
            # Show statistics
            st.subheader("📊 Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            total = len(service.get_all_specializations(active_only=False))
            active = len([s for s in specializations if s.is_active])
            inactive = total - active
            
            with col1:
                st.metric("Total Specializations", total)
            with col2:
                st.metric("Active", active)
            with col3:
                st.metric("Inactive", inactive)
            with col4:
                total_capacity = sum(s.max_capacity for s in specializations if s.is_active)
                st.metric("Total Capacity", total_capacity)
        else:
            st.info("No specializations found matching your criteria.")
    
    except Exception as e:
        st.error(f"❌ Error loading specializations: {e}")


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
