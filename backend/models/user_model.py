import bcrypt
from datetime import datetime
from services.database.database_service import db_service
import logging

logger = logging.getLogger(__name__)

class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.role = kwargs.get('role')
        self.created_at = kwargs.get('created_at')
        self.status = kwargs.get('status')
        self.phone_number = kwargs.get('phoneNumber') or kwargs.get('phone_number')
        self.country = kwargs.get('Country') or kwargs.get('country')

        self.extra_fields = {
            k: v for k, v in kwargs.items()
            if k not in [
                'id', 'name', 'email', 'password', 'role',
                'created_at', 'status', 'phoneNumber', 'phone_number', 'country', 'Country'
            ]
        }

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    def create_user(cls, name, email, password, role, status='inProcess'):
        try:
            if cls.get_by_email(email):
                raise ValueError("Email already exists")

            hashed_password = cls.hash_password(password)
            query = """
                INSERT INTO users (name, email, password, role, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (name, email, hashed_password, role, status)
            success = db_service.execute_query(query, params)

            if success:
                logger.info(f"User {name} ({email}) created successfully")
                created_user = cls.get_by_email(email)
                created_user.log_activity("Created account")
                return created_user
            else:
                raise Exception("Failed to create user")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    @classmethod
    def get_by_email(cls, email):
        try:
            query = "SELECT * FROM users WHERE email = %s"
            result = db_service.execute_single_query(query, (email,))
            return cls(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None

    @classmethod
    def get_by_id(cls, user_id):
        try:
            query = "SELECT * FROM users WHERE id = %s"
            result = db_service.execute_single_query(query, (user_id,))
            return cls(**result) if result else None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None

    @classmethod
    def authenticate(cls, email, password):
        try:
            user = cls.get_by_email(email)
            if user and cls.verify_password(password, user.password):
                logger.info(f"User {email} authenticated successfully")
                user.log_activity("Logged in")
                return user
            logger.warning(f"Authentication failed for email: {email}")
            return None
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None

    def update_password(self, new_password):
        try:
            hashed_password = self.hash_password(new_password)
            query = "UPDATE users SET password = %s WHERE id = %s"
            success = db_service.execute_query(query, (hashed_password, self.id))
            if success:
                self.password = hashed_password
                logger.info(f"Password updated for user {self.email}")
                self.log_activity("Updated password")
            return success
        except Exception as e:
            logger.error(f"Error updating password: {e}")
            return False

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'phoneNumber': self.phone_number,
            'country': self.country
        }
        data.update(self.extra_fields)
        return data

    @classmethod
    def get_all_users(cls):
        try:
            query = "SELECT * FROM users ORDER BY created_at DESC"
            results = db_service.execute_query(query, fetch=True)
            return [cls(**row) for row in results] if results else []
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []

    @classmethod
    def get_users_by_status(cls, status):
        try:
            query = "SELECT * FROM users WHERE status = %s ORDER BY created_at DESC"
            results = db_service.execute_query(query, (status,), fetch=True)
            return [cls(**row) for row in results] if results else []
        except Exception as e:
            logger.error(f"Error getting users by status: {e}")
            return []

    @classmethod
    def seed_initial_users(cls):
        initial_users = [
            {
                'name': 'System Administrator',
                'email': 'admin@aidentify.com',
                'password': 'admin123',
                'role': 'admin',
                'status': 'active'
            },
            {
                'name': 'Dr. John Smith',
                'email': 'doctor@aidentify.com',
                'password': 'doctor123',
                'role': 'doctor',
                'status': 'active'
            },
            {
                'name': 'Sarah Johnson',
                'email': 'employee@aidentify.com',
                'password': 'employee123',
                'role': 'employee',
                'status': 'active'
            }
        ]
        try:
            for user_data in initial_users:
                if not cls.get_by_email(user_data['email']):
                    user = cls.create_user(
                        name=user_data['name'],
                        email=user_data['email'],
                        password=user_data['password'],
                        role=user_data['role'],
                        status=user_data['status']
                    )
                    logger.info(f"Created initial user: {user_data['email']}")
                else:
                    logger.info(f"User {user_data['email']} already exists")
            logger.info("Initial users seeding completed")
            return True
        except Exception as e:
            logger.error(f"Error seeding initial users: {e}")
            return False

    def log_activity(self, action_description):
        try:
            query = """
                INSERT INTO activity_logs (user_id, action, description, timestamp)
                VALUES (%s, %s, %s, %s)
            """
            action = action_description.split()[0].capitalize()
            params = (self.id, action, action_description, datetime.now())
            success = db_service.execute_query(query, params)
            if success:
                logger.info(f"Activity logged for user {self.email}: {action_description}")
            return success
        except Exception as e:
            logger.error(f"Error logging activity: {e}")
            return False

    @classmethod
    def get_activity_logs(cls, limit=100):
        try:
            query = """
                SELECT al.*, u.name, u.email 
                FROM activity_log al 
                JOIN users u ON al.user_id = u.id 
                ORDER BY al.timestamp DESC 
                LIMIT %s
            """
            results = db_service.execute_query(query, (limit,), fetch=True)
            return results if results else []
        except Exception as e:
            logger.error(f"Error getting activity logs: {e}")
            return []
