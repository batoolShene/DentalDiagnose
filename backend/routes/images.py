from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
from werkzeug.utils import secure_filename

image_bp = Blueprint('image', __name__)

UPLOAD_FOLDER = 'uploads'

@image_bp.route('/api/images/upload', methods=['POST'])
@jwt_required()
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({'message': 'Image uploaded successfully', 'filename': filename}), 200
