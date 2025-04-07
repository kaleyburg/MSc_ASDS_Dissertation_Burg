# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 16:00:09 2024

@author: kburg
"""

import pandas as pd

def convert_paths(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file, engine='openpyxl')

    # Define the path parts to replace
    old_base_path = r"C:/Users/kburg/OneDrive/Documents/Trinity/Dissertation"
    new_base_path = "/home/users/burgk/leaflets"

    # Function to convert paths
    def convert_path(old_path):
        # Replace the base path
        if old_path.startswith(old_base_path):
            new_path = old_path.replace(old_base_path, new_base_path)
            # Replace backslashes with forward slashes
            new_path = new_path.replace('\\', '/')
            return new_path
        return old_path

    # Apply the function to the 'leaflet_path' column
    df['leaflet_path'] = df['leaflet_path'].apply(convert_path)

    # Save the modified DataFrame back to an Excel file
    df.to_excel(output_file, index=False, engine='openpyxl')

# Example usage
input_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel.xlsx'
output_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel2.xlsx'

convert_paths(input_file, output_file)





import pandas as pd

# Replace 'input_file.xlsx' with your actual Excel file path
input_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel2.xlsx'

# Read Excel file
df = pd.read_excel(input_file)

# Replace 'scripts' with 'leaflets' in specific columns (adjust column names as needed)
columns_to_replace = ['leaflet_path', 'folder_name']  # Adjust based on your actual column names
for column in columns_to_replace:
    df[column] = df[column].str.replace('scripts', 'leaflets')

# Write modified DataFrame back to Excel
output_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel2.xlsx'
df.to_excel(output_file, index=False)

print(f'Updated Excel file saved to {output_file}')

# Replace 'input_file.xlsx' with your actual Excel file path
input_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel2.xlsx'

# Read Excel file
df = pd.read_excel(input_file)

# Replace 'scripts' with 'leaflets' in specific columns (adjust column names as needed)
columns_to_replace = ['leaflet_path', 'folder_name']  # Adjust based on your actual column names
for column in columns_to_replace:
    df[column] = df[column].str.replace('scripts', 'leaflets')

# Write modified DataFrame back to Excel
output_file = 'C:/Users/kburg/OneDrive/Documents/Trinity/diss_all_other/xcel2.xlsx'
df.to_excel(output_file, index=False)

print(f'Updated Excel file saved to {output_file}')

