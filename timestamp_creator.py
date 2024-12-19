#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:13:34 2023

@author: colinbehr
"""

import pandas as pd
import os
os.chdir('/Users/colinbehr/Downloads') #change wd to downloads

# Read the Excel file
file_path = "Chicago_Bears_Boxscore_Data_20231011125115.xlsx"
df = pd.read_excel(file_path)

# Convert "Date" and "Time" columns to a single datetime column
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].str.strip(': '))

# Generate the timestamps in the required format
df['Timestamp 1'] = df['Datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')
df['Timestamp 2'] = (df['Datetime'] + pd.Timedelta(hours=1)).dt.strftime('%Y-%m-%dT%H:%M:%S')
df['Timestamp 3'] = (df['Datetime'] + pd.Timedelta(hours=2)).dt.strftime('%Y-%m-%dT%H:%M:%S')

# Drop the combined 'Datetime' column and original "Date" and "Time" columns
df = df.drop(columns=['Datetime', 'Date', 'Time'])

# Save the modified DataFrame back to Excel
output_path = "path_to_your_output_file.xlsx"
df.to_excel(output_path, index=False)

print("Data processed and saved!")
