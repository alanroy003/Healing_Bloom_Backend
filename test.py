import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image

# Define model path and image path
MODEL_PATH = "diseases/models/skin_dis.h5"
IMAGE_PATH = "OIP.jpeg"
CLASS_NAMES = ['AKIEC', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'VASC']

# Load model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = load_model(MODEL_PATH)
print("Model loaded successfully!")

# Load and preprocess image
try:
    img = Image.open(IMAGE_PATH)
    img = img.convert("RGB")  # Ensure it's in RGB mode
    img = img.resize((224, 224))  # Resize to match model input size

    # Convert to numpy array and normalize pixel values
    img_array = np.array(img) / 255.0  # Normalize to [0,1] range
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
except Exception as e:
    raise ValueError(f"Error processing image: {str(e)}")

# Make prediction
predictions = model.predict(img_array)
confidence = float(np.max(predictions))
class_index = int(np.argmax(predictions))

print("Expected input shape:", model.input_shape)
print("Actual input shape:", img_array.shape)

if class_index >= len(CLASS_NAMES):
    raise ValueError("Invalid class index from model prediction")

predicted_class = CLASS_NAMES[class_index]

# Print results
print(f"Predicted class: {predicted_class}")
print(f"Confidence: {confidence:.4f}")
