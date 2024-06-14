from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model('ml/models/quickdraw_cnn_model_some_animals.keras')


def load_categories(directory):
    categories = []
    for filename in os.listdir(directory):
        if filename.endswith('.npy'):
            category = filename.split('.')[0]
            categories.append(category)
    return categories


data_directory = 'ml/datasets'
categories = load_categories(data_directory)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guess', methods=['POST'])
def predict():
    try:
        data = request.json

        if not isinstance(data, dict):
            raise ValueError

        drawing = data.get('drawing')

        if drawing is None or not isinstance(drawing, list) or len(drawing) != 784:
            raise ValueError

        drawing = np.array(drawing).reshape(1, 28, 28, 1)
        prediction = model.predict(drawing)

        confidence_threshold = 0.5
        max_confidence = np.max(prediction)

        if max_confidence < confidence_threshold:
            return jsonify({'label': 'Looks like you are not so skilled at drawing. Let\'s try again?!'})

        label_index = np.argmax(prediction, axis=1)[0]
        label = categories[label_index]
        return jsonify({'label': f'Let me guess, it is a {label}?'})

    except Exception:
        return jsonify({'label': 'An error occurred... Stop playing around!'}), 400


if __name__ == '__main__':
    app.run(debug=True)
