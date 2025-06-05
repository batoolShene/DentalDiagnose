# backend/services/image_processing/enhance_service.py
import cv2
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

def enhance_image(image_path, output_dir):
    """
    Enhance dental X-ray or CT scan image.
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save the enhanced image
        
    Returns:
        Path to the enhanced image if successful, None otherwise
    """
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Could not read image at {image_path}")
            return None
        
        # Convert to grayscale if not already
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Save the enhanced image
        filename = f"enhanced_{os.path.basename(image_path)}"
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, enhanced)
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error enhancing image: {str(e)}")
        return None