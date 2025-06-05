# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:54:17 2024

@author: kburg
"""

#fix keras stuff and then run and fix the plots to make the paper look more professional

#fixed a lot of the plots to use the percentage of environmental words in the text, rather than the raw count
# %%
#paper plots

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import os
import zipfile
import sys
import csv


# Set the working directory
new_directory = "C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg"
os.chdir(new_directory)
print("Current working directory:", os.getcwd())

#making maps with environmental mentions
# Load CSV data
csv_file = "CSVandSHPfiles/model_data_revision2.csv"
df = pd.read_csv(csv_file)
print(df.columns)

# Load shapefile for constituencies
shapefile = "CSVandSHPfiles/westminster-parliamentary-constituencies.shp"
gdf = gpd.read_file(shapefile)

# Load England boundary GeoJSON file
england_boundary_path = "CSVandSHPfiles/england-uk_1321.geojson"  # Replace with the correct GeoJSON file path
gdf_england = gpd.read_file("CSVandSHPfiles/england-uk_1321.geojson", engine="fiona")

# Ensure the constituency names match the ones in the shapefile
df['constituency'] = df['constituency'].str.lower().str.strip()
gdf['CONSTITUENCY'] = gdf['pcon22nm'].str.lower().str.strip()

# Merge the dataframes
merged_gdf = gdf.merge(df, left_on='CONSTITUENCY', right_on='constituency')

# Calculate average environmental word percentage per constituency
environment_word_pct_mean = merged_gdf.groupby('CONSTITUENCY')['environment_word_pct'].mean().reset_index()
environment_word_pct_mean.columns = ['CONSTITUENCY', 'avg_environment_word_pct']

# Merge the average data back into merged_gdf
merged_gdf = merged_gdf.merge(environment_word_pct_mean, on='CONSTITUENCY', how='left')

# Create a new DataFrame without the 'environment_word_pct' column
new_df = merged_gdf.drop(columns=['environment_word_pct'])

# Drop duplicate rows
new_df = new_df.drop_duplicates()

# Define unique parties
unique_parties = merged_gdf['Party'].unique()

# Function to plot and save environmental word percentage
def plot_and_save_environment_word_pct(data, overall=False):
    # Base path: folder where this script is located
    base_dir = os.getcwd()

    # Define full output path
    output_folder = os.path.join(base_dir, "tex_files_withallimagesandbib", "plots")
    os.makedirs(output_folder, exist_ok=True)
    print("Output folder is:", os.path.abspath(output_folder))

    # Function to clean up file names
    def sanitize_filename(text):
        return text.strip().replace(" ", "_").replace("/", "_")

    if overall:
        print("Generating overall plot...")
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))

        data.plot(column='avg_environment_word_pct', 
                  cmap='Greys', 
                  linewidth=0.8, 
                  edgecolor='0.8', 
                  ax=ax, 
                  legend=True,
                  missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})
        
        gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')
        ax.set_title('Overall Average Environmental Word Percentage by UK constituency', fontdict={'fontsize': '15', 'fontweight': '3'})
        ax.set_axis_off()

        filename = "Overall_Environmental_Word_Percentage.png"
        output_file = os.path.join(output_folder, filename)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved overall plot to {os.path.abspath(output_file)}")

    else:
        for party in unique_parties:
            print(f"Generating plot for {party}...")
            subset_df = data[data['Party'] == party]

            if subset_df.empty:
                print(f"No data for {party}, skipping.")
                continue

            fig, ax = plt.subplots(1, 1, figsize=(15, 10))

            subset_df.plot(column='avg_environment_word_pct', 
                           cmap='Greys', 
                           linewidth=0.8, 
                           edgecolor='0.8', 
                           ax=ax, 
                           legend=True,
                           missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})

            gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')
            ax.set_title(f'Average Environmental Word Percentage by UK constituency ({party})', fontdict={'fontsize': '15', 'fontweight': '3'})
            ax.set_axis_off()

            safe_party = sanitize_filename(party)
            filename = f"{safe_party}_Environmental_Word_Percentage.png"
            output_file = os.path.join(output_folder, filename)

            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close(fig)
            print(f"Saved plot to {os.path.abspath(output_file)}")

plot_and_save_environment_word_pct(new_df, overall=True)
plot_and_save_environment_word_pct(merged_gdf, overall=False)


#i dont think i need this - dont run

# Function to plot and save environmental word percentage with a narrower range
def plot_and_save_environment_word_pct_narrow(data):
    # Base path: folder where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define full output path
    output_folder = os.path.join(base_dir, "tex_files_withallimagesandbib", "plots")
    os.makedirs(output_folder, exist_ok=True)
    print("Output folder is:", os.path.abspath(output_folder))

    # Calculate the 90th percentile of average environmental word percentage
    max_value = data['avg_environment_word_pct'].quantile(0.9)

    # Filter data to include only values between 0 and the 90th percentile
    filtered_data = data[data['avg_environment_word_pct'] <= max_value]

    print("Generating narrow range plot...")
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    filtered_data.plot(column='avg_environment_word_pct', 
                       cmap='Greys', 
                       linewidth=0.8, 
                       edgecolor='0.8', 
                       ax=ax, 
                       legend=True,
                       missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})

    gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')
    ax.set_title('Average Environmental Word Percentage by UK constituency (0 to 90th Percentile)', 
                 fontdict={'fontsize': '15', 'fontweight': '3'})
    ax.set_axis_off()

    filename = "Narrow_Range_Environmental_Word_Percentage.png"
    output_file = os.path.join(output_folder, filename)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved narrow range plot to {os.path.abspath(output_file)}")

# Call the new function
plot_and_save_environment_word_pct_narrow(new_df)
