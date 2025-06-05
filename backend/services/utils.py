# backend/services/utils.py
import os
import uuid
import base64
import time
import logging
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# Mock image processing log
image_logs = []

def save_uploaded_file(file, upload_folder):
    """Save uploaded file and return the filepath"""
    if file.filename == '':
        return None
    
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    return filepath

def image_to_base64(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error converting image to base64: {str(e)}")
        return None

def log_processing(user_id, action, image_path, result_path=None):
    """Log image processing action"""
    log_entry = {
        'id': len(image_logs) + 1,
        'user_id': user_id,
        'action': action,
        'timestamp': time.time(),
        'image_path': image_path,
        'result_path': result_path
    }
    image_logs.append(log_entry)
    return log_entry

def get_image_logs():
    """Get all image processing logs"""
    return image_logs