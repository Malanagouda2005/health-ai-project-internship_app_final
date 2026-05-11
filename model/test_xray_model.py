import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = 224
BATCH_SIZE = 32

# Resolve paths relative to repository root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEST_DIR = os.path.join(BASE_DIR, 'data', 'datasets', 'chest_xray', 'test')

# Load test data
test_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
)

test_gen = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# Load trained model
model = tf.keras.models.load_model("best_model.h5")

# Evaluate
loss, acc, auc = model.evaluate(test_gen)

print("\n✅ X-RAY MODEL RESULTS")
print("Test Accuracy:", acc)
print("Test AUC:", auc)