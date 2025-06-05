# backend/setup_database_xampp.py
"""
Database setup script for AIDentify with XAMPP
This version handles empty passwords correctly for XAMPP setup.
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import bcrypt

# Load environment variables
load_dotenv()

def create_initial_users():
    """Create initial admin, doctor, and employee users."""
    try:
        # Get database connection parameters
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')  # Empty string is valid for XAMPP
        db_name = os.getenv('DB_NAME', 'dental_diagnostic_system')
        db_port = int(os.getenv('DB_PORT', 3306))
        
        print(f"Connecting to: {db_user}@{db_host}:{db_port}/{db_name}")
        print(f"Password: {'(empty)' if db_password == '' else '(set)'}")
        
        # Connect to the database
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        
        cursor = connection.cursor()
        
        # Initial users data for your schema
        initial_users = [
            {
                'name': 'System Administrator',
                'email': 'admin@aidentify.com',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'name': 'Dr. John Smith',
                'email': 'doctor@aidentify.com',
                'password': 'doctor123',
                'role': 'doctor'
            },
            {
                'name': 'Sarah Johnson',
                'email': 'employee@aidentify.com',
                'password': 'employee123',
                'role': 'employee'
            }
        ]
        
        for user_data in initial_users:
            try:
                # Check if user already exists
                check_query = "SELECT email FROM users WHERE email = %s"
                cursor.execute(check_query, (user_data['email'],))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    print(f"✓ User '{user_data['email']}' already exists")
                    continue
                
                # Hash password
                password_hash = bcrypt.hashpw(
                    user_data['password'].encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # Insert user using your table structure
                insert_query = """
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
                """
                
                cursor.execute(insert_query, (
                    user_data['name'],
                    user_data['email'],
                    password_hash,
                    user_data['role']
                ))
                
                print(f"✓ Created user: {user_data['email']} ({user_data['role']})")
                
            except Error as e:
                print(f"✗ Error creating user {user_data['email']}: {e}")
                continue
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"✗ Error creating initial users: {e}")
        return False

def test_connection():
    """Test database connection and show table structure."""
    try:
        # Get database connection parameters
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')  # Empty string is valid for XAMPP
        db_name = os.getenv('DB_NAME', 'dental_diagnostic_system')
        db_port = int(os.getenv('DB_PORT', 3306))
        
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        
        if connection.is_connected():
            print("✓ Database connection successful")
            
            cursor = connection.cursor()
            
            # Check users table
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"✓ Total users in database: {user_count}")
            
            # Show table structure
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            print("\n✓ Users table structure:")
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
            
            # Show all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n✓ Database tables: {[table[0] for table in tables]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Database connection failed: {e}")
        return False

def verify_users():
    """Verify that users were created correctly."""
    try:
        # Get database connection parameters
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'dental_diagnostic_system')
        db_port = int(os.getenv('DB_PORT', 3306))
        
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, email, role, created_at FROM users ORDER BY created_at")
        users = cursor.fetchall()
        
        print("\n✓ Current users in database:")
        for user in users:
            print(f"  - {user['name']} ({user['email']}) - Role: {user['role']} - Created: {user['created_at']}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"✗ Error verifying users: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("AIDentify Database Setup - XAMPP Version")
    print("=" * 60)
    
    # Show environment variables (but don't require all to be non-empty)
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'dental_diagnostic_system')
    
    print(f"Database Host: {db_host}")
    print(f"Database Name: {db_name}")
    print(f"Database User: {db_user}")
    print(f"Database Password: {'(empty - correct for XAMPP)' if db_password == '' else '(set)'}")
    print("-" * 60)
    
    # Check critical variables (allow empty password for XAMPP)
    if not db_host or not db_user or not db_name:
        print("✗ Missing critical environment variables")
        print("Please check your .env file")
        sys.exit(1)
    
    # Step 1: Test connection
    print("Step 1: Testing database connection...")
    if not test_connection():
        print("✗ Connection test failed")
        print("\nTroubleshooting:")
        print("1. Make sure XAMPP MySQL is running")
        print("2. Check if database 'dental_diagnostic_system' exists in phpMyAdmin")
        print("3. Verify XAMPP is using default port 3306")
        sys.exit(1)
    
    # Step 2: Create initial users
    print("\nStep 2: Creating initial users...")
    if not create_initial_users():
        print("✗ User creation failed")
        sys.exit(1)
    
    # Step 3: Verify users
    print("\nStep 3: Verifying users...")
    if not verify_users():
        print("✗ User verification failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print("\nInitial login credentials:")
    print("Admin: admin@aidentify.com / admin123")
    print("Doctor: doctor@aidentify.com / doctor123")  
    print("Employee: employee@aidentify.com / employee123")
    print("\nNOTE: Use EMAIL addresses to log in, not usernames.")
    print("Please change these passwords after first login.")

if __name__ == "__main__":
    main()