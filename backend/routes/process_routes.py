from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth.auth_service import check_permission
from services.image_processing.enhance_service import enhance_image
from services.image_processing.colorize_service import colorize_image
from services.utils import save_uploaded_file, image_to_base64, log_processing
import logging

logger = logging.getLogger(__name__)
process_bp = Blueprint('process', __name__)

@process_bp.route('/enhance', methods=['POST'])
@jwt_required()
def enhance_image_route():
    """Enhance dental image route."""
    current_user = get_jwt_identity()
    
    # Check if the user has permission (admin or doctor)
    if not check_permission(current_user, ['admin', 'doctor']):
        return jsonify({'message': 'Permission denied'}), 403
    
    # Check if file is provided
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400
    
    file = request.files['image']
    filepath = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
    
    if not filepath:
        return jsonify({'message': 'Invalid file'}), 400
    
    # Enhance the image
    result_path = enhance_image(filepath, current_app.config['UPLOAD_FOLDER'])
    
    if not result_path:
        return jsonify({'message': 'Error enhancing image'}), 500
    
    # Log the processing
    log_processing(current_user, 'enhance', filepath, result_path)
    
    # Return the enhanced image as base64
    base64_image = image_to_base64(result_path)
    if not base64_image:
        return jsonify({'message': 'Error encoding image'}), 500
        
    return jsonify({
        'message': 'Image enhanced successfully',
        'image': base64_image
    })

@process_bp.route('/colorize', methods=['POST'])
@jwt_required()
def colorize_image_route():
    """Colorize dental image route."""
    current_user = get_jwt_identity()
    
    # Check if the user has permission (admin or doctor)
    if not check_permission(current_user, ['admin', 'doctor']):
        return jsonify({'message': 'Permission denied'}), 403
    
    # Check if file is provided
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400
    
    file = request.files['image']
    filepath = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
    
    if not filepath:
        return jsonify({'message': 'Invalid file'}), 400
    
    # Colorize the image
    result_path = colorize_image(filepath, current_app.config['UPLOAD_FOLDER'])
    
    if not result_path:
        return jsonify({'message': 'Error colorizing image'}), 500
    
    # Log the processing
    log_processing(current_user, 'colorize', filepath, result_path)
    
    # Return the colorized image as base64
    base64_image = image_to_base64(result_path)
    if not base64_image:
        return jsonify({'message': 'Error encoding image'}), 500
        
    return jsonify({
        'message': 'Image colorized successfully',
        'image': base64_image
    })