from __future__ import print_function, division
from flask import Flask, jsonify, request
import numpy as np
import os
import tensorflow as tf
import re
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from keras.preprocessing.sequence import pad_sequences

# Initialize Flask App
app = Flask(__name__)

graph = tf.get_default_graph()

def loadsavedmodel(path):
    reconstructed_model = tf.keras.models.load_model(path)
    reconstructed_model.summary()
    return reconstructed_model

def preprocess(content, stem=False):
    english_stopwords = stopwords.words('english')

    stemmer = SnowballStemmer('english')

    regex = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"  
    content = re.sub(regex, ' ', str(content).lower()).strip()
    
    tokens = []
    
    for token in content.split():
        if token not in english_stopwords:
            tokens.append(stemmer.stem(token))
    return " ".join(tokens)

def inference(infermodel, tweet):
    predictions = infermodel.predict(tweet) #(1, 5)
    # score = tf.nn.softmax(predictions[0])#Tensor: shape=(5,)
    
    return int(np.round(predictions))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    model = loadsavedmodel('tfmodel.h5')

    #img_array = tfgetimagearray(args.data_path, args.img_height, args.img_width)

    x = preprocess([data['tweet']])

    with graph.as_default():
        y = inference(model, x)

        if y == 1:
            return jsonify({'prediction': "Positive"})
        else:
            return jsonify({'prediction': "Negative"})

if __name__ == '__main__':
    app.run()

