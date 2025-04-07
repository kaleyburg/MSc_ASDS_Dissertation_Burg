# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 18:09:20 2024

@author: kburg
"""


# Missing numbers: [2563, 4331, 4427, 4486, 5700, 5943, 6170, 
# 8622, 8623, 9559, 12108, 12631]


#2563 was not a zip file
#4331 was rotated wrong - fixed
#4427 was rotated wrong - fixed
#4486 was rotated wrong - fixed
#5700 was rotated wrong - fixed
#5943 was rotated correctly but couldn't broadcast, cropped it and fixed
#6170 couldnt broadcast but was rotated correctly, cropped and fixed
#8622 saved as gif, fixed
#8623 saved as gif, fixed
#9559 was not zip file
#12108 was rotated wrong - fixed
#12631 was rotated wrong - fixed


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
#on desktop
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kburg\anaconda3\envs\boobs\Library\bin\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Users\kburg\anaconda3\envs\boobs\share\tessdata'


#loading things
#on cluster
#pytesseract.pytesseract.tesseract_cmd = '/home/users/burgk/.conda/envs/leafy/bin/tesseract'
#os.environ['TESSDATA_PREFIX'] = '/home/users/burgk/.conda/pkgs/tesseract-5.4.1-h776bbad_0/share/tessdata'





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
            try:
                results = pytesseract.image_to_osd(keras_image, output_type=pytesseract.Output.DICT)
                if 'rotate' in results:
                    rotation_angle = results["rotate"]
                    print(f"Original rotation angle: {rotation_angle} degrees")
                else:
                    rotation_angle = 0  # Default to no rotation if unable to detect angle
                    print("Unable to detect rotation angle. Assuming no rotation.")
            except Exception as e:
                print(f"Error detecting rotation angle with Tesseract: {e}")
                rotation_angle = 0  # Default to no rotation in case of error
            
            # Perform OCR on the original image or rotated image if necessary
            if rotation_angle == 90 or rotation_angle == 270:
                # Rotate the image using the detected rotation angle
                rotated_image = cv2.rotate(keras_image, cv2.ROTATE_90_CLOCKWISE if rotation_angle == 90 else cv2.ROTATE_90_COUNTERCLOCKWISE)
                predictions = pipeline.recognize([rotated_image])[0]
            else:
                # Use the original image without rotation
                predictions = pipeline.recognize([keras_image])[0]


    # Save the rotated image to the specified output folder
    output_filename = os.path.join(output_folder, f"rotated_image_{row_number}.jpg")
   # cv2.imwrite(output_filename, rotated_image)
    
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
   # input_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel.xlsx'
    output_folder = '/home/users/burgk/output3'
#    output_folder = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/cluster/output/output'  # Replace with your desired output folder

    start_index = (sysvariable) * 1
    end_index = sysvariable *1

    df = pd.read_excel(input_file)

   # for i in range(start_index, end_index):
  #      try:
   #         process_image_from_excel(i, output_folder, input_file)
    #    except Exception as e:
     #       print(f"Error processing row {i}: {str(e)}")
      #      traceback.print_exc()  # Print the traceback
       #     continue
    for i in range(start_index, end_index):
        process_image_from_excel(i, output_folder, input_file)



input_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel.xlsx'
output_folder = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/fortransfer'  # Replace with your desired output folder

#/cluster/output/output

process_image_from_excel(, output_folder, input_file)

# List of specific indices to process
indices_to_process = [4331, 4427, 4486, 5700, 5943, 6170, 8622, 8623, 12108, 12631]


# Loop through each index and call process_image_from_excel
for index in indices_to_process:
    process_image_from_excel(index, output_folder, input_file)


