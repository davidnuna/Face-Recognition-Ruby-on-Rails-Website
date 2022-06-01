import keras
import numpy as np
import os
import pickle

from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers, models

def create_model(image_shape):
    input_layer = layers.Input(shape = image_shape)
    convolution_1 = layers.Conv2D(36, (7,7), activation = "relu")(input_layer)
    max_pooling_1 = layers.MaxPooling2D((2,2))(convolution_1)
    batch_normalization_1 = layers.BatchNormalization()(max_pooling_1)
    dropout_1 = layers.Dropout(0.25)(batch_normalization_1)
    convolution_2 = layers.Conv2D(54, (5,5), activation = "relu")(dropout_1)
    max_pooling_2 = layers.MaxPooling2D((2,2))(convolution_2)
    batch_normalization_2 = layers.BatchNormalization()(max_pooling_2)
    dropout_2 = layers.Dropout(0.25)(batch_normalization_2)
    flatten_1 = layers.Flatten()(dropout_2)
    dense_1 = layers.Dense(2048, activation = 'relu')(flatten_1)
    dropout_3 = layers.Dropout(0.25)(dense_1)
    dense_2 = layers.Dense(512, activation = 'relu')(dropout_3)
    dropout_4 = layers.Dropout(0.25)(dense_2)
    output_layer = layers.Dense(39, activation = 'softmax')(dropout_4)

    model = models.Model(inputs = input_layer, outputs = output_layer)
    model.compile(optimizer = Adam(lr=0.0001), loss = 'categorical_crossentropy', metrics = ['accuracy'])
    model.summary()

    return model

def load_model_from_file():
	current_dir = os.getcwd().split('/')[-1]
	path = './face_recognition/cnn_implementation_YALE/model.h5' if current_dir == 'face_recognition_app' else './model.h5'
	model = models.load_model(path)
	return model

def compute_classes():
    current_dir = os.getcwd().split('/')[-1]
    path = './face_recognition/cnn_implementation_YALE/YALE_database/yale_faces_altered/' if current_dir == 'face_recognition_app' else './YALE_database/yale_faces_altered/'
    a = np.array([i for i in range(39)])
    classes = np.zeros((a.size, a.max() + 1))
    classes[np.arange(a.size), a] = 1
    dir_array = []

    path_dstore = path + '.DS_Store'
    if os.path.exists(path_dstore):
        os.remove(path_dstore)

    counter = 0
    for dir in os.listdir(path):
        dir_array.append(dir)

    return classes, dir_array