import os
import numpy as np
import tensorflow as tf


def predictSingleImage(imagePath, modelPath, datasetPath):
    class_names = os.listdir(datasetPath)
    model = tf.keras.saving.load_model(modelPath)
    img = tf.keras.utils.load_img(
        imagePath, target_size=(300, 2400)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
    )