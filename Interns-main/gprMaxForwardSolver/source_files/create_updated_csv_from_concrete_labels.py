# -*- coding: utf-8 -*-
"""

This code creates an updated csv file for concrete_labels by removing the labels 
of missing files in the output_Ascans folder.
Output file: updated_concrete_labels.csv
"""

import pandas as pd
import os

file_path = "C:\Work\gprMaxPythonScripts\gpr_in_files\Concrete_labels.txt"

# Load the data into a pandas DataFrame
df = pd.read_csv(file_path, sep=" ", header=None, names=["filename", "radius", "depth","mv"])

print(df.head())

# Strip any leading/trailing '/' nad ':'' from the 'filename' column
df['filename'] = df['filename'].str.strip('\\').str.rstrip('.in:')


# Display the DataFrame
print(df.head())

# Get the list of files in the folder
folder_path = "C:\Work\gprMaxPythonScripts\output_Ascans" 

files_in_folder = (os.listdir(folder_path))
print(len(files_in_folder))


# Strip '.out' from filenames
files_in_folder = {file.rstrip('.out') for file in files_in_folder}
# Print first 5 files in the folder (or fewer if there are less than 5)
print("First 5 files in the folder (or fewer if there are less than 5):")
for file in list(files_in_folder)[:5]:
    print(file)

# Filter the DataFrame to keep only rows where the filename exists in the folder
df_updated = df[df['filename'].isin(files_in_folder)]

# Save the updated DataFrame to a new CSV file
df_updated.to_csv('updated_concrete_labels.csv', index=False)

print(f"Updated DataFrame saved to 'updated_concrete_labels.csv'")
print(f"Removed {len(df) - len(df_updated)} entries for missing files.")