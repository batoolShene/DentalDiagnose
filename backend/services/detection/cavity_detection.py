# backend/services/detection/cavity_detection.py
import cv2
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

def detect_cavities(image_path, output_dir):
    """
    Detect cavities in dental X-ray.
    
    Args:
        image_path: Path to the input image
        output_dir: Directory to save the result image
        
    Returns:
        Tuple of (result_path, detection_results) if successful,
        (None, None) otherwise
    """
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Could not read image at {image_path}")
            return None, None
        
        # For now, this is a placeholder for actual ML model inference
        # In a real implementation, you'd load and use your trained model here
        img_copy = img.copy()
        
        # Convert to grayscale if not already
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            img_copy = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        # Mock detection: find potential cavity-like regions based on intensity
        _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and draw bounding boxes
        min_area = 50
        max_area = 1000
        cavities = []
        
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Mock confidence score (random for demo)
                confidence = np.random.uniform(0.7, 0.95)
                
                # Draw on image
                cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img_copy, f"{confidence:.2f}", (x, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                # Add to results
                cavities.append({
                    'id': i + 1,
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'confidence': float(confidence)
                })
        
        # Save the result image
        filename = f"cavities_{os.path.basename(image_path)}"
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img_copy)
        
        return output_path, {
            'cavities': cavities,
            'count': len(cavities)
        }
        
    except Exception as e:
        logger.error(f"Error detecting cavities: {str(e)}")
        return None, None