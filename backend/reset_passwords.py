import os
import mysql.connector
import bcrypt
from dotenv import load_dotenv

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'dental_diagnostic_system'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    
    cursor = connection.cursor()
    
    # Reset passwords
    users = [
        ('admin@aidentify.com', 'admin123'),
        ('doctor@aidentify.com', 'doctor123'),
        ('secretaire@aidentify.com', 'employee123'),
        ('employee@aidentify.com', 'employee123')
    ]
    
    for email, password in users:
        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed, email))
        print(f"Reset password for {email}")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("✓ All passwords reset successfully!")
    
except Exception as e:
    print(f"Error: {e}")