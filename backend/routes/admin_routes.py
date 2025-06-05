from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth.auth_service import check_permission
from services.utils import get_image_logs
from models.user_model import User
import logging
import pprint
from services.database.database_service import db_service

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

# ✅ Get logs
@admin_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    current_user = get_jwt_identity()

    if not check_permission(current_user, ['admin']):
        logger.warning(f"Permission denied for user: {current_user}")
        return jsonify({'message': 'Permission denied: admin role required'}), 403

    try:
        logs = get_image_logs()
        return jsonify(logs), 200
    except Exception as e:
        logger.error(f"Error fetching logs for user {current_user}: {e}", exc_info=True)
        return jsonify({'message': 'Internal server error'}), 500

# ✅ Get users by status
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users_by_status():
    current_user = get_jwt_identity()

    if not check_permission(current_user, ['admin']):
        logger.warning(f"Permission denied for user: {current_user}")
        return jsonify({'message': 'Permission denied: admin role required'}), 403

    status = request.args.get('status', '').strip()
    if not status:
        return jsonify({'message': 'Status query parameter is required'}), 400

    try:
        users = User.get_users_by_status(status)
        users_dict = [user.to_dict() for user in users]
        logger.debug(f"Users to return: {pprint.pformat(users_dict)}")
        return jsonify(users_dict), 200
    except Exception as e:
        logger.error(f"Error fetching users by status '{status}' for user {current_user}: {e}", exc_info=True)
        return jsonify({'message': 'Internal server error'}), 500

# ✅ Update user status
@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
def update_user_status(user_id):
    current_user = get_jwt_identity()

    if not check_permission(current_user, ['admin']):
        logger.warning(f"Permission denied for user: {current_user}")
        return jsonify({'message': 'Permission denied: admin role required'}), 403

    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ['approved', 'declined']:
        return jsonify({'message': 'Invalid status value'}), 400

    try:
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        query = "UPDATE users SET status = %s WHERE id = %s"
        success = db_service.execute_query(query, (new_status, user_id))
        if not success:
            return jsonify({'message': 'Failed to update user status'}), 500

        logger.info(f"User {user.email} status changed to {new_status} by admin {current_user}")

        user.log_activity(f"Status changed to {new_status} by admin {current_user}")

        return jsonify({'message': f'User status updated to {new_status}'}), 200
    except Exception as e:
        logger.error(f"Error updating user status: {e}", exc_info=True)
        return jsonify({'message': 'Internal server error'}), 500

@admin_bp.route('/admin-data', methods=['GET'])
@jwt_required()
def get_admin_data():
    current_user = get_jwt_identity()

    if not check_permission(current_user, ['admin']):
        logger.warning(f"Permission denied for user: {current_user}")
        return jsonify({'message': 'Permission denied: admin role required'}), 403

    try:
        query_users = """
            SELECT id, name, role, created_at AS lastLogin
            FROM users
            WHERE status = 'approved'
        """
        users = db_service.execute_query(query_users, fetch=True)

        query_logs = """
            SELECT id, user_id, action_description AS action, action_time AS timestamp
            FROM activity_logs
        """
        logs = db_service.execute_query(query_logs, fetch=True)

        logger.debug(f"Approved Users: {pprint.pformat(users)}")
        logger.debug(f"Activity Logs: {pprint.pformat(logs)}")

        return jsonify({'users': users, 'logs': logs}), 200
    except Exception as e:
        logger.error(f"Error fetching admin data for user {current_user}: {e}", exc_info=True)
        return jsonify({'message': 'Internal server error'}), 500
