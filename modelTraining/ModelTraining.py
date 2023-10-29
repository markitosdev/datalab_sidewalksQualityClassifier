import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib


class ModelTraining():

    def __init__(self, datasetPath, epochs=6, modelName="model"):
        self.DATASET_PATH = pathlib.Path(f'/{datasetPath}')
        self.img_height = 300
        self.img_width = 2400
        self.batch_size = 64
        self.normalization_layer = layers.Rescaling(1./255)
        self.epochs = epochs
        self.modelName = modelName

    def setTrainingDataset(self):
        return tf.keras.utils.image_dataset_from_directory(
            self.DATASET_PATH.name,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

    def setValidationDataset(self):
        return tf.keras.utils.image_dataset_from_directory(
            self.DATASET_PATH.name,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

    def setModel(self, num_classes):
        return Sequential([
            layers.Rescaling(1./255, input_shape=(self.img_height, self.img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes, kernel_regularizer='l1_l2')
        ])

    def trainModel(self):
        train_ds = self.setTrainingDataset()
        val_ds = self.setValidationDataset()
        class_names = train_ds.class_names
        num_classes = len(class_names)
        model = self.setModel(num_classes)
        print(model.summary())
        model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
        tf.keras.saving.save_model(
            model, f"{self.modelName}.keras", overwrite=True, save_format="keras"
        )
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=self.epochs
        )
        return history

    def createNeuralNetwork(self):
        results = self.trainModel()

        acc = results.history['accuracy']
        val_acc = results.history['val_accuracy']

        loss = results.history['loss']
        val_loss = results.history['val_loss']

        epochs_range = range(self.epochs)

        plt.figure(figsize=(8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.show()






