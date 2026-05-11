import os
import tensorflow as tf
import numpy as np
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

# CONFIG
IMG_SIZE = 224
BATCH_SIZE = 32

# Resolve paths relative to repository root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_DIR = os.path.dirname(__file__)
CLASSES_FILE = os.path.join(MODEL_DIR, 'skin_classes.json')
TEST_DIR = os.path.join(BASE_DIR, 'data', 'datasets', 'SkinDisease', 'SkinDisease', 'test')
MODEL_FILE = os.path.join(MODEL_DIR, 'best_skin_model.h5')

# ✅ Load class names from JSON if available, otherwise extract from test directory
if os.path.exists(CLASSES_FILE):
    with open(CLASSES_FILE, "r") as f:
        class_names = json.load(f)
else:
    # Extract class names from test directory structure
    class_names = sorted([d for d in os.listdir(TEST_DIR) if os.path.isdir(os.path.join(TEST_DIR, d))])
    if not class_names:
        raise FileNotFoundError(f"No classes found in {TEST_DIR}")

# ✅ Data generator (same as training)
test_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
)

# ✅ Load test dataset
test_gen = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# ✅ Load trained model
model = tf.keras.models.load_model(MODEL_FILE)

# ✅ Evaluate
loss, acc, top3 = model.evaluate(test_gen)

print("\n✅ SKIN MODEL TEST RESULTS")
print("Test Accuracy:", acc)
print("Top-3 Accuracy:", top3)

# ✅ Predictions
preds = model.predict(test_gen)
y_pred = np.argmax(preds, axis=1)
y_true = test_gen.classes

print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred, target_names=class_names))