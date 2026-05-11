import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# CONFIG
IMG_SIZE = 224
BATCH_SIZE = 32

# ✅ SAME preprocessing as training (VERY IMPORTANT)
test_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input
)

# ✅ LOAD TEST DATA
test_gen = test_datagen.flow_from_directory(
    "data/datasets/chest_xray/test",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# ✅ LOAD TRAINED MODEL
model = tf.keras.models.load_model("best_model.h5")

# ✅ EVALUATE MODEL
loss, acc, auc = model.evaluate(test_gen)

print("\n✅ FINAL TEST RESULTS")
print("Test Accuracy:", acc)
print("Test AUC:", auc)