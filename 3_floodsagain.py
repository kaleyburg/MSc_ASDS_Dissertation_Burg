# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:08:45 2024

@author: kburg
"""

import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from geopandas.tools import sjoin

# Set the working directory
working_directory = "C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other"
os.chdir(working_directory)

# Load the shapefiles and the Excel workbook
admin_boundaries_fp = "C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/Administrative_Areas___Environment_Agency_and_Natural_England.shp"
constituencies_fp = "C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/map2/westminster-parliamentary-constituencies.shp"
excel_fp = "C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/202404 Historic Flood Warnings - EA.xlsx"

admin_boundaries_gdf = gpd.read_file(admin_boundaries_fp)
constituencies_gdf = gpd.read_file(constituencies_fp)
flood_warnings_df = pd.read_excel(excel_fp)

# Inspecting data
print(admin_boundaries_gdf.head())
admin_boundaries_gdf.columns
print(constituencies_gdf.head())
constituencies_gdf.columns

print(flood_warnings_df.head())
flood_warnings_df.columns


#function to check if any part of the SHORT_NAME exists in the AREA column
def match_area(area, short_names):
    for short_name in short_names:
        if short_name in area:
            return short_name
    return None

#apply function to create a new column in the Excel dataframe
admin_short_names = admin_boundaries_gdf['SHORT_NAME'].tolist()
flood_warnings_df['SHORT_NAME'] = flood_warnings_df['AREA'].apply(lambda x: match_area(x, admin_short_names))

#merge GeoDataFrame with the DataFrame on the SHORT_NAME
merged_gdf = flood_warnings_df.merge(admin_boundaries_gdf, on='SHORT_NAME')


constituencies_gdf = constituencies_gdf.to_crs(admin_boundaries_gdf.crs)

#plotting data to visualize overlays
#shown different ways for best visibility
# Plotting the data to visualize the overlays
fig, ax = plt.subplots(figsize=(15, 10))

# Plot constituency boundaries
constituencies_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=0.8, label='Constituencies')

# Plot administrative boundaries
admin_boundaries_gdf.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=0.8, linestyle='--', label='Administrative Areas')

# Add legend and title
plt.legend(loc='upper right')
plt.title("Overlay of Constituency Boundaries with Administrative Boundaries")
plt.show()


# Plotting the constituency boundaries
fig, ax = plt.subplots(figsize=(15, 10))

constituencies_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=0.5)

plt.title("Constituency Boundaries")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()


# Plotting administrative boundaries
fig, ax = plt.subplots(figsize=(10, 10))
admin_boundaries_gdf.plot(ax=ax, edgecolor='black', facecolor='none')

# Plotting constituency boundaries with transparency
constituencies_gdf.plot(ax=ax, edgecolor='red', facecolor='none', alpha=0.5)

# Customize the plot
ax.set_title('Administrative and Constituency Boundaries')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.show()

##


# Create subplots
fig, ax = plt.subplots(1, 1, figsize = (10, 10))

# Plot data
constituencies_gdf.plot(ax = ax, color = 'bisque', edgecolor = 'dimgray', alpha = 0.75)
admin_boundaries_gdf.plot(ax = ax, color = 'lightskyblue', edgecolor = 'dodgerblue', alpha = 0.55)

# Stylize plots
plt.style.use('bmh')

# Set title
ax.set_title('Constituency and Admin Areas', fontdict = {'fontsize': '15', 'fontweight' : '3'})

plt.show()





#Spatial overlay for dataset
merged_with_admin_boundaries = gpd.overlay(constituencies_gdf, admin_boundaries_gdf, how='intersection')
merged_with_admin_boundaries.columns


print(merged_with_admin_boundaries.head())
merged_with_admin_boundaries['pcon22nm']

flood_warnings_df.columns
flood_warnings_df.head
flood_warnings_df['TYPE']
merged_with_admin_boundaries.columns

#flood warnings data for years 2009 to 2020
flood_warnings_subset = flood_warnings_df[(flood_warnings_df['DATE'].dt.year >= 2009) & (flood_warnings_df['DATE'].dt.year <= 2020)].copy()


#merge based on 'SHORT_NAME' column
merged_data = merged_with_admin_boundaries.merge(flood_warnings_df, on='SHORT_NAME', how='inner')

#flood warnings data for years 2009 to 2020
flood_warnings_subset = flood_warnings_df[(flood_warnings_df['DATE'].dt.year >= 2009) & (flood_warnings_df['DATE'].dt.year <= 2020)].copy()

#merge spatially joined GeoDataFrame with flood warnings data
merged_data = merged_with_admin_boundaries.merge(flood_warnings_subset, on='SHORT_NAME', how='inner')

#group by year, admin_boundary_name, constituency (SHORT_NAME), and flood alert type (TYPE), and count occurrences
counts_by_type = merged_data.groupby([merged_data['DATE'].dt.year, 'SHORT_NAME', 'TYPE']).size().reset_index(name='count')

print(counts_by_type.head())
counts_by_type.columns


#counts_by_type with merged_with_admin_boundaries to include constituency names (pcon22nm)
merged_data_full = counts_by_type.merge(merged_with_admin_boundaries[['pcon22nm', 'SHORT_NAME']], on='SHORT_NAME', how='left')

#group by DATE, pcon22nm (constituency name), SHORT_NAME (admin area name), TYPE, and sum counts
aggregated_data = merged_data_full.groupby(['DATE', 'pcon22nm', 'SHORT_NAME', 'TYPE']).agg({'count': 'sum'}).reset_index()


aggregated_data = aggregated_data.drop_duplicates()

#select only the relevant columns for the final dataset
final_dataset = aggregated_data[['DATE', 'pcon22nm', 'SHORT_NAME', 'TYPE', 'count']]

print(final_dataset.head())


output_csv_path = 'final_floods.csv'


final_dataset.to_csv(output_csv_path, index=False)

print(f"CSV file saved successfully at: {output_csv_path}")


floods = pd.read_csv('final_floods.csv')

floods.columns
