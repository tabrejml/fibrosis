﻿from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.wsgi import WSGIServer

# Define a flask app
app = Flask(__name__)


MODEL_PATH = 'models/Model.h5'


model = load_model(MODEL_PATH)

print('Model loaded. Start serving...')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(135, 135)) 

    # Preprocessing the image
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

   
    preds = model.predict(img)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        os.remove(file_path)

       
        str1 = 'Normal'
        str2 = 'fibrosis'
        if preds == 1:
            return str1
        else:
            return str2
    return None

    #this section is used by gunicorn to serve the app on Heroku
if __name__ == '__main__':
        app.run()
    
