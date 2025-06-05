# backend/services/auth/auth_service.py
from flask_jwt_extended import create_access_token
from models.user_model import User
import logging

logger = logging.getLogger(__name__)

# User authentication functions
def authenticate_user(email, password):
    """Authenticate a user and return user data if valid."""
    try:
        # Authenticate using database (email instead of username)
        user = User.authenticate(email, password)
        
        if not user:
            logger.warning(f"Authentication failed for email: {email}")
            return None
        
        # Log the login activity
        user.log_activity("User logged in")
        
        # Create token with user information
        access_token = create_access_token(
            identity=user.email,  # Using email as identity
            additional_claims={
                'role': user.role,
                'user_id': user.id,
                'name': user.name,
                'email': user.email
            }
        )
        
        logger.info(f"User {email} authenticated successfully")
        
        return {
            'token': access_token,
            'user': user.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return None

def get_user_by_email(email):
    """Get user information by email."""
    try:
        user = User.get_by_email(email)
        return user.to_dict() if user else None
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

def get_user_by_id(user_id):
    """Get user information by ID."""
    try:
        user = User.get_by_id(user_id)
        return user.to_dict() if user else None
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

def get_user_role(email):
    """Get a user's role by email."""
    try:
        user = User.get_by_email(email)
        return user.role if user else None
    except Exception as e:
        logger.error(f"Error getting user role: {e}")
        return None

def check_permission(email, allowed_roles):
    """Check if a user has permission for an action."""
    try:
        role = get_user_role(email)
        return role in allowed_roles if role else False
    except Exception as e:
        logger.error(f"Error checking permission: {e}")
        return False

def create_user(name, email, password, role):
    """Create a new user (admin only function)."""
    try:
        # Validate role
        valid_roles = ['admin', 'doctor', 'employee']
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        user = User.create_user(name, email, password, role)
        if user:
            logger.info(f"New user created: {email} with role: {role}")
            return user.to_dict()
        return None
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise

def get_all_users():
    """Get all users (admin only function)."""
    try:
        users = User.get_all_users()
        return [user.to_dict() for user in users]
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

def update_user_password(email, new_password):
    """Update user password."""
    try:
        user = User.get_by_email(email)
        if user:
            success = user.update_password(new_password)
            if success:
                user.log_activity("Password updated")
                logger.info(f"Password updated for user: {email}")
            return success
        return False
    except Exception as e:
        logger.error(f"Error updating password: {e}")
        return False

def get_activity_logs(limit=100):
    """Get activity logs (admin only function)."""
    try:
        logs = User.get_activity_logs(limit)
        return logs
    except Exception as e:
        logger.error(f"Error getting activity logs: {e}")
        return []

def log_user_activity(email, action_description):
    """Log user activity."""
    try:
        user = User.get_by_email(email)
        if user:
            return user.log_activity(action_description)
        return False
    except Exception as e:
        logger.error(f"Error logging user activity: {e}")
        return False

def initialize_auth_system():
    """Initialize the authentication system with database setup."""
    try:
        from services.database.database_service import db_service
        
        # Connect to database
        if not db_service.connect():
            logger.error("Failed to connect to database")
            return False
        
        # Test if tables exist by trying to get users
        try:
            db_service.execute_query("SELECT COUNT(*) FROM users", fetch=True)
            logger.info("Database tables verified")
        except Exception as e:
            logger.error(f"Database tables not found or accessible: {e}")
            return False
        
        # Seed initial users if none exist
        existing_users = User.get_all_users()
        if not existing_users:
            if not User.seed_initial_users():
                logger.error("Failed to seed initial users")
                return False
        else:
            logger.info(f"Found {len(existing_users)} existing users in database")
        
        logger.info("Authentication system initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing auth system: {e}")
        return False