import ray
from ray import serve

import os
import time
import numpy as np

TRAINED_MODEL_PATH = './models/mnist_model.h5'


def train_and_save_model():
    import tensorflow as tf

    # Load mnist dataset
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # Train a simple neural net model
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10),
        ]
    )
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=1)

    model.evaluate(x_test, y_test, verbose=2)
    model.summary()

    # Save the model in h5 format in local file system
    model.save(TRAINED_MODEL_PATH)


if not os.path.exists(TRAINED_MODEL_PATH):
    train_and_save_model()
