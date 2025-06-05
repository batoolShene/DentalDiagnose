from flask import Blueprint, request, jsonify
import os
import mysql.connector
import bcrypt
from flask_jwt_extended import create_access_token
from services.logger_service import log_activity  # Ensure this is correctly implemented

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint with activity logging."""
    try:
        data = request.json
        print(f"Login attempt with data: {data}")
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        email = data.get('username', '') or data.get('email', '')
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'dental_diagnostic_system'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = connection.cursor(dictionary=True)

        # Fetch user from database
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            log_activity(None, "login_failed", f"Failed login attempt for unknown user {email}")
            return jsonify({'message': 'Invalid email or password'}), 401

        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            log_activity(user['id'], "login_failed", "Invalid password attempt")
            return jsonify({'message': 'Invalid email or password'}), 401

        # Create JWT
        access_token = create_access_token(
            identity=user['email'],
            additional_claims={
                'role': user['role'],
                'user_id': user['id'],
                'name': user['name']
            }
        )

        # Log successful login
        log_activity(user['id'], "login", "User logged in successfully")

        # Clean up DB
        cursor.close()
        connection.close()

        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            },
            'username': user['email'],
            'role': user['role']
        })

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': f'Login error: {str(e)}'}), 500


@auth_bp.route('/test-db', methods=['GET'])
def test_database():
    """Test database connection and list users."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'dental_diagnostic_system'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, role FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify({
            'status': 'success',
            'message': 'Database connection successful',
            'users': users,
            'total_users': len(users)
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500
