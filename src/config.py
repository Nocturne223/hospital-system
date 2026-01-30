"""
Configuration file for Hospital Management System
"""

# Database Configuration
USE_MYSQL = True  # Set to False to use SQLite

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Empty for default XAMPP
    'database': 'hospital_system'
}

# SQLite Configuration (if needed)
SQLITE_CONFIG = {
    'db_path': 'data/hospital_system.db'
}
