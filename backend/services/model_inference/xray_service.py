import numpy as np
import tensorflow as tf
from PIL import Image
import io

# Load the model once at startup
model = tf.keras.models.load_model('models/MultiLabel.keras')

def predict_xray(image_bytes):
    class_labels = ["caries", "ectopic", "decayed tooth", "healthy teeth"]  # Adjust order if needed
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')  # Ensure 3 channels
    image = image.resize((256, 256))  # Model expects 256x256
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 256, 256, 3)
    prediction = model.predict(img_array)
    predicted_index = int(np.argmax(prediction))
    predicted_label = class_labels[predicted_index]
    confidence = float(np.max(prediction))
    return {
        "label": predicted_label,
        "confidence": confidence,
        "raw": prediction.tolist()
    }