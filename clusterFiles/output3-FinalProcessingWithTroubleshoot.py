# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 19:29:56 2024

@author: kburg
"""


import tensorflow as tf
import sys
import pandas as pd
import os
import zipfile
import keras_ocr
import traceback
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
from pytesseract import output
import argparse
import imutils
import re
import cv2



#loading things
#on cluster
pytesseract.pytesseract.tesseract_cmd = '/home/users/burgk/.conda/envs/leafy/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/home/users/burgk/.conda/pkgs/tesseract-5.4.1-h776bbad_0/share/tessdata'



def process_image_from_excel(row_number, output_folder, input_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Assuming the row_number is provided as an index, adjust accordingly
    if row_number >= len(df):
        raise ValueError(f"Row number {row_number} is out of range.")

    # Get information from the specified row
    leaflet_path = df.loc[row_number, 'leaflet_path']
    image_file = df.loc[row_number, 'image_file']  # Assuming 'image_file' is the column name for image file
    folder_name = df.loc[row_number, 'folder_name']

    # Process image with keras_ocr pipeline
    leaflet_number = os.path.basename(leaflet_path).split('-')[-1].split('.')[0]
    pipeline = keras_ocr.pipeline.Pipeline()

    with zipfile.ZipFile(leaflet_path, 'r') as zip_ref:
        with zip_ref.open(image_file) as img_file:
            keras_image = keras_ocr.tools.read(img_file)
            
            # Determine orientation using Tesseract
            rgb = cv2.cvtColor(keras_image, cv2.COLOR_BGR2RGB)
            results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)
            rotation_angle = results["rotate"]
            print(f"Rotation angle: {rotation_angle} degrees")
            
            # Rotate the image using the extracted rotation angle
            rotated_image = imutils.rotate_bound(keras_image, angle=rotation_angle)

            predictions = pipeline.recognize([rotated_image])[0]

    # Save the rotated image to the specified output folder
    output_filename = os.path.join(output_folder, f"rotated_image_{row_number}.jpg")
    cv2.imwrite(output_filename, rotated_image)
    
    print(f"Rotated image saved to '{output_filename}'")
    
    
    
    text = ' '.join([text for text, _ in predictions])

    # Save the output with the specified row number
    output_filename = os.path.join(output_folder, f"output_{row_number}.txt")
    with open(output_filename, 'w') as f:
        f.write(f"Leaflet Number: {leaflet_number}, Image: {image_file}, Text: {text}, Folder Name: {folder_name}")

    print(f"Processed image and saved output to '{output_filename}'")
    

    
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <sysvariable>")
        sys.exit(1)

    sysvariable = int(sys.argv[1])  # Convert command-line argument to integer
    input_file = '/home/users/burgk/scripts/xcel2.xlsx'
    output_folder = '/home/users/burgk/output3'  # Replace with your desired output folder

    for i in range((sysvariable-1)*50, sysvariable*50):  # Process rows based on sysvariable
        try:
            process_image_from_excel(i, output_folder, input_file)
        except Exception as e:
            print(f"Error processing row {i}: {str(e)}")
            continue




