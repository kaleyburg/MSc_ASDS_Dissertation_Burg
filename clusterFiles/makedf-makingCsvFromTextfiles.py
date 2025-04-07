# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 17:38:28 2024

@author: kburg
"""

import os
import pandas as pd
import re
# Directory path
#directory = r"C:\Users\kburg\OneDrive\Documents\Trinity\diss_all_other\cluster\output\output"
directory = "/home/users/burgk/output"



# List to hold file names and their contents
file_data = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Check if it's a file (not a directory)
    if os.path.isfile(file_path):
        # Open the file and read its content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Append the file name and content to the list
            file_data.append((filename, content))

# Create a DataFrame
df = pd.DataFrame(file_data, columns=['FileName', 'Content'])

# Display the DataFrame
#print(df)


# Save DataFrame to a CSV file in the specified directory
output_path = "/home/users/burgk/output.csv"
df.to_csv(output_path, index=False)

print(f"DataFrame saved to {output_path}")


import pandas as pd


csv_file_path = r"C:\Users\kburg\OneDrive\Documents\Trinity\diss_all_other\cluster\output_july3.csv"
df = pd.read_csv(csv_file_path)
print(df)

df.columns


df['Content']
# Extract the numeric part of each file name
df['Number'] = df['FileName'].apply(lambda x: int(re.search(r'output_(\d+)', x).group(1)))

# Determine the range of these numbers
min_num = df['Number'].min()
max_num = df['Number'].max()

# Generate the complete range of numbers
complete_range = set(range(min_num, max_num + 1))

# Determine the existing numbers
existing_numbers = set(df['Number'])

# Identify the missing numbers
missing_numbers = sorted(complete_range - existing_numbers)

# Display results
print(f"Range of output numbers: {min_num} to {max_num}")
print(f"Missing numbers: {missing_numbers}")


# Function to extract Leaflet Number, Image, and Folder from Content
def extract_info(content):
    # Extract Leaflet Number
    leaflet_number = re.search(r'Leaflet Number: (\d+)', content).group(1)
    
    # Extract Image
    image = re.search(r'Image: ([\w.-]+)', content).group(1)
    
    # Extract Folder Name
    folder_match = re.search(r'Folder Name: ([\w.-]+)$', content)
    folder = folder_match.group(1) if folder_match else ''
    
    # Remove extracted info from content
    content = re.sub(r'Leaflet Number: \d+, Image: [\w.-]+, Text:', '', content)
    content = re.sub(r'Folder Name: [\w.-]+$', '', content).strip()
    
    return leaflet_number, image, folder, content

# Apply the function to create new columns and update Content
df['Leaflet_Number'], df['Image'], df['Folder'], df['Content'] = zip(*df['Content'].apply(extract_info))

# Display the updated DataFrame
print(df)

# Specify the directory path
directory = r'C:\Users\kburg\OneDrive\Documents\Trinity\diss_all_other'

# Save DataFrame to CSV
df.to_csv(f'{directory}\\data_0307.csv', index=False)

print(f"DataFrame saved as 'data_0307.csv' in '{directory}'")

