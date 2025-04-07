# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:54:17 2024

@author: kburg
"""

#paper plots


import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import os

# Set the working directory
new_directory = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other'
os.chdir(new_directory)
print("Current working directory:", os.getcwd())

#making maps with environmental mentions

# Load CSV data
csv_file = "cluster/sorted_full_df_july4_5.csv"
df = pd.read_csv(csv_file)

# Load shapefile for constituencies
shapefile = "map2/westminster-parliamentary-constituencies.shp"
gdf = gpd.read_file(shapefile)

# Load England boundary GeoJSON file
england_boundary_path = "england-uk_1321.geojson"
gdf_england = gpd.read_file(england_boundary_path)

# Ensure the constituency names match the ones in the shapefile
df['constituency'] = df['Constituency'].str.lower().str.strip()
gdf['CONSTITUENCY'] = gdf['pcon22nm'].str.lower().str.strip()

# Merge the dataframes
merged_gdf = gdf.merge(df, left_on='CONSTITUENCY', right_on='constituency')

# Calculate mean environmental mentions per constituency
environment_mean = merged_gdf.groupby('CONSTITUENCY')['environment'].mean().reset_index()
environment_mean.columns = ['CONSTITUENCY', 'mean_environmental_mentions']

# Merge the mean data back into merged_gdf
merged_gdf = merged_gdf.merge(environment_mean, on='CONSTITUENCY', how='left')

# Create a new DataFrame without the 'environment' column
new_df = merged_gdf.drop(columns=['environment'])

# Drop duplicate rows
new_df = new_df.drop_duplicates()

# Define unique parties and election years
unique_parties = merged_gdf['Party'].unique()
unique_elections = merged_gdf['Election'].unique()

# Function to plot and save environmental mentions by constituency
def plot_and_save_environmental_mentions(data, output_folder, overall=False):
    os.makedirs(output_folder, exist_ok=True)
    
    if overall:
        # Plot overall constituency environmental mentions combined for all years and parties
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))
        
        data.plot(column='mean_environmental_mentions', 
                  cmap='Greys', 
                  linewidth=0.8, 
                  edgecolor='0.8', 
                  ax=ax, 
                  legend=True,
                  missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})
        
        gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')  # Add England boundary
        
        ax.set_title('Overall Mean Environmental Mentions by UK Constituency', fontdict={'fontsize': '15', 'fontweight' : '3'})
        ax.set_axis_off()
        
        output_file = os.path.join(output_folder, 'Overall_Environmental_Mentions.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
    else:
        for party in unique_parties:
            for election in unique_elections:
                subset_df = data[(data['Party'] == party) & (data['Election'] == election)]
                
                fig, ax = plt.subplots(1, 1, figsize=(15, 10))
                
                subset_df.plot(column='mean_environmental_mentions', 
                               cmap='Greys', 
                               linewidth=0.8, 
                               edgecolor='0.8', 
                               ax=ax, 
                               legend=True,
                               missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})
                
                gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')  # Add England boundary
                
                ax.set_title(f'Mean Environmental Mentions by UK Constituency ({party}, {election})', fontdict={'fontsize': '15', 'fontweight' : '3'})
                ax.set_axis_off()
                
                output_file = os.path.join(output_folder, f'{party}_{election}_Environmental_Mentions.png')
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                plt.close(fig)

# Plot overall environmental mentions combined for all years and parties
output_folder = './plots'
plot_and_save_environmental_mentions(new_df, output_folder, overall=True)

# Plot individual party and election combinations
plot_and_save_environmental_mentions(merged_gdf, output_folder, overall=False)



## fix the plot names



import os

# Define the directory containing your images
directory = r'C:\Users\kburg\OneDrive\Documents\Trinity\diss_all_other\plots'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if there is a space in the filename
    if ' ' in filename:
        # Create the new filename by replacing spaces with underscores
        new_filename = filename.replace(' ', '_')
        # Construct the full path for the old and new filenames
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_filename}')

print('Renaming completed.')


#%% accuracy scores of my model



import pandas as pd
#pip install scikit-learn
from sklearn import datasets
import statsmodels.api as sm
from stargazer.stargazer import Stargazer

# Assuming your DataFrame is named df and contains the necessary data

# Environment conditions
environment_condition = df['environment'] >= 1
environment_mentioned = df['Issues.Covered'].apply(lambda x: 'Environment' in x if pd.notna(x) else False)

# Calculate accuracy for Environment
correct_mentions_when_env_high = (environment_condition == environment_mentioned).sum()
total_mentions_when_env_high = len(df)
accuracy_when_env_high = correct_mentions_when_env_high / total_mentions_when_env_high

correct_mentions_when_mentioned = (environment_mentioned & environment_condition).sum()
total_mentions_when_mentioned = environment_mentioned.sum()
accuracy_when_mentioned = correct_mentions_when_mentioned / total_mentions_when_mentioned if total_mentions_when_mentioned > 0 else float('nan')

# Create a DataFrame for Environment accuracy scores
data_env = {
    'Condition': ["Accuracy when 'environment' is 1 or greater", "Accuracy when 'Environment' is mentioned"],
    'Count': [correct_mentions_when_env_high, correct_mentions_when_mentioned],
    'Total': [total_mentions_when_env_high, total_mentions_when_mentioned],
    'Accuracy': [f"{accuracy_when_env_high:.2%}", f"{accuracy_when_mentioned:.2%}"]
}

df_env = pd.DataFrame(data_env)

# Economy conditions
economy_condition = df['economy'] >= 1
economy_mentioned = df['Issues.Covered'].apply(lambda x: 'Economy' in x if pd.notna(x) else False)

# Calculate accuracy for Economy
correct_economy_mentions_when_high = (economy_condition == economy_mentioned).sum()
total_economy_mentions_when_high = len(df)
accuracy_economy_when_high = correct_economy_mentions_when_high / total_economy_mentions_when_high

correct_economy_mentions_when_mentioned = (economy_mentioned & economy_condition).sum()
total_economy_mentions_when_mentioned = economy_mentioned.sum()
accuracy_economy_when_mentioned = correct_economy_mentions_when_mentioned / total_economy_mentions_when_mentioned if total_economy_mentions_when_mentioned > 0 else float('nan')



print(f"Accuracy when 'environment' is 1 or greater: {accuracy_when_env_high:.2%}")
print(f"Number of correct mentions when 'environment' is 1 or greater: {correct_mentions_when_env_high}")
print(f"Total number of rows: {total_mentions_when_env_high}")

print(f"Accuracy when 'Environment' is mentioned: {accuracy_when_mentioned:.2%}")
print(f"Number of correct mentions when 'Environment' is mentioned: {correct_mentions_when_mentioned}")
print(f"Total number of 'Environment' mentions: {total_mentions_when_mentioned}")



print(f"Accuracy when 'economy' is 1 or greater: {accuracy_economy_when_high:.2%}")
print(f"Number of correct mentions when 'economy' is 1 or greater: {correct_economy_mentions_when_high}")
print(f"Total number of rows: {total_economy_mentions_when_high}")

print(f"Accuracy when 'Economy' is mentioned: {accuracy_economy_when_mentioned:.2%}")
print(f"Number of correct mentions when 'Economy' is mentioned: {correct_economy_mentions_when_mentioned}")
print(f"Total number of 'Economy' mentions: {total_economy_mentions_when_mentioned}")






# Create a DataFrame for Economy accuracy scores
data_econ = {
    'Condition': ["Accuracy when 'economy' is 1 or greater", "Accuracy when 'Economy' is mentioned"],
    'Count': [correct_economy_mentions_when_high, correct_economy_mentions_when_mentioned],
    'Total': [total_economy_mentions_when_high, total_economy_mentions_when_mentioned],
    'Accuracy': [f"{accuracy_economy_when_high:.2%}", f"{accuracy_economy_when_mentioned:.2%}"]
}

df_econ = pd.DataFrame(data_econ)

print(df_env.to_latex(index=False,
    formatters={"name": str.upper},
    float_format="{:.1f}".format,
    ))  

print(df_econ.to_latex(index=False,
    formatters={"name": str.upper},
    float_format="{:.1f}".format,
    ))  



#%% showing a leaflet as an example

import os 
import matplotlib.pyplot as plt
import zipfile
import sys
#pip install pandas
import pandas as pd
import csv

#print(sys.executable)

#INSTALLATION OF KERAS OCR

#pip install -q keras-ocr

#uncomment below for setup
#pip install git+https://github.com/faustomorales/keras-ocr.git#egg=keras-ocr


#uncomment below for tensorflow setup
#pip install "tensorflow==2.15.1"

#pip install --force-reinstall -v "tensorflow==2.15.1"


import keras_ocr


#CREATE PIPELINE

pipeline = keras_ocr.pipeline.Pipeline()


#SET WORKING DIRECTORY

new_directory = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other'
os.chdir(new_directory)

print("Current working directory:", os.getcwd())


#READING IMAGES ONE AT A TIME

image_filenames = ['28_1.jpg', '28_2.jpg']

# Construct full paths for each image
image_paths = [os.path.join(new_directory, filename) for filename in image_filenames]

# Print paths to confirm
for path in image_paths:
    print("Image path:", path)

# Read images from the constructed paths
images = [keras_ocr.tools.read(img_path) for img_path in image_paths]

# Optional: Print out the images to confirm they are loaded
print("Number of images loaded:", len(images))
# Read images from folder path to image object
images = [keras_ocr.tools.read(img_path) for img_path in image_paths]



# generate text predictions from the images
prediction_groups = pipeline.recognize(images)

prediction = pipeline.recognize(images)[0]


# Create subplots
fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))

# Ensure axs is always a list
if len(images) == 1:
    axs = [axs]

# Plot each image and its predictions
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

plt.show()


