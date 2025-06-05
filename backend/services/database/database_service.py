# backend/services/database/database_service.py
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        """Initialize database connection."""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME', 'dental_diagnostic_system')  # Updated to match your DB name
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = None
    
    def connect(self):
        """Create database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=True
            )
            
            if self.connection.is_connected():
                logger.info("Successfully connected to MySQL database")
                return True
                
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and return results if fetch=True."""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
                
        except Error as e:
            logger.error(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
            return None if fetch else False
    
    def execute_single_query(self, query, params=None):
        """Execute a query and return single result."""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            result = cursor.fetchone()
            cursor.close()
            return result
                
        except Error as e:
            logger.error(f"Error executing single query: {e}")
            return None

# Global database instance
db_service = DatabaseService()