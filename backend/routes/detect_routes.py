# backend/routes/detect_routes.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth.auth_service import check_permission
from services.detection.cavity_detection import detect_cavities
from services.detection.missing_teeth_detection import detect_missing_teeth
from services.utils import save_uploaded_file, image_to_base64, log_processing
from services.model_inference.xray_service import predict_xray
import logging

logger = logging.getLogger(__name__)
detect_bp = Blueprint('detect', __name__)

@detect_bp.route('/cavities', methods=['POST'])
@jwt_required()
def detect_cavities_route():
    """Detect cavities in dental image route."""
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
    
    # Detect cavities in the image
    result_path, results = detect_cavities(filepath, current_app.config['UPLOAD_FOLDER'])
    
    if not result_path or not results:
        return jsonify({'message': 'Error detecting cavities'}), 500
    
    # Log the processing
    log_processing(current_user, 'detect_cavities', filepath, result_path)
    
    # Return the result image as base64 and detection results
    base64_image = image_to_base64(result_path)
    if not base64_image:
        return jsonify({'message': 'Error encoding image'}), 500
        
    return jsonify({
        'message': f'Detected {results["count"]} potential cavities',
        'image': base64_image,
        'results': results
    })

@detect_bp.route('/missing-teeth', methods=['POST'])
@jwt_required()
def detect_missing_teeth_route():
    """Detect missing teeth in dental image route."""
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
    
    # Detect missing teeth in the image
    result_path, results = detect_missing_teeth(filepath, current_app.config['UPLOAD_FOLDER'])
    
    if not result_path or not results:
        return jsonify({'message': 'Error detecting missing teeth'}), 500
    
    # Log the processing
    log_processing(current_user, 'detect_missing_teeth', filepath, result_path)
    
    # Return the result image as base64 and detection results
    base64_image = image_to_base64(result_path)
    if not base64_image:
        return jsonify({'message': 'Error encoding image'}), 500
        
    return jsonify({
        'message': f'Detected {results["count"]} potentially missing teeth',
        'image': base64_image,
        'results': results
    })

@detect_bp.route('/xray', methods=['POST'])
@jwt_required()
def detect_xray_route():
    """Detect features in X-ray image using DL model."""
    current_user = get_jwt_identity()
    
    # Check if the user has permission (admin or doctor)
    if not check_permission(current_user, ['admin', 'doctor']):
        return jsonify({'message': 'Permission denied'}), 403
    
    # Check if file is provided
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400
    
    file = request.files['image']
    image_bytes = file.read()
    try:
        prediction = predict_xray(image_bytes)
        return jsonify({'result': prediction})
    except Exception as e:
        logger.error(f"X-ray detection error: {e}")
        return jsonify({'message': 'Error during X-ray detection', 'error': str(e)}), 500