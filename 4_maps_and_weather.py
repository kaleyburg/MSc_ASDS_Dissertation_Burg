# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 16:43:01 2024

@author: kburg
"""



#this code file fixes the weather issues before
#output of this file is data_withweather.csv
#this is the file that will be used for the maps and the analysis   

# note - this file has been edited to fix the outcome variable
#was getting no variation across year and constituency because the mean was being calculated across all years and constituencies

#fixed this file again on July 6, 2024 to add a percentage of environment words out of total length of combined text

#%% imports and setup
#conda install ipykernel  
#do this for every env to be able to run in interactive cell
#%%setup

#conda install -c conda-forge matplotlib pandas geopandas shapely numpy statsmodels geocoder openpyxl
#pip install meteostat

import os 
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import numpy as np
from datetime import datetime, timedelta
from datetime import datetime
from meteostat import Monthly, Hourly, Daily
from shapely.geometry import Point
from meteostat import Point
from meteostat import Stations

import geocoder
import winsound



print(os.getcwd())
new_directory = 'C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg/CSVandSHPfiles'
os.chdir(new_directory)

print("Current working directory:", os.getcwd())


#%%load data and check accuracy
#not creating maps yet but creating tables regarding accuracy
# Load CSV data
csv_file = "sorted_full_df_july4_5.csv"
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


#just to identify which ones are wrong so that you can check manually
# Identify rows where 'Environment' is mentioned but 'environment' is not 1 or greater
incorrect_mentions_env_in_issues = df[environment_mentioned & ~environment_condition]
print("\nLeaflets where 'Environment' is mentioned but 'environment' is not 1 or greater:")
print(incorrect_mentions_env_in_issues[['Leaflet.Number', 'Election', 'Issues.Covered', 'environment']])

# Identify rows where 'environment' is 1 or greater but 'Environment' is not mentioned
incorrect_mentions_env_high = df[environment_condition & ~environment_mentioned]
print("\nLeaflets where 'environment' is 1 or greater but 'Environment' is not mentioned:")
print(incorrect_mentions_env_high[['Leaflet.Number', 'Election', 'Issues.Covered', 'environment']])

#running the same code but for economy condition

# Condition for 'economy' column being 1 or greater
economy_condition = df['economy'] >= 1
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

#same thing - figure out which ones are off
# Identify rows where 'Economy' is mentioned but 'economy' is not 1 or greater
incorrect_mentions_economy_in_issues = df[economy_mentioned & ~economy_condition]
print("\nLeaflets where 'Economy' is mentioned but 'economy' is not 1 or greater:")
print(incorrect_mentions_economy_in_issues[['Leaflet.Number', 'Election', 'Issues.Covered', 'economy']])

# Identify rows where 'economy' is 1 or greater but 'Economy' is not mentioned
incorrect_mentions_economy_high = df[economy_condition & ~economy_mentioned]
print("\nLeaflets where 'economy' is 1 or greater but 'Economy' is not mentioned:")
print(incorrect_mentions_economy_high[['Leaflet.Number', 'Election', 'Issues.Covered', 'economy']])


#%% merging datasets
shapefile = "westminster-parliamentary-constituencies.shp"
gdf = gpd.read_file(shapefile)
gdf.columns

# Ensure the constituency names match the ones in the shapefile
#converting to lower case or stripping whitespace
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
#june 2 - got rid of mean_env_mentions bc we want variance across constituencies

import pandas as pd

grouping_keys = ['constituency', 'Election', 'Party']

# Step 1: Calculate mean by grouping
mean_env = merged_gdf.groupby(grouping_keys)['environment'].transform('mean')

# Step 2: Add as a new column (no merge needed!)
merged_gdf['mean_environmental_mentions'] = mean_env



merged_gdf.columns
# Calculate percentage of environment words out of total word count
# Assumes columns: 'environment' (count of env words), 'Word.Count' (total words)
# Calculate percentage of environment words out of total length of combined text
# Assumes columns: 'environment' (count of env words), 'Combined.Text' (full text)
merged_gdf['environment_word_pct'] = merged_gdf['environment'] / merged_gdf['CombinedText'].str.len()

# Step 3: If you want a separate variable
new_df = merged_gdf.copy()

new_df.columns
new_df

#%% plots for report --important part


#  %% plots for report --important part


output_folder = 'C:/Users/kburg/OneDrive/Documents/GitHub/MSc_ASDS_Dissertation_Burg/tex_files_withallimagesandbib/plots'
# Ensure your output folder exists
os.makedirs(output_folder, exist_ok=True)

#create unique
unique_parties = new_df['Party'].unique()       
unique_elections = new_df['Election'].unique()


# Loop through each combination of Party and Election
for party in unique_parties:
    for election in unique_elections:
        # Filter the data
        subset_df = new_df[(new_df['Party'] == party) & (new_df['Election'] == election)]

        if subset_df.empty:
            print(f"Skipping empty subset for {party} - {election}")
            continue

        # Remove spaces for filenames
        party_no_spaces = party.replace(' ', '')
        election_no_spaces = election.replace(' ', '')

        # Set vmin/vmax based on subset if desired
        vmin = 0
        vmax = subset_df['mean_environmental_mentions'].quantile(0.90)

        # Create plot
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))
        subset_df.plot(
            column='mean_environmental_mentions',
            cmap='Greys',
            linewidth=0.8,
            edgecolor='0.8',
            ax=ax,
            legend=True,
            vmin=vmin,
            vmax=vmax,
            missing_kwds={'color': 'lightgrey', 'label': 'No Data', 'edgecolor': 'black'}
        )

        ax.set_title(f"{party} - {election}", fontsize=16)
        ax.set_axis_off()

        # Save the plot
        output_file = os.path.join(output_folder, f"{party_no_spaces}_{election_no_spaces}_Environmental_Mentions.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        print(f"Saved plot: {output_file}")

#%% working with meteostat 

new_df.columns
# Strip whitespace
new_df['Election'] = new_df['Election'].str.strip()

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
election_df = pd.DataFrame({
    'Election Date': election_dates,
    'Year Before Election': year_before_election,
    'Election': election_labels
})

# election_df with new_df based on 'Election' column
new_df = new_df.merge(election_df[['Election', 'Election Date', 'Year Before Election']], on='Election', how='left')

# Convert 'Year Before Election' and 'Election Date' to datetime objects
new_df['Year Before Election'] = pd.to_datetime(new_df['Year Before Election'])
new_df['Election Date'] = pd.to_datetime(new_df['Election Date'])

# Concatenate 'long' and 'lat' into a new column called '2dshape'
new_df['2dshape'] = new_df.apply(lambda row: (row['lat'], row['long']), axis=1)

unique_results = new_df['2dshape'].unique()
unique_results_df = pd.DataFrame(unique_results, columns=['location'])

new_df.columns


warnings.filterwarnings("ignore")
# Initialize an empty list to store variance results
weather_stds = []

# Loop over each constituency in new_df
for unique_shape in new_df['2dshape'].unique():
    lat, lon = unique_shape
    election_date = new_df.loc[new_df['2dshape'] == unique_shape, 'Election Date'].iloc[0]
    
    # Calculate start and end date for the year before the election
    start_date = election_date - pd.DateOffset(years=1)
    end_date = election_date
    
    # Find the nearest station for the current lat, lon
    stations = Stations()
    stations = stations.nearby(lat, lon)
    stations = stations.inventory('daily', start_date)
    station = stations.fetch(1)  # Get the closest station
    if station.empty:
        print(f"No station found for ({lat}, {lon})")
        continue

    # Fetch the daily data for the closest station
    daily_data = Daily(station, start=start_date, end=end_date)
    daily_data = daily_data.normalize()
    daily_data = daily_data.interpolate()
    coverage = daily_data.coverage()
    if coverage < 1:
        print(f"Insufficient coverage for station near ({lat}, {lon})")
        winsound.Beep(1000, 300)
        continue    

    # Aggregate the data weekly
    weekly_agg_data = daily_data.aggregate('1W')
    df = weekly_agg_data.fetch()

    if df.empty:
        print(f"Empty data for station near ({lat}, {lon})")
        continue
    #elif df.isna().any().any():
       # print(f"NaN values in filtered data for station near ({lat}, {lon})")
       # continue

    # Calculate standard deviation for each weather variable
    stds = df.std()
    overall_stds = stds.mean()  # Average standard deviation across all weather variables

    # Store the results
    weather_stds.append({
        'coordinates': (lat, lon),
        'overall_stds': overall_stds,
        'stds': stds.to_dict()  # Store individual standard deviations for reference
    })

# Convert the list of standard deviations to a DataFrame
stds_df = pd.DataFrame(weather_stds)
print(stds_df.columns)

# Merge the standard deviation data back into new_df
if not stds_df.empty:
    # Ensure no missing values in coordinates or overall_stds
    stds_df = stds_df.dropna(subset=['coordinates', 'overall_stds'])
    new_df['overall_weather_std'] = new_df['2dshape'].map(
        dict(zip(stds_df['coordinates'], stds_df['overall_stds']))
    )
else:
    print("Warning: stds_df is empty. 'overall_weather_std' will not be added.")
    new_df['overall_weather_std'] = np.nan

# Print the updated DataFrame
print(new_df[['2dshape', 'overall_weather_std']])
#winsound.Beep(1000, 1000)

new_df.columns

for column in new_df.columns:
    print(new_df[column])


smalldf = new_df.drop(columns=['fid', 'pcon22cd', 'pcon22nm', 'bng_e', 'bng_n', 'globalid',
       'shape_leng', 'shape_area', 'CONSTITUENCY',
       'Constituency', 
       'Year Before Election'])

smalldf.columns
new_df['pcon22nm']
new_df['Constituency']

#%% saving csv

output_path = os.path.join(os.getcwd(), "data_withweather.csv")


smalldf.to_csv(output_path, index=False)
print(f"DataFrame saved to {output_path}")    