# services/logger_service.py
import os
import mysql.connector
from datetime import datetime

def log_activity(user_id, action, description):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'dental_diagnostic_system'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO activity_logs (user_id, action_description, action_time)
            VALUES (%s, %s, %s)
        """, (user_id, f"{action}: {description}", datetime.utcnow()))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to log activity: {e}")
