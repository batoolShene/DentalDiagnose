# backend/routes/dental_detection_route.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth.auth_service import check_permission
from services.detection.dental_classification_service import get_dental_classifier
from services.utils import save_uploaded_file, image_to_base64, log_processing
import os
import logging

logger = logging.getLogger(__name__)
dental_bp = Blueprint('dental', __name__)

@dental_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_dental_xray():
    """Analyze dental X-ray for multiple conditions."""
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
    
    # Initialize model path
    model_path = os.path.join(current_app.config.get('MODEL_DIR', 'models'), 'MultiLabel.keras')
    
    # Get classifier
    classifier = get_dental_classifier(model_path)
    
    # Analyze the image
    results, error = classifier.predict(filepath)
    
    if error:
        return jsonify({'message': f'Error analyzing image: {error}'}), 500
    
    # Log the processing
    log_processing(current_user, 'dental_analysis', filepath, results.get('visualization'))
    
    # Return the result
    return jsonify({
        'message': 'Dental X-ray analysis complete',
        'image': image_to_base64(results.get('visualization')) if results.get('visualization') else None,
        'results': results.get('detected_conditions', [])
    })