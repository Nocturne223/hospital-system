"""
Database package for Hospital Management System.
"""

try:
    # Try relative import first (when in src package)
    try:
        from config import USE_MYSQL
    except ImportError:
        # Try absolute import (when src is in path)
        from src.config import USE_MYSQL
    
    if USE_MYSQL:
        from .mysql_db_manager import MySQLDatabaseManager as DatabaseManager
    else:
        from .db_manager import DatabaseManager
except (ImportError, NameError):
    # Fallback to SQLite if config doesn't exist or USE_MYSQL not defined
    from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
