# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:49:22 2024

@author: kburg
"""


#NEED TO RUN THIS FIRST IN ENVIRONMENT

#INSTALLATION OF KERAS OCR

#pip install -q keras-ocr

#uncomment below for setup
#pip install git+https://github.com/faustomorales/keras-ocr.git#egg=keras-ocr


#uncomment below for tensorflow setup
#pip install "tensorflow==2.15.1"

#pip install --force-reinstall -v "tensorflow==2.15.1"

import os 
import matplotlib.pyplot as plt
import zipfile
import sys
import pandas as pd
import csv
import keras_ocr


def process_image(leaflet_path, image_file, folder_name):
    leaflet_number = os.path.basename(leaflet_path).split('-')[-1].split('.')[0]
    pipeline = keras_ocr.pipeline.Pipeline()

    with zipfile.ZipFile(leaflet_path, 'r') as zip_ref:
        with zip_ref.open(image_file) as img_file:
            keras_image = keras_ocr.tools.read(img_file)
            predictions = pipeline.recognize([keras_image])[0]

    text = ' '.join([text for text, _ in predictions])
  #  print(f"Leaflet Number: {leaflet_number}, Image: {image_file}, Text: {text}, ElectionParty: {folder_name}")

if __name__ == "__main__":
    leaflet_path = sys.argv[1]
    image_file = sys.argv[2]
    folder_name = sys.argv[3]
    process_image(leaflet_path, image_file, folder_name)
    
    
    