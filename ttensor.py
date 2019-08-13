from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
from tensorflow import keras

tf.logging.set_verbosity(tf.compat.v1.logging.INFO)


# Returns a short sequential model
def create_model():
  model = tf.keras.models.Sequential([
    keras.layers.Dense(512, activation=tf.keras.activations.relu, input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation=tf.keras.activations.softmax)
  ])

  model.compile(optimizer=tf.keras.optimizers.Adam(),
                loss=tf.keras.losses.sparse_categorical_crossentropy,
                metrics=['accuracy'])

  return model


# Create a basic model instance
model = create_model()
model.summary()



print("Done")

