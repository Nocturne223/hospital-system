"""
MySQL Database Manager for Hospital Management System
Alternative to SQLite - uses MySQL from XAMPP.

To use this instead of SQLite:
1. Install XAMPP and start MySQL
2. Create database: hospital_system
3. Install: pip install mysql-connector-python
4. Update imports to use MySQLDatabaseManager instead of DatabaseManager
"""

import mysql.connector
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySQLDatabaseManager:
    """
    MySQL Database Manager for Hospital Management System.
    
    Requires:
    - XAMPP MySQL running
    - Database 'hospital_system' created
    - mysql-connector-python installed
    """
    
    def __init__(self, 
                 host: str = 'localhost',
                 port: int = 3306,
                 user: str = 'root',
                 password: str = '',
                 database: str = 'hospital_system',
                 schema_path: Optional[str] = None):
        """
        Initialize MySQL Database Manager.
        
        Args:
            host: MySQL host (default: localhost)
            port: MySQL port (default: 3306)
            user: MySQL username (default: root)
            password: MySQL password (default: empty for XAMPP)
            database: Database name
            schema_path: Path to schema SQL file
        """
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self._last_insert_id = None
        
        if schema_path is None:
            schema_path = os.path.join(
                os.path.dirname(__file__),
                'schema_mysql.sql'
            )
        self.schema_path = schema_path
        
        # Test connection with timeout - make it quick
        try:
            print(f"Connecting to MySQL at {host}:{port}...")
            # Use a quick connection test
            test_conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connection_timeout=3,  # Very short timeout
                autocommit=True
            )
            test_conn.close()
            logger.info(f"Connected to MySQL database: {database}")
            print(f"Successfully connected to database: {database}")
        except mysql.connector.Error as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            print(f"ERROR: Failed to connect to MySQL: {e}")
            raise
        
        # Skip schema initialization during __init__ - do it lazily if needed
        # This prevents hanging during initialization
        self._schema_checked = False
    
    def _check_and_init_schema(self):
        """Lazily check and initialize schema only once"""
        if self._schema_checked:
            return
        
        self._schema_checked = True
        
        if not os.path.exists(self.schema_path):
            return
        
        try:
            # Quick check if tables exist - use direct connection
            check_conn = mysql.connector.connect(
                **self.config,
                connection_timeout=3,
                autocommit=True
            )
            cursor = check_conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            cursor.close()
            check_conn.close()
            
            if tables:
                logger.info(f"Database already initialized with {len(tables)} tables")
                return
            
            # Only initialize if no tables exist
            logger.info("Initializing database schema...")
            self.init_database()
        except Exception as e:
            logger.warning(f"Could not check/initialize database: {e}")
            # Continue anyway - tables might already exist
    
    @contextmanager
    def get_connection(self):
        """
        Get a MySQL database connection with context manager.
        """
        # Check and initialize schema lazily on first connection
        self._check_and_init_schema()
        
        # Add connection timeout to prevent hanging
        config_with_timeout = self.config.copy()
        config_with_timeout['connection_timeout'] = 5  # 5 second timeout
        config_with_timeout['autocommit'] = False
        
        conn = mysql.connector.connect(**config_with_timeout)
        try:
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
        Initialize database by executing schema SQL.
        """
        try:
            logger.info("Initializing MySQL database...")
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if os.path.exists(self.schema_path):
                    with open(self.schema_path, 'r', encoding='utf-8') as f:
                        schema_sql = f.read()
                    
                    # Execute statements one by one (MySQL doesn't support executescript)
                    statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
                    for statement in statements:
                        if statement:
                            cursor.execute(statement)
                    
                    logger.info("MySQL database schema created successfully")
                else:
                    logger.warning(f"Schema file not found: {self.schema_path}")
        except mysql.connector.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.
        
        Returns:
            List of dictionaries (row data)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)  # Return as dict
                cursor.execute(query, params)
                return cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Returns:
            Number of rows affected
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                # Store lastrowid before connection closes
                self._last_insert_id = cursor.lastrowid
                return cursor.rowcount
        except mysql.connector.Error as e:
            logger.error(f"Update execution failed: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute a query multiple times with different parameters.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, params_list)
                return cursor.rowcount
        except mysql.connector.Error as e:
            logger.error(f"Batch execution failed: {e}")
            raise
    
    def get_last_insert_id(self) -> int:
        """
        Get the ID of the last inserted row.
        
        Note: This returns the ID from the last execute_update() call
        within the same DatabaseManager instance.
        """
        if self._last_insert_id is not None:
            return self._last_insert_id
        # Fallback: query database
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            return result[0] if result else 0
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists.
        """
        query = """
            SELECT COUNT(*) as count 
            FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = %s
        """
        result = self.execute_query(query, (self.config['database'], table_name))
        return result[0]['count'] > 0 if result else False
    
    def get_table_count(self, table_name: str) -> int:
        """
        Get the number of rows in a table.
        """
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about a table's structure.
        """
        query = f"DESCRIBE {table_name}"
        return self.execute_query(query)
    
    def backup_database(self, backup_path: Optional[str] = None) -> str:
        """
        Create a backup using mysqldump (requires mysqldump in PATH).
        """
        import subprocess
        
        if backup_path is None:
            backup_dir = 'data/backups'
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"hospital_system_mysql_{timestamp}.sql")
        
        # Use mysqldump command
        cmd = [
            'mysqldump',
            f'--host={self.config["host"]}',
            f'--port={self.config["port"]}',
            f'--user={self.config["user"]}',
            f'--password={self.config["password"]}',
            self.config['database']
        ]
        
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                subprocess.run(cmd, stdout=f, check=True)
            logger.info(f"Database backed up to {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
