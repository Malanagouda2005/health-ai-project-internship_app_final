import json
import os

import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image

print("🚀 Flask app starting...")

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "skin_model.h5")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "skin_class_names.json")

print("📂 Loading model from:", MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)

if os.path.exists(CLASS_NAMES_PATH):
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
    print(f"✅ Loaded {len(class_names)} class names from {CLASS_NAMES_PATH}")
else:
    class_names = [
        'Acne', 'Actinic_Keratosis', 'Benign_tumors', 'Bullous', 'Candidiasis',
        'DrugEruption', 'Eczema', 'Infestations_Bites', 'Lichen', 'Lupus',
        'Moles', 'Psoriasis', 'Rosacea', 'Seborrh_Keratoses', 'SkinCancer',
        'Sun_Sunlight_Damage', 'Tinea', 'Unknown_Normal', 'Vascular_Tumors',
        'Vasculitis', 'Vitiligo', 'Warts'
    ]
    print("⚠️ skin_class_names.json not found, using fallback classes")

@app.route('/')
def home():
    return "Skin Disease Prediction API Running 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']

    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    scores = prediction[0].tolist()
    class_index = int(np.argmax(scores))
    confidence = float(scores[class_index])

    return jsonify({
        "prediction": class_names[class_index],
        "confidence": round(confidence, 4),
        "scores": {class_names[i]: round(score, 4) for i, score in enumerate(scores)}
    })

if __name__ == '__main__':
    app.run(debug=True)