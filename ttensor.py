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


model2 = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(60, (3, 3), activation='relu', input_shape=(120, 120,3)),
  tf.keras.layers.MaxPooling2D((2, 2)),
  tf.keras.layers.Conv2D(15, (3, 3), activation='relu'),
  tf.keras.layers.MaxPooling2D((2, 2)),
  #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(8, activation='relu'),
  tf.keras.layers.Dropout(0.4),
  #tf.keras.layers.Dense(2, activation='sigmoid')
  tf.keras.layers.Dense(2, activation='softmax')
])

# Create a basic model instance
#model = create_model()
#model.summary()



print("Done")
