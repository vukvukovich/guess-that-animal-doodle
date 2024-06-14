import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, Input
from sklearn.model_selection import train_test_split

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def load_all_quickdraw_data(directory, num_samples_per_category=5000):
    categories = []
    X = []
    y = []

    for filename in os.listdir(directory):
        if filename.endswith('.npy'):
            category = filename.split('.')[0]
            categories.append(category)
            data = np.load(os.path.join(directory, filename))
            X.append(data[:num_samples_per_category])
            y.extend([len(categories) - 1] * num_samples_per_category)

    X = np.concatenate(X, axis=0)
    y = np.array(y)
    return X, y, categories


data_directory = 'ml/datasets'

X, y, categories = load_all_quickdraw_data(data_directory)

X = X / 255.0

X = X.reshape(-1, 28, 28, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = models.Sequential([
    Input(shape=(28, 28, 1)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(len(categories), activation='softmax')  # Number of categories
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test))

model.save('ml/models/quickdraw_cnn_model_some_animals.keras')

print(categories)
