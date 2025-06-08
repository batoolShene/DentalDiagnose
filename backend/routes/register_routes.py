from flask import Blueprint, request, jsonify
from models.user_model import User

register_bp = Blueprint('register', __name__)

@register_bp.route('', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        name = data.get('fullName')
        email = data.get('email')
        password = 'temp1234'  # Temporary password or empty
        role = 'pending_user'  # Default role
        status = 'inProcess'

        user = User.create_user(name, email, password, role, status)

        return jsonify({'message': 'Registration submitted successfully', 'user': user.to_dict()}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400
