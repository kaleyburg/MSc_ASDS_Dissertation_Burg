# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 16:43:01 2024

@author: kburg
"""


#%%setup

import os 
import matplotlib.pyplot as plt
import zipfile
import pandas as pd
#pip install geopandas
import geopandas as gpd
#pip install folium
#import folium
from shapely import wkt
from shapely.geometry import Polygon
import numpy as np
from datetime import datetime, timedelta
import re
import meteostat
from datetime import datetime
from meteostat import Point, Daily, Stations, Monthly
from shapely.geometry import Point
from meteostat import Point, Daily

import logging
#pip install statsmodels.api
import statsmodels.api as sm

#pip install geocode-ss
from geocode import Geocoder

#pip install openpyxl
import openpyxl



new_directory = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other'
os.chdir(new_directory)

print("Current working directory:", os.getcwd())


#%%load data and check accuracy
#very rough code to troublshoot, visualize, and create plots
#THIS IS WRONG
# Load CSV data
csv_file = "C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/cluster/sorted_full_df_july4_5.csv"
df = pd.read_csv(csv_file)

df.columns

df['Mentions']

df['Issues.Covered']
df['environment']
df['economy']
df['culture']


#p check accuracy


# Condition for 'environment' column being 1 or greater
environment_condition = df['environment'] >= 1

# Condition for 'Environment' being in 'Issues.Covered'
environment_mentioned = df['Issues.Covered'].apply(lambda x: 'Environment' in x if pd.notna(x) else False)

# Calculate accuracy for both conditions
correct_mentions_when_env_high = (environment_condition == environment_mentioned).sum()
total_mentions_when_env_high = len(df)

accuracy_when_env_high = correct_mentions_when_env_high / total_mentions_when_env_high

# Calculate how often 'environment' is 1 or greater when 'Environment' is mentioned
correct_mentions_when_mentioned = (environment_mentioned & environment_condition).sum()
total_mentions_when_mentioned = environment_mentioned.sum()

accuracy_when_mentioned = correct_mentions_when_mentioned / total_mentions_when_mentioned if total_mentions_when_mentioned > 0 else np.nan

print(f"Accuracy when 'environment' is 1 or greater: {accuracy_when_env_high:.2%}")
print(f"Number of correct mentions when 'environment' is 1 or greater: {correct_mentions_when_env_high}")
print(f"Total number of rows: {total_mentions_when_env_high}")

print(f"Accuracy when 'Environment' is mentioned: {accuracy_when_mentioned:.2%}")
print(f"Number of correct mentions when 'Environment' is mentioned: {correct_mentions_when_mentioned}")
print(f"Total number of 'Environment' mentions: {total_mentions_when_mentioned}")

# Identify leaflets where 'Environment' is mentioned but 'environment' is not 1 or greater
incorrect_environment_mentions = df[environment_mentioned & ~environment_condition]

# Print specific columns for incorrect environment mentions
print("\nLeaflets where 'Environment' is mentioned but 'environment' is not 1 or greater:")
print(incorrect_environment_mentions[['Leaflet.Number', 'Election', 'Issues.Covered', 'environment']])



df.columns
#and for economy too as sanity check



#test CORRECT WAY TO DO IT


# Condition for 'environment' column being 1 or greater
environment_condition = df['environment'] >= 1

# Assuming the boolean series `environment_mentioned` is provided
# It indicates whether 'Environment' is mentioned in 'Issues.Covered'

# 1. Accuracy when 'Environment' is mentioned in 'Issues.Covered':
correct_when_env_mentioned = (environment_mentioned & environment_condition).sum()
total_env_mentions_in_issues_covered = environment_mentioned.sum()

accuracy_when_env_mentioned = correct_when_env_mentioned / total_env_mentions_in_issues_covered if total_env_mentions_in_issues_covered > 0 else np.nan

print(f"Accuracy of detecting environment (score 1 or greater) when 'Environment' is mentioned in 'Issues.Covered': {accuracy_when_env_mentioned:.2%}")
print(f"Number of correct mentions when 'Environment' is mentioned: {correct_when_env_mentioned}")
print(f"Total number of 'Environment' mentions in 'Issues.Covered': {total_env_mentions_in_issues_covered}")

# 2. Accuracy when 'environment' is 1 or greater:
correct_when_env_high = (environment_mentioned & environment_condition).sum()
total_env_high = environment_condition.sum()

accuracy_when_env_high = correct_when_env_high / total_env_high if total_env_high > 0 else np.nan

print(f"Accuracy of 'Environment' being mentioned in 'Issues.Covered' when environment score is 1 or greater: {accuracy_when_env_high:.2%}")
print(f"Number of correct mentions when environment score is 1 or greater: {correct_when_env_high}")
print(f"Total number of times environment score is 1 or greater: {total_env_high}")

# Identify rows where 'Environment' is mentioned but 'environment' is not 1 or greater
incorrect_mentions_env_in_issues = df[environment_mentioned & ~environment_condition]

# Print specific columns for incorrect environment mentions
print("\nLeaflets where 'Environment' is mentioned but 'environment' is not 1 or greater:")
print(incorrect_mentions_env_in_issues[['Leaflet.Number', 'Election', 'Issues.Covered', 'environment']])

# Identify rows where 'environment' is 1 or greater but 'Environment' is not mentioned
incorrect_mentions_env_high = df[environment_condition & ~environment_mentioned]

print("\nLeaflets where 'environment' is 1 or greater but 'Environment' is not mentioned:")
print(incorrect_mentions_env_high[['Leaflet.Number', 'Election', 'Issues.Covered', 'environment']])



#ECONOMY CORRECTLY


# Condition for 'economy' column being 1 or greater
economy_condition = df['economy'] >= 1

# Assuming the boolean series `economy_mentioned` is generated
# It indicates whether 'Economy' is mentioned in 'Issues.Covered'
economy_mentioned = df['Issues.Covered'].apply(lambda x: 'Economy' in x if pd.notna(x) else False)

# 1. Accuracy when 'Economy' is mentioned in 'Issues.Covered':
correct_when_economy_mentioned = (economy_mentioned & economy_condition).sum()
total_economy_mentions_in_issues_covered = economy_mentioned.sum()

accuracy_when_economy_mentioned = correct_when_economy_mentioned / total_economy_mentions_in_issues_covered if total_economy_mentions_in_issues_covered > 0 else np.nan

print(f"Accuracy of detecting economy (score 1 or greater) when 'Economy' is mentioned in 'Issues.Covered': {accuracy_when_economy_mentioned:.2%}")
print(f"Number of correct mentions when 'Economy' is mentioned: {correct_when_economy_mentioned}")
print(f"Total number of 'Economy' mentions in 'Issues.Covered': {total_economy_mentions_in_issues_covered}")

# 2. Accuracy when 'economy' is 1 or greater:
correct_when_economy_high = (economy_mentioned & economy_condition).sum()
total_economy_high = economy_condition.sum()

accuracy_when_economy_high = correct_when_economy_high / total_economy_high if total_economy_high > 0 else np.nan

print(f"Accuracy of 'Economy' being mentioned in 'Issues.Covered' when economy score is 1 or greater: {accuracy_when_economy_high:.2%}")
print(f"Number of correct mentions when economy score is 1 or greater: {correct_when_economy_high}")
print(f"Total number of times economy score is 1 or greater: {total_economy_high}")

# Identify rows where 'Economy' is mentioned but 'economy' is not 1 or greater
incorrect_mentions_economy_in_issues = df[economy_mentioned & ~economy_condition]

# Print specific columns for incorrect economy mentions
print("\nLeaflets where 'Economy' is mentioned but 'economy' is not 1 or greater:")
print(incorrect_mentions_economy_in_issues[['Leaflet.Number', 'Election', 'Issues.Covered', 'economy']])

# Identify rows where 'economy' is 1 or greater but 'Economy' is not mentioned
incorrect_mentions_economy_high = df[economy_condition & ~economy_mentioned]

print("\nLeaflets where 'economy' is 1 or greater but 'Economy' is not mentioned:")
print(incorrect_mentions_economy_high[['Leaflet.Number', 'Election', 'Issues.Covered', 'economy']])



##

## THIS IS ALSO WRONG

# Economy conditions
economy_condition = df['economy'] >= 1
economy_mentioned = df['Issues.Covered'].apply(lambda x: 'Economy' in x if pd.notna(x) else False)

# Calculate accuracy for Economy
correct_economy_mentions_when_high = (economy_condition == economy_mentioned).sum()
total_economy_mentions_when_high = len(df)
accuracy_economy_when_high = correct_economy_mentions_when_high / total_economy_mentions_when_high

correct_economy_mentions_when_mentioned = (economy_mentioned & economy_condition).sum()
total_economy_mentions_when_mentioned = economy_mentioned.sum()
accuracy_economy_when_mentioned = correct_economy_mentions_when_mentioned / total_economy_mentions_when_mentioned if total_economy_mentions_when_mentioned > 0 else np.nan

print(f"Accuracy when 'economy' is 1 or greater: {accuracy_economy_when_high:.2%}")
print(f"Number of correct mentions when 'economy' is 1 or greater: {correct_economy_mentions_when_high}")
print(f"Total number of rows: {total_economy_mentions_when_high}")

print(f"Accuracy when 'Economy' is mentioned: {accuracy_economy_when_mentioned:.2%}")
print(f"Number of correct mentions when 'Economy' is mentioned: {correct_economy_mentions_when_mentioned}")
print(f"Total number of 'Economy' mentions: {total_economy_mentions_when_mentioned}")



#%% Load shapefile for consituencies, merge, and mapping mentions by area
shapefile = "C:map2/westminster-parliamentary-constituencies.shp"
gdf = gpd.read_file(shapefile)

gdf.columns

gdf['pcon22nm']
df.columns


# Ensure the constituency names match the ones in the shapefile
# This may involve some preprocessing, such as converting to lower case or stripping whitespace
df['constituency'] = df['Constituency'].str.lower().str.strip()
gdf['CONSTITUENCY'] = gdf['pcon22nm'].str.lower().str.strip()



# Check the unique constituency names in both datasets
print("\nUnique Constituencies in CSV:")
print(df['constituency'].unique())
print("\nUnique Constituencies in Shapefile:")
print(gdf['CONSTITUENCY'].unique())

# Merge the dataframes
merged_gdf = gdf.merge(df, left_on='CONSTITUENCY', right_on='constituency')

merged_gdf.columns
merged_gdf['Constituency']
merged_gdf['CONSTITUENCY']
merged_gdf['geometry']


# Print the geometry for point 1
print(merged_gdf.loc[1, 'geometry'])


# #%% plot stuff

# # Save the DataFrame to a CSV file
# merged_gdf.to_csv('mapstuff.csv', index=False)


# Plotting the data
fig, ax = plt.subplots(1, 1, figsize=(15, 10))


#this works!
# Plot the constituencies, shading by environmental_mentions
merged_gdf.plot(column='environment', 
                cmap='YlGn', 
                linewidth=0.8, 
                edgecolor='0.8', 
                ax=ax, 
                legend=True)

# Customize the plot
ax.set_title('Environmental Mentions by UK Constituency', fontdict={'fontsize': '15', 'fontweight' : '3'})
ax.set_axis_off()

# Show the plot
plt.show()

type(merged_gdf['constituency'])


# Aggregate data to get the average environmental mentions per constituency
environment_mean = merged_gdf.groupby('constituency')['environment'].mean().reset_index()
environment_mean.columns = ['constituency', 'mean_environmental_mentions']





# Merge the aggregated data back into merged_gdf
merged_gdf = merged_gdf.merge(environment_mean, on='constituency', how='left')

# Create a new DataFrame without the 'environment' column
new_df = merged_gdf.drop(columns=['environment'])

new_df = merged_gdf

# Drop duplicate rows
new_df = new_df.drop_duplicates()

print(new_df.head())


new_df['mean_environmental_mentions']


new_df.columns



# Plotting the data
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Plot the constituencies, shading by environmental_mentions
new_df.plot(column='mean_environmental_mentions', 
                cmap='YlGn', 
                linewidth=0.8, 
                edgecolor='0.8', 
                ax=ax, 
                legend=True)

# Customize the plot
ax.set_title('Mean Environmental Mentions by UK Constituency', fontdict={'fontsize': '15', 'fontweight' : '3'})
ax.set_axis_off()

# Show the plot
plt.show()



# Define unique parties and election years
unique_parties = merged_gdf['Party'].unique()
unique_elections = merged_gdf['Election'].unique()

# Loop through each combination of Party and Election
for party in unique_parties:
    for election in unique_elections:
        # Filter the data based on Party and Election
        subset_df = merged_gdf[(merged_gdf['Party'] == party) & (merged_gdf['Election'] == election)]
        
        # Plotting the data
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))

        # Plot the constituencies, shading by environmental_mentions
        subset_df.plot(column='mean_environmental_mentions', 
                            cmap='YlGn', 
                            linewidth=0.8, 
                            edgecolor='0.8', 
                            ax=ax, 
                            legend=True)

        # Customize the plot
        ax.set_title(f'Mean Environmental Mentions by UK Constituency ({party}, {election})', fontdict={'fontsize': '15', 'fontweight' : '3'})
        ax.set_axis_off()

        # Show the plot
        plt.show()





#%%plots for report --important part


# Plotting the overall constituency environmental mentions combined for all years and parties
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Plot the constituencies, shading by mean_environmental_mentions
merged_gdf.plot(column='mean_environmental_mentions', 
                cmap='YlGn', 
                linewidth=0.8, 
                edgecolor='0.8', 
                ax=ax, 
                legend=True,
                missing_kwds={'color': 'red', 'label': 'No Data', 'edgecolor': 'black'})

# Customize the plot
ax.set_title('Overall Mean Environmental Mentions by UK Constituency', fontdict={'fontsize': '15', 'fontweight' : '3'})
ax.set_axis_off()

plt.show()


#trying again bc doesnt look good


# Manually set vmin and vmax to focus on a specific range of data
vmin = 0  # Minimum value for color scale
vmax = merged_gdf['mean_environmental_mentions'].quantile(0.90)  # Focus on the lower 90% of data

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Plot the constituencies, shading by mean_environmental_mentions
merged_gdf.plot(column='mean_environmental_mentions', 
                cmap='YlGn',  # Or try a different color map like 'OrRd' or 'PuBuGn'
                linewidth=0.8, 
                edgecolor='0.8', 
                ax=ax, 
                legend=True,
                vmin=vmin,
                vmax=vmax,
                missing_kwds={'color': 'red', 'label': 'No Data', 'edgecolor': 'black'})



ax.set_axis_off()

plt.show()


output_folder = './plots'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

output_file = os.path.join(output_folder, 'Overall_Environmental_Mentions.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# Close the figure to prevent memory issues
plt.close(fig)


# Loop through each combination of Party and Election
for party in unique_parties:
    for election in unique_elections:
        # Filter the data based on Party and Election
        subset_df = merged_gdf[(merged_gdf['Party'] == party) & (merged_gdf['Election'] == election)]
        
        # Plotting the data
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))

        # Plot the constituencies, shading by mean_environmental_mentions
        subset_df.plot(column='mean_environmental_mentions', 
                       cmap='YlGn', 
                       linewidth=0.8, 
                       edgecolor='0.8', 
                       ax=ax, 
                       legend=True,
                       missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})

        # Customize the plot
     #   ax.set_title(f'Mean Environmental Mentions by UK Constituency ({party}, {election})', fontdict={'fontsize': '15', 'fontweight' : '3'})
        ax.set_axis_off()

        # Save the plot
        output_file = os.path.join(output_folder, f'{party}_{election}_Environmental_Mentions.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')

        # Close the figure to prevent memory issues
        plt.close(fig)

plt.show()


#fix titles

# Specify the directory containing the images
output_folder = './plots' # Replace with your output folder path

# Loop through all files in the directory
for filename in os.listdir(output_folder):
    # Check if the file is an image and contains spaces
    if filename.endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp')) and ' ' in filename:
        # Create the new file name by replacing spaces with '2'
        new_filename = filename.replace('__', '_')
        old_filepath = os.path.join(output_folder, filename)
        new_filepath = os.path.join(output_folder, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f'Renamed: {filename} -> {new_filename}')

print("Image file renaming complete.")


#trying it again -  fixing minor things

# Loop through each combination of Party and Election
for party in unique_parties:
    for election in unique_elections:
        # Filter the data based on Party and Election
        subset_df = merged_gdf[(merged_gdf['Party'] == party) & (merged_gdf['Election'] == election)]
        
        # Remove spaces from the party and election names for the output file name
        party_no_spaces = party.replace(' ', '')
        election_no_spaces = election.replace(' ', '')

        # Plotting the data
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))  # Ensure the size is consistent

        # Plot the constituencies, shading by mean_environmental_mentions in grayscale
        im = subset_df.plot(column='mean_environmental_mentions', 
                            cmap='Greys',  # Use grayscale color map
                            linewidth=0.8, 
                            edgecolor='0.8', 
                            ax=ax, 
                            legend=True,
                            missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'})

        # Get the colorbar and set its properties to black and white
        cbar = im.get_figure().get_axes()[1]  # Get the colorbar axis
        cbar.set_facecolor('white')  # Set the background color of the colorbar
        for label in cbar.get_xticklabels() + cbar.get_yticklabels():
            label.set_color('black')  # Set the color of colorbar labels to black
        
        # Customize the plot
        ax.set_axis_off()

        # Save the plot with spaces in party and election names removed
        output_file = os.path.join(output_folder, f'{party_no_spaces}_{election_no_spaces}_Environmental_Mentions.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.1)
      #  plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f'Saved plot: {output_file}')

        # Close the figure to prevent memory issues
        plt.close(fig)

print("All plots have been saved successfully.")

#



#%%

#%% getting centers of constituencies
#
#pip install geocode-ss
#https://github.com/SheffieldSolar/Geocode


points = pd. DataFrame()

def get_center(constituencies):
    with Geocoder() as geocoder:
        # Geocode the provided constituencies
        print("GEOCODE CONSTITUENCIES:")
        results = geocoder.geocode_constituency(constituencies)
        print(results)
     #   for constituency, (lat, lon) in zip(constituencies, results):
        #    print(f"    Constituency: `{constituency}`  ->  {lat:.3f}, {lon:.3f}")
        points['results'] = results
        points['const'] = constituencies


consts = merged_gdf['constituency'].unique()
consts = consts.tolist()


get_center(consts)


points

# Merge the dataframes
merged_gdf = merged_gdf.merge(points, left_on='CONSTITUENCY', right_on='const')

merged_gdf['const']
merged_gdf['CONSTITUENCY']

(merged_gdf['const'] == merged_gdf['CONSTITUENCY']).all()

type(merged_gdf['Election'])


# Strip whitespace
merged_gdf['Election'] = merged_gdf['Election'].str.strip()


election_dates = [
    datetime(2010, 5, 6),
    datetime(2015, 5, 7),
    datetime(2017, 6, 8),
    datetime(2019, 12, 12)
]


year_before_election = [date - timedelta(days=365) for date in election_dates]



# Define corresponding labels for each election
election_labels = [
    '2010 General Election',
    '2015 General Election',
    '2017 General Election',
    '2019 General Election'
]

type(election_labels)



election_df = pd.DataFrame({
    'Election Date': election_dates,
    'Year Before Election': year_before_election,
    'Election': election_labels
})



print("Unique values in merged_gdf['Election']: ", merged_gdf['Election'].unique())
print("Unique values in election_df['Election']: ", election_df['Election'].unique())

# election_df with merged_gdf based on 'Election' column
merged_gdf = merged_gdf.merge(election_df[['Election', 'Election Date', 'Year Before Election']], on='Election', how='left')




# Convert 'Year Before Election' and 'Election Date' to datetime objects
merged_gdf['Year Before Election'] = pd.to_datetime(merged_gdf['Year Before Election'])
merged_gdf['Election Date'] = pd.to_datetime(merged_gdf['Election Date'])

# Extract unique location tuples

unique_results = merged_gdf['results'].unique()


unique_results_df = pd.DataFrame(unique_results, columns=['location'])



# Initialize an empty DataFrame to store monthly data
monthly_data_df = pd.DataFrame()


type(unique_results[0])

len(merged_gdf['results'].unique())


#%% try again - think this worked


# Initialize an empty list to store dataframes
dfs = []

# Loop through each unique location tuple
for location_tuple in merged_gdf['results'].unique():
    x, y = location_tuple  # Unpack the tuple
    coords = x, y
    print(location_tuple)

    # Find the corresponding row in merged_gdf for the current location_tuple
    row = merged_gdf.loc[(merged_gdf['results'] == location_tuple)].iloc[0]
    
    # Extract start and end dates from the row
    start = row['Year Before Election']
    end = row['Election Date']
    
    # Set the radius for the Point (assuming Point is defined elsewhere)
    Point.radius = 200000
    
    # Create a Point object for the current location
    location_point = Point(x, y)
    
    # Assuming 'start' and 'end' are defined somewhere in your code
    # Fetch monthly data using the Monthly class
    data = Monthly(location_point, start, end).fetch()
    
    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)


    df['x_coordinate'] = x
    df['y_coordinate'] = y

  #  print(df)
    # Append the fetched data to the list of dataframes
    dfs.append(df)
  #  print(dfs)


# Concatenate all dataframes in dfs
result_df = pd.concat(dfs, ignore_index=False)

result_df.columns
result_df.index

result_df['date'] = result_df.index

#%%test
# Step 1: Filter data for the specific date
test_date = '2009-05-01'  # Change this to the date you want to test

filtered_data = result_df[result_df.index == test_date]

# #%% plot averages
# # Step 2: Plotting
# plt.figure(figsize=(10, 8))

# # Adjust the colormap as needed
# cmap = 'viridis'  # Example colormap, change as desired
# vmin, vmax = filtered_data['prcp'].min(), filtered_data['prcp'].max()

# # Scatter plot with color mapped to precipitation values
# scatter = plt.scatter(filtered_data['x_coordinate'], filtered_data['y_coordinate'],
#                       c=filtered_data['prcp'], cmap=cmap, vmin=vmin, vmax=vmax, marker='o', edgecolors='k')

# plt.colorbar(scatter, label='Precipitation')
# plt.title(f'Precipitation on {test_date}')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.tight_layout()
# plt.show()



#%% merging weather data back

#trying to merge dataframes

merged_gdf.columns
merged_gdf['results']
result_df.columns



result_df['coordinates'] = list(zip(result_df['x_coordinate'], result_df['y_coordinate']))



print(result_df.head())


#result_df with merged_gdf based on 'coordinates' and 'results'
merged_data = pd.merge(result_df, merged_gdf, left_on='coordinates', right_on='results', how='inner')



# Check if 'coordinates' and 'results' are equal
coordinates_equal = (merged_data['coordinates'] == merged_data['results']).all()
# Print the result
if coordinates_equal:
    print("Coordinates and results are equal in merged_data")
else:
    print("Coordinates and results are not equal in merged_data")


merged_data.columns





#%% get yearly avgs



#convert 'Election Date' and 'Year Before Election' to datetime if they are not already
merged_data['Election Date'] = pd.to_datetime(merged_data['Election Date'])
merged_data['Year Before Election'] = pd.to_datetime(merged_data['Year Before Election'])

#list to store the yearly averages
yearly_averages = []

#loop through unique coordinates
for coord in merged_data['coordinates'].unique():
    group_data = merged_data[merged_data['coordinates'] == coord]
    location_info = group_data.iloc[0]
    filtered_data = group_data[(group_data['date'] >= location_info['Year Before Election']) & (group_data['date'] <= location_info['Election Date'])]
    yearly_avg = filtered_data[['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'tsun']].mean()
    yearly_avg['coordinates'] = location_info['coordinates']
    yearly_averages.append(yearly_avg)

# Convert the list of dictionaries to DataFrame
yearly_averages_df = pd.DataFrame(yearly_averages)


# Rename columns 
yearly_averages_df = yearly_averages_df.rename(columns={
    'tavg': 'yearly_avg_tavg',
    'tmin': 'yearly_avg_tmin',
    'tmax': 'yearly_avg_tmax',
    'prcp': 'yearly_avg_prcp',
    'wspd': 'yearly_avg_wspd',
    'pres': 'yearly_avg_pres',
    'tsun': 'yearly_avg_tsun',
    'coordinates': 'coordinates'
})

# Merge yearly averages back to the original merged_data DataFrame
merged_data = pd.merge(merged_data, yearly_averages_df, on='coordinates', how='left')




# List of columns to drop
columns_to_drop = ['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'tsun', 'x_coordinate',
                   'y_coordinate', 'date', 'coordinates', 'fid', 'pcon22cd', 'pcon22nm',
                   'bng_e', 'bng_n', 'long', 'lat', 'globalid', 'shape_leng', 'shape_area',
                   'geometry', 'CONSTITUENCY', 'Leaflet.Number', 'Mentions', 'Issues.Covered',
                   'ElectionParty', 'CombinedText', 'culture', 'economy', 'groups',
                   'institutions', 'law_and_order', 'rural', 'urban', 'values',
                   'Constituency', 'results', 'const']

simplified_df = merged_data.drop(columns=columns_to_drop)

# Print the new DataFrame
print(simplified_df)

# Remove duplicate rows
simplified_df = simplified_df.drop_duplicates()

# Print the simplified and deduplicated DataFrame
print(simplified_df)



simplified_df.to_csv('simple_df.csv', index=False)


#%% adding other controls -- did this in R instead

#pip install pandas numpy scipy patsy
#pip uninstall requests charset_normalizer
#pip install requests charset_normalizer

#pip install --force-reinstall charset-normalizer==3.1.0

#pip install pandas statsmodels


#os.chdir('C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other')

# Read the CSV files
df = pd.read_csv("simple_df.csv")
#df = simplified_df

# Display the first few rows of the data table
print(df.head())
print(df.columns)

# # Create the regression model
# X = df[['yearly_avg_tavg', 'yearly_avg_tmin', 'yearly_avg_tmax', 'yearly_avg_prcp', 'yearly_avg_wspd', 'yearly_avg_pres', 'yearly_avg_tsun']]
# y = df['environment']
# X = sm.add_constant(X)  # Adds a constant term to the predictor

# model = sm.OLS(y, X).fit()

# # Summarize the model
# print(model.summary())

# Read the census data
census = pd.read_csv("custom-filtered-2024-07-08T20_38_56Z.csv")
print(census.columns)

# Rename the constituency column in census data
census.rename(columns={"Westminster Parliamentary constituencies": "constituency"}, inplace=True)


# Convert constituency names to lowercase in both dataframes
df['constituency'] = df['constituency'].str.lower()
census['constituency'] = census['constituency'].str.lower()


# Define columns to keep based on ending with "Code"
columns_to_keep = [col for col in census.columns if col.endswith('Code')]

# Include additional essential columns
essential_columns = ['constituency', 'Observation']  # Add other columns if necessary

# Combine columns to keep
columns_to_keep.extend(essential_columns)

# Subset merged_df to keep only the desired columns
census = census[columns_to_keep]

# Verify the updated DataFrame
print(census.columns)

census = census.drop(columns='Westminster Parliamentary constituencies Code')





# Read the election results data
election_res = pd.read_csv("1918-2019election_results.csv", encoding='utf-8')
#election_res = pd.read_csv("1918-2019election_results.csv", encoding='utf-8')
#election_res = pd.read_csv("1918-2019election_results.csv", encoding='latin1')





print(election_res.head())
election_res.columns
election_res['country/region']

election_res['election'].unique


# Convert 'election' column to numeric type
election_res['election'] = pd.to_numeric(election_res['election'], errors='coerce')

# Filter based on numeric comparison
subset_election_res = election_res[(election_res['election'] >= 2010) & (election_res['election'] <= 2019)]

subset_election_res = subset_election_res[~subset_election_res['country/region'].isin(["Scotland", "Wales", "Northern Ireland"])]
print(subset_election_res.head())
election_res['election']


# Check if all values in 'natSW_votes' and 'natSW_share' are NA and remove those columns if so
if subset_election_res['natSW_votes'].isna().all() and subset_election_res['natSW_share'].isna().all():
    subset_election_res.drop(columns=['natSW_votes', 'natSW_share'], inplace=True)

print(subset_election_res.head())
subset_election_res.columns

# Rename constituency column in election results data
subset_election_res.rename(columns={"constituency_name": "constituency"}, inplace=True)
subset_election_res['constituency'] = subset_election_res['constituency'].str.lower()
print(subset_election_res.head())

subset_election_res['constituency']

# Define columns to drop
columns_to_drop = ['constituency_id', 'seats', 'country/region', 'electorate',
                   'con_votes', 'lib_votes ', 'lab_votes', 'oth_votes',
                   'turnout ', 'boundary_set', 'Unnamed: 19']

# Drop columns from merged_df
election = subset_election_res.drop(columns=columns_to_drop)

# Verify the updated DataFrame
print(election.columns)



census.columns




df.columns


full_data = pd.DataFrame()
# Merge the data frames
full_data = pd.merge(df, census, on='constituency')
full_data = pd.merge(full_data, subset_election_res, on='constituency')


# Check the merged data frame
print(full_data.head())


full_data.to_csv('fulldf.csv', index=False)



