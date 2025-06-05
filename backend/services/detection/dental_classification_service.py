# backend/services/detection/dental_classification_service.py
import os
import cv2
import numpy as np
import tensorflow as tf
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

class DentalClassifier:
    def __init__(self, model_path=None):
        """Initialize the dental classifier with a pre-trained model."""
        self.model = None
        self.class_names = ['Caries', 'Decayed Tooth', 'Ectopic', 'Healthy Teeth']
        self.img_size = (224, 224)
        self.threshold = 0.4
        
        # Load model if path is provided
        if model_path and os.path.exists(model_path):
            try:
                self.model = tf.keras.models.load_model(model_path)
                logger.info(f"Model loaded successfully from {model_path}")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
        else:
            logger.warning(f"Model path not found: {model_path}")
    
    def preprocess_image(self, image_path):
        """Preprocess the image for the model."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"Could not read image at {image_path}")
                return None
                
            # Convert to RGB (from BGR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size
            img = cv2.resize(img, self.img_size)
            
            # Normalize
            img = img / 255.0
            
            return img
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image_path):
        """Make predictions on the given image."""
        if self.model is None:
            logger.error("Model not loaded")
            return None, "Model not loaded"
        
        try:
            # Preprocess the image
            img = self.preprocess_image(image_path)
            if img is None:
                return None, "Failed to preprocess image"
            
            # Expand dimensions for batch
            img_array = np.expand_dims(img, axis=0)
            
            # Make prediction
            predictions = self.model.predict(img_array)[0]
            
            # Process results
            results = []
            has_any_condition = False
            
            for i, class_name in enumerate(self.class_names):
                confidence = float(predictions[i])
                if confidence >= self.threshold:
                    has_any_condition = True
                    results.append({
                        'condition': class_name,
                        'confidence': round(confidence * 100, 2)
                    })
            
            # If no conditions meet the threshold but not healthy
            if not has_any_condition and predictions[3] < self.threshold:
                # Get the highest confidence condition
                max_index = np.argmax(predictions[:3])  # Exclude "Healthy Teeth"
                results.append({
                    'condition': self.class_names[max_index],
                    'confidence': round(float(predictions[max_index]) * 100, 2),
                    'note': 'Low confidence detection'
                })
            
            # Create visualization with detections
            visualization = self.create_visualization(image_path, results)
            
            return {
                'detected_conditions': results,
                'visualization': visualization
            }, None
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None, f"Error making prediction: {str(e)}"
    
    # def create_visualization(self, image_path, results):
    #     """Create a visualization of the dental conditions."""
    #     try:
    #         # Read the original image
    #         img = cv2.imread(image_path)
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
    #         # Create a copy for visualization
    #         viz_img = img.copy()
            
    #         # Add text for each detected condition
    #         font = cv2.FONT_HERSHEY_SIMPLEX
    #         y_offset = 30
            
    #         for result in results:
    #             condition = result['condition']
    #             confidence = result['confidence']
                
    #             # Set color based on condition
    #             if condition == 'Caries':
    #                 color = (255, 0, 0)  # Red
    #             elif condition == 'Decayed Tooth':
    #                 color = (255, 165, 0)  # Orange
    #             elif condition == 'Ectopic':
    #                 color = (255, 0, 255)  # Purple
    #             elif condition == 'Healthy Teeth':
    #                 color = (0, 255, 0)  # Green
    #             else:
    #                 color = (255, 255, 255)  # White
                
    #             # Add text to image
    #             text = f"{condition}: {confidence}%"
    #             cv2.putText(viz_img, text, (10, y_offset), font, 0.7, color, 2)
    #             y_offset += 30
            
    #         # Convert back to BGR for OpenCV operations
    #         viz_img = cv2.cvtColor(viz_img, cv2.COLOR_RGB2BGR)
            
    #         # Save visualization to a temporary file
    #         result_filename = f"dental_analysis_{os.path.basename(image_path)}"
    #         result_path = os.path.join(os.path.dirname(image_path), result_filename)
    #         cv2.imwrite(result_path, viz_img)
            
    #         return result_path
            
    #     except Exception as e:
    #         logger.error(f"Error creating visualization: {str(e)}")
    #         return None

    def create_visualization(self, image_path, results):
        """Create a visualization of the dental conditions without overlaying text."""
        try:
            # Read the original image
            img = cv2.imread(image_path)
            
            # No text or modifications on the image
            # Just save a copy of the original image for displaying results
            
            # Save visualization to a temporary file
            result_filename = f"dental_analysis_{os.path.basename(image_path)}"
            result_path = os.path.join(os.path.dirname(image_path), result_filename)
            cv2.imwrite(result_path, img)
            
            return result_path
                
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            return None

# Initialize singleton for global use
dental_classifier = None

def get_dental_classifier(model_path=None):
    """Get or initialize dental classifier singleton."""
    global dental_classifier
    if dental_classifier is None:
        dental_classifier = DentalClassifier(model_path)
    return dental_classifier