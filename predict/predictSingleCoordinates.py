import shutil

import requests
import os
import tensorflow as tf
import numpy as np

from googleMapsApiKey import GoogleMapsApiKey
from imageProcessors.utils.joinImagesInFolder import joinImagesInFolder
import time


def predictSingleCoordinates(latitude, longitude, singlePointName, modelPath, datasetPath):
    # class_names = os.listdir(datasetPath)
    class_names = ['bad', 'good', 'medium']
    model = tf.keras.saving.load_model(modelPath)
    if os.path.isdir(singlePointName):
        shutil.rmtree(singlePointName)
    imagePathName = createSingleFormattedImage(latitude, longitude, singlePointName)
    img = tf.keras.utils.load_img(
        f"{imagePathName}/0_joined_0.png", target_size=(300, 2400)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    shutil.rmtree("predictionImages")
    return ("This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )


def createSingleFormattedImage(latitude, longitude, imagePathName):
    failed = False
    index = 0
    os.mkdir(imagePathName)
    folderName = f'''{imagePathName}/_{index}_{0}'''
    os.mkdir(f"{folderName}")
    for angle in [0, 90, 180, 270]:
        metadataResponse = requests.post(f"https://maps.googleapis.com/maps/api/streetview/metadata?location={latitude},{longitude}&heading={angle}&pitch=0.0&fov=90&key={GoogleMapsApiKey.GoogleMapsApiKey}").json()
        if metadataResponse.get('status') == 'ZERO_RESULTS':
            failed = True
            os.rmdir(folderName)
            raise "no image in selected coordinates"
        response = requests.post(f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={latitude},{longitude}&heading={angle}&pitch=0.0&fov=90&key={GoogleMapsApiKey.GoogleMapsApiKey}")
        file = open(f"{folderName}/{index}_{angle}_{0}.png", "wb")
        file.write(response.content)
        file.close()
    if not failed:
        joinImagesInFolder(folderToStoreProcessedImage=imagePathName, index=index, score=0, imagesFolderName=folderName)
    return imagePathName
