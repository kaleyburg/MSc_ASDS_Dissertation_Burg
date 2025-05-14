# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:54:17 2024

@author: kburg
"""

#fix keras stuff and then run and fix the plots to make the paper look more professional


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
csv_file = "CSVandSHPfiles/sorted_full_df_july4_5.csv"
df = pd.read_csv(csv_file)

# Load shapefile for constituencies
shapefile = "CSVandSHPfiles/westminster-parliamentary-constituencies.shp"
gdf = gpd.read_file(shapefile)

# Load England boundary GeoJSON file
england_boundary_path = "CSVandSHPfiles/england-uk_1321.geojson"  # Replace with the correct GeoJSON file path
gdf_england = gpd.read_file("CSVandSHPfiles/england-uk_1321.geojson", engine="fiona")


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



# Function to plot and save environmental mentions
def plot_and_save_environmental_mentions(data, overall=False):
    # Base path: folder where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

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

        data.plot(column='mean_environmental_mentions', 
                  cmap='Greys', 
                  linewidth=0.8, 
                  edgecolor='0.8', 
                  ax=ax, 
                  legend=True,
                  missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})
        
        gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')
        ax.set_title('Overall Mean Environmental Mentions by UK Constituency', fontdict={'fontsize': '15', 'fontweight': '3'})
        ax.set_axis_off()

        filename = "Overall_Environmental_Mentions.png"
        output_file = os.path.join(output_folder, filename)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved overall plot to {os.path.abspath(output_file)}")


    

    else:
        unique_parties = data['Party'].unique()
        unique_elections = data['Election'].unique()

        for party in unique_parties:
            for election in unique_elections:
                print(f"Generating plot for {party} in {election}...")
                subset_df = data[(data['Party'] == party) & (data['Election'] == election)]

                if subset_df.empty:
                    print(f"No data for {party} in {election}, skipping.")
                    continue

                fig, ax = plt.subplots(1, 1, figsize=(15, 10))

                subset_df.plot(column='mean_environmental_mentions', 
                               cmap='Greys', 
                               linewidth=0.8, 
                               edgecolor='0.8', 
                               ax=ax, 
                               legend=True,
                               missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})

                gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')
                ax.set_title(f'Mean Environmental Mentions by UK Constituency ({party}, {election})', fontdict={'fontsize': '15', 'fontweight': '3'})
                ax.set_axis_off()

                safe_party = sanitize_filename(party)
                safe_election = sanitize_filename(election)
                filename = f"{safe_party}_{safe_election}_Environmental_Mentions.png"
                output_file = os.path.join(output_folder, filename)

                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                plt.close(fig)
                print(f"Saved plot to {os.path.abspath(output_file)}")


plot_and_save_environmental_mentions(new_df, overall=True)
plot_and_save_environmental_mentions(merged_gdf, overall=False)


# Function to plot and save environmental mentions with a narrower range
def plot_and_save_environmental_mentions_narrow(data):
    # Base path: folder where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define full output path
    output_folder = os.path.join(base_dir, "tex_files_withallimagesandbib", "plots")
    os.makedirs(output_folder, exist_ok=True)
    print("Output folder is:", os.path.abspath(output_folder))

    # Calculate the 90th percentile of mean environmental mentions
    max_value = data['mean_environmental_mentions'].quantile(0.9)

    # Filter data to include only values between 0 and the 90th percentile
    filtered_data = data[data['mean_environmental_mentions'] <= max_value]

    print("Generating narrow range plot...")
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    filtered_data.plot(column='mean_environmental_mentions', 
                       cmap='Greys', 
                       linewidth=0.8, 
                       edgecolor='0.8', 
                       ax=ax, 
                       legend=True,
                       missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})

    gdf_england.boundary.plot(ax=ax, linewidth=1, color='black')
    ax.set_title('Mean Environmental Mentions by UK Constituency (0 to 90th Percentile)', 
                 fontdict={'fontsize': '15', 'fontweight': '3'})
    ax.set_axis_off()

    filename = "Narrow_Range_Environmental_Mentions.png"
    output_file = os.path.join(output_folder, filename)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved narrow range plot to {os.path.abspath(output_file)}")

# Call the new function
plot_and_save_environmental_mentions_narrow(new_df)


#%% accuracy scores of my model


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


