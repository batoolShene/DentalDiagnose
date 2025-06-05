# backend/services/image_processing/colorize_service.py
import cv2
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

def colorize_image(image_path, output_dir):
    """
    Colorize dental X-ray or CT scan image.
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save the colorized image
        
    Returns:
        Path to the colorized image if successful, None otherwise
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
        
        # Apply pseudo-coloring (this is a simplified example)
        # In a real implementation, you'd use more sophisticated techniques
        colored = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        
        # Save the colorized image
        filename = f"colorized_{os.path.basename(image_path)}"
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, colored)
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error colorizing image: {str(e)}")
        return None