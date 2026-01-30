"""
Main Window for Hospital Management System
PyQt6 GUI Application
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
    QMessageBox, QTabWidget, QHeaderView, QDialog, QFormLayout,
    QDateEdit, QComboBox, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import with fallback for linter
try:
    from database import DatabaseManager  # type: ignore
    from services.patient_service import PatientService  # type: ignore
    from config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG  # type: ignore
except ImportError:
    # Fallback for absolute imports
    from src.database import DatabaseManager  # type: ignore
    from src.services.patient_service import PatientService  # type: ignore
    from src.config import USE_MYSQL, MYSQL_CONFIG, SQLITE_CONFIG  # type: ignore


class PatientDialog(QDialog):
    """Dialog for creating/editing patients"""
    
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.setWindowTitle("Edit Patient" if patient_data else "New Patient")
        self.setModal(True)
        self.setup_ui()
        
        if patient_data:
            self.load_patient_data(patient_data)
    
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout()
        
        # Form
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        form.addRow("Full Name *:", self.name_input)
        
        self.dob_input = QDateEdit()
        self.dob_input.setDate(QDate.currentDate().addYears(-30))
        self.dob_input.setCalendarPopup(True)
        form.addRow("Date of Birth *:", self.dob_input)
        
        self.gender_input = QComboBox()
        self.gender_input.addItems(["", "Male", "Female", "Other"])
        form.addRow("Gender:", self.gender_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("555-1234")
        form.addRow("Phone Number:", self.phone_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form.addRow("Email:", self.email_input)
        
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(60)
        form.addRow("Address:", self.address_input)
        
        self.status_input = QComboBox()
        self.status_input.addItems(["Normal", "Urgent", "Super-Urgent"])
        form.addRow("Status:", self.status_input)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.resize(400, 350)
    
    def load_patient_data(self, patient_data):
        """Load patient data into form"""
        self.name_input.setText(patient_data.get('full_name', ''))
        if patient_data.get('date_of_birth'):
            date = QDate.fromString(patient_data['date_of_birth'], Qt.DateFormat.ISODate)
            if date.isValid():
                self.dob_input.setDate(date)
        if patient_data.get('gender'):
            index = self.gender_input.findText(patient_data['gender'])
            if index >= 0:
                self.gender_input.setCurrentIndex(index)
        self.phone_input.setText(patient_data.get('phone_number', ''))
        self.email_input.setText(patient_data.get('email', ''))
        self.address_input.setPlainText(patient_data.get('address', ''))
        status = patient_data.get('status', 0)
        self.status_input.setCurrentIndex(status)
    
    def get_patient_data(self):
        """Get patient data from form"""
        return {
            'full_name': self.name_input.text().strip(),
            'date_of_birth': self.dob_input.date().toString(Qt.DateFormat.ISODate),
            'gender': self.gender_input.currentText() or None,
            'phone_number': self.phone_input.text().strip() or None,
            'email': self.email_input.text().strip() or None,
            'address': self.address_input.toPlainText().strip() or None,
            'status': self.status_input.currentIndex()
        }


class PatientManagementWidget(QWidget):
    """Widget for patient management"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = None
        self._db_error = None
        self.setup_ui()
        # Delay database initialization to prevent blocking window creation
        # Use QTimer to initialize after window is shown
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self.init_database_delayed)
    
    def init_database_delayed(self):
        """Initialize database after window is shown"""
        self.init_database()
        self.load_patients()
    
    def init_database_delayed(self):
        """Initialize database after window is shown (delayed to prevent blocking)"""
        self.init_database()
        if self.service:
            self.load_patients()
    
    def init_database(self):
        """Initialize database and service"""
        try:
            if USE_MYSQL:
                # Note: DatabaseManager is dynamically selected (MySQL or SQLite)
                # The type checker may show warnings, but code works correctly at runtime
                db = DatabaseManager(  # pyright: ignore[reportCallIssue]
                    host=MYSQL_CONFIG['host'],
                    port=MYSQL_CONFIG['port'],
                    user=MYSQL_CONFIG['user'],
                    password=MYSQL_CONFIG['password'],
                    database=MYSQL_CONFIG['database']
                )
            else:
                db = DatabaseManager(db_path=SQLITE_CONFIG['db_path'])  # pyright: ignore[reportCallIssue]
            
            self.service = PatientService(db)
        except Exception as e:
            # Print error instead of showing message box (app might not be ready)
            print(f"ERROR: Failed to connect to database: {e}")
            print("The application will start but database operations will fail.")
            print("Please check:")
            print("  1. XAMPP MySQL is running")
            print("  2. Database 'hospital_system' exists")
            print("  3. Credentials in src/config.py are correct")
            # Show message box after app is initialized (in main function)
            self._db_error = str(e)
    
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Patient Management")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, or email...")
        self.search_input.textChanged.connect(self.on_search)
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.on_search)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add New Patient")
        self.add_btn.clicked.connect(self.on_add_patient)
        self.edit_btn = QPushButton("Edit Patient")
        self.edit_btn.clicked.connect(self.on_edit_patient)
        self.delete_btn = QPushButton("Delete Patient")
        self.delete_btn.clicked.connect(self.on_delete_patient)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_patients)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Age", "Status", "Phone", "Email"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.on_edit_patient)
        layout.addWidget(self.table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def load_patients(self):
        """Load patients into table"""
        if not self.service:
            return
        
        try:
            patients = self.service.get_all_patients()
            self.table.setRowCount(len(patients))
            
            for row, patient in enumerate(patients):
                self.table.setItem(row, 0, QTableWidgetItem(str(patient.patient_id)))
                self.table.setItem(row, 1, QTableWidgetItem(patient.full_name))
                age_str = str(patient.age) if patient.age else "N/A"
                self.table.setItem(row, 2, QTableWidgetItem(age_str))
                self.table.setItem(row, 3, QTableWidgetItem(patient.status_text))
                self.table.setItem(row, 4, QTableWidgetItem(patient.phone_number or "N/A"))
                self.table.setItem(row, 5, QTableWidgetItem(patient.email or "N/A"))
            
            self.status_label.setText(f"Loaded {len(patients)} patients")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load patients:\n{e}")
    
    def on_search(self):
        """Handle search"""
        if not self.service:
            return
        
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_patients()
            return
        
        try:
            patients = self.service.search_patients(search_term)
            self.table.setRowCount(len(patients))
            
            for row, patient in enumerate(patients):
                self.table.setItem(row, 0, QTableWidgetItem(str(patient.patient_id)))
                self.table.setItem(row, 1, QTableWidgetItem(patient.full_name))
                age_str = str(patient.age) if patient.age else "N/A"
                self.table.setItem(row, 2, QTableWidgetItem(age_str))
                self.table.setItem(row, 3, QTableWidgetItem(patient.status_text))
                self.table.setItem(row, 4, QTableWidgetItem(patient.phone_number or "N/A"))
                self.table.setItem(row, 5, QTableWidgetItem(patient.email or "N/A"))
            
            self.status_label.setText(f"Found {len(patients)} patient(s)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed:\n{e}")
    
    def get_selected_patient_id(self):
        """Get selected patient ID from table"""
        current_row = self.table.currentRow()
        if current_row < 0:
            return None
        id_item = self.table.item(current_row, 0)
        if id_item:
            return int(id_item.text())
        return None
    
    def on_add_patient(self):
        """Handle add patient"""
        dialog = PatientDialog(self)
        if dialog.exec():
            patient_data = dialog.get_patient_data()
            if not patient_data['full_name']:
                QMessageBox.warning(self, "Validation Error", "Full name is required!")
                return
            
            try:
                patient_id = self.service.create_patient(patient_data)
                QMessageBox.information(self, "Success", 
                                      f"Patient created successfully!\nID: {patient_id}")
                self.load_patients()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create patient:\n{e}")
    
    def on_edit_patient(self):
        """Handle edit patient"""
        patient_id = self.get_selected_patient_id()
        if not patient_id:
            QMessageBox.warning(self, "No Selection", "Please select a patient to edit.")
            return
        
        try:
            patient = self.service.get_patient(patient_id)
            if not patient:
                QMessageBox.warning(self, "Not Found", "Patient not found.")
                return
            
            dialog = PatientDialog(self, patient.to_dict())
            if dialog.exec():
                patient_data = dialog.get_patient_data()
                success = self.service.update_patient(patient_id, patient_data)
                if success:
                    QMessageBox.information(self, "Success", "Patient updated successfully!")
                    self.load_patients()
                else:
                    QMessageBox.warning(self, "Error", "Failed to update patient.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit patient:\n{e}")
    
    def on_delete_patient(self):
        """Handle delete patient"""
        patient_id = self.get_selected_patient_id()
        if not patient_id:
            QMessageBox.warning(self, "No Selection", "Please select a patient to delete.")
            return
        
        # Get patient name for confirmation
        try:
            patient = self.service.get_patient(patient_id)
            if not patient:
                QMessageBox.warning(self, "Not Found", "Patient not found.")
                return
            
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete patient:\n{patient.full_name}?\n\n"
                "This will also delete all related records (queue entries, appointments).",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.service.delete_patient(patient_id)
                if success:
                    QMessageBox.information(self, "Success", "Patient deleted successfully!")
                    self.load_patients()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete patient.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete patient:\n{e}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Management System")
        self.setGeometry(100, 100, 1200, 700)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main window UI"""
        # Create central widget with tabs
        central_widget = QTabWidget()
        
        # Patient Management Tab
        patient_widget = PatientManagementWidget()
        central_widget.addTab(patient_widget, "Patient Management")
        
        # Placeholder for future tabs
        placeholder = QWidget()
        placeholder_layout = QVBoxLayout()
        placeholder_label = QLabel("More features coming soon...\n\n"
                                   "Queue Management\n"
                                   "Doctor Management\n"
                                   "Appointment System\n"
                                   "Reports & Analytics")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_layout.addWidget(placeholder_label)
        placeholder.setLayout(placeholder_layout)
        central_widget.addTab(placeholder, "Queue Management")
        central_widget.addTab(placeholder, "Doctors")
        central_widget.addTab(placeholder, "Appointments")
        central_widget.addTab(placeholder, "Reports")
        
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")


def main():
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Check if database connection was successful
        patient_widget = window.centralWidget().widget(0) if window.centralWidget() else None
        if patient_widget and hasattr(patient_widget, '_db_error') and patient_widget._db_error:
            QMessageBox.warning(window, "Database Warning", 
                              f"Database connection failed!\n\n"
                              f"Error: {patient_widget._db_error}\n\n"
                              f"Please check:\n"
                              f"1. XAMPP MySQL is running\n"
                              f"2. Database 'hospital_system' exists\n"
                              f"3. Credentials in src/config.py are correct\n\n"
                              f"The application will start but database operations will fail.")
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
