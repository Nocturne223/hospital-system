"""
Database Manager for Hospital Management System
Handles all database operations including connection management,
initialization, backup, and restore functionality.
"""

import sqlite3
import os
import shutil
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages database connections and operations for the Hospital Management System.
    
    Features:
    - Connection management with context managers
    - Database initialization
    - Transaction support
    - Backup and restore functionality
    - Query execution helpers
    """
    
    def __init__(self, db_path: str = 'data/hospital_system.db'):
        """
        Initialize the DatabaseManager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.schema_path = os.path.join(
            os.path.dirname(__file__), 
            'schema.sql'
        )
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database if it doesn't exist
        if not os.path.exists(self.db_path):
            self.init_database()
        else:
            logger.info(f"Database found at {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """
        Get a database connection with context manager.
        Automatically handles commit/rollback and connection closing.
        
        Usage:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients")
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """
        Initialize the database by creating all tables from schema.sql.
        """
        try:
            logger.info("Initializing database...")
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Read and execute schema
                if os.path.exists(self.schema_path):
                    with open(self.schema_path, 'r', encoding='utf-8') as f:
                        schema_sql = f.read()
                    cursor.executescript(schema_sql)
                    logger.info("Database schema created successfully")
                else:
                    raise FileNotFoundError(
                        f"Schema file not found at {self.schema_path}"
                    )
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
            
        Returns:
            List of Row objects (can be accessed like dictionaries)
            
        Example:
            results = db.execute_query(
                "SELECT * FROM patients WHERE status = ?",
                (1,)
            )
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of rows affected
            
        Example:
            rows_affected = db.execute_update(
                "INSERT INTO patients (full_name, date_of_birth) VALUES (?, ?)",
                ("John Doe", "1990-01-01")
            )
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute a query multiple times with different parameters.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of rows affected
            
        Example:
            params = [("John", "1990-01-01"), ("Jane", "1991-02-02")]
            db.execute_many(
                "INSERT INTO patients (full_name, date_of_birth) VALUES (?, ?)",
                params
            )
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, params_list)
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Batch execution failed: {e}")
            raise
    
    def get_last_insert_id(self) -> int:
        """
        Get the ID of the last inserted row.
        
        Returns:
            Last insert row ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            return cursor.fetchone()[0]
    
    def backup_database(self, backup_path: Optional[str] = None) -> str:
        """
        Create a backup of the database.
        
        Args:
            backup_path: Optional custom backup path. If not provided,
                        creates a timestamped backup in data/backups/
        
        Returns:
            Path to the backup file
        """
        try:
            if backup_path is None:
                # Create backup directory if it doesn't exist
                backup_dir = os.path.join(
                    os.path.dirname(self.db_path),
                    'backups'
                )
                os.makedirs(backup_dir, exist_ok=True)
                
                # Generate timestamped backup filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"hospital_system_backup_{timestamp}.db"
                backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
    
    def restore_database(self, backup_path: str) -> None:
        """
        Restore database from a backup file.
        
        Args:
            backup_path: Path to the backup file
            
        Warning: This will overwrite the current database!
        """
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Create a backup of current database before restore
            current_backup = self.backup_database()
            logger.info(f"Current database backed up to {current_backup} before restore")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            logger.info(f"Database restored from {backup_path}")
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about a table's structure.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of dictionaries with column information
        """
        query = f"PRAGMA table_info({table_name})"
        rows = self.execute_query(query)
        return [dict(row) for row in rows]
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        query = """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
    
    def get_table_count(self, table_name: str) -> int:
        """
        Get the number of rows in a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Number of rows
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query)
        return result[0][0] if result else 0
    
    def vacuum_database(self) -> None:
        """
        Optimize the database by running VACUUM.
        This reclaims unused space and optimizes the database file.
        """
        try:
            with self.get_connection() as conn:
                conn.execute("VACUUM")
            logger.info("Database vacuum completed")
        except Exception as e:
            logger.error(f"Vacuum failed: {e}")
            raise
