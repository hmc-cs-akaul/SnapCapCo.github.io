from __future__ import division, print_function
import sys
import os
import glob
import re
import random
from pathlib import Path

# Import fast.ai Library
from fastai import *
from fastai.vision import *

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename



#load the model
def load_model(model_path):
    path = Path(model_path)
    # the classes for our model at the correct index it returns
    classes = ['anger', 'happy','neutral', 'sad']
    data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
    learn = create_cnn(data2, models.resnet34)
    learn.load('stage-3')
    return learn

def model_predict(img_path, model_path):
    """
       model_predict will return the preprocessed image
    """
    learn = load_model(model_path)
    img = open_image(img_path)
    # get the outputs from the model
    pred_class,pred_idx,outputs = learn.predict(img)
    # return the classification the model returns
    return pred_class
