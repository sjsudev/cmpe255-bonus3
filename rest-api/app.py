from __future__ import print_function, division
from flask import Flask, jsonify, request
import numpy as np
import os
import tensorflow as tf

# Initialize Flask App
app = Flask(__name__)

def loadsavedmodel(path):
    reconstructed_model = tf.keras.models.load_model(path)
    reconstructed_model.summary()
    return reconstructed_model

def inference(infermodel, img_np, class_names):
    img_array = tf.expand_dims(img_np, 0) # Create a batch (1, 224, 224, 3)

    predictions = infermodel.predict(img_array)#(1, 5)
    score = tf.nn.softmax(predictions[0])#Tensor: shape=(5,)

    return str(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    model = loadsavedmodel('tfmodel.h5')

    #img_array = tfgetimagearray(args.data_path, args.img_height, args.img_width)


    return str(inference(model, data['tweet']))

if __name__ == '__main__':
    app.run()