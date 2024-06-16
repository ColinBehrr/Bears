#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 22:05:38 2024

@author: colinbehr
"""

import pandas as pd
import os
os.chdir('/Users/colinbehr/Downloads')
df = pd.read_csv('ALL.csv')

#yard line coverter
def convert_location(location):
    loc = str(location)
    parts = loc.split()
    #if not CHI then 100 -
    if len(parts) == 2 and parts[1].isdigit():
        yard = int(parts[1])
        return 100 - yard if parts[0] != 'CHI' else yard

#lead -- DONT USE
def map_lead(lead):
    mapping = {'Leading': 1, 'Behind': -1, 'Tied': 0}
    return mapping.get(lead, 0)  # Default to 0 if unknown

#icon -- DONT USE 
def map_hourly_icon(icon):
    mapping = {'clear-day': 1, 'clear-night': 2, 'rain': 3, 'snow': 4, 'cloudy': 5, 'partially-cloudy-day': 6, 'partially-cloudy-night': 7}
    return mapping.get(icon, 0)  # Default to 0 if unknown

#time
def convert_time_to_minutes(time_str):
    time_str = str(time_str)
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes + seconds / 60.0
    return 0

#time
def calculate_total_time(quarter, time_str):
    if str(quarter) == 'OT':
        # Assuming 10 minutes for overtime; adjust if your game rules are different
        return convert_time_to_minutes(time_str)
    else:
        quarter = int(quarter)  # Convert quarter to integer if not 'OT'
        time_left_in_quarter = convert_time_to_minutes(time_str)
        return (4 - quarter) * 15 + time_left_in_quarter

#convert surface type
def convert_surface(surface_str):
    surface_str = str(surface_str).lower()  # Ensure string format and lower case for comparison
    return 0 if 'turf' in surface_str else 1  # 0 for turf, 1 for grass

#roof -- DONT USE
def convert_roof_type(roof_str):
    # Map roof types to numerical codes
    roof_mapping = {'N': 0, 'D': 1, 'R': 2}  # N for open, D for dome, R for retractable
    return roof_mapping.get(str(roof_str)) 

#df
df = pd.read_excel('ALL.xlsx', engine='openpyxl')  # Make sure 'ALL.xlsx' is in your current directory or provide the full path

# Apply conversions
df['Location'] = df['Location'].apply(convert_location)
df['Lead'] = df['Lead'].apply(map_lead)
df['Hourly Icon'] = df['Hourly Icon'].apply(map_hourly_icon)
df['TotalTime'] = df.apply(lambda row: calculate_total_time(row['Quarter'], row['Time']), axis=1)
df['Surface'] = df['Surface'].apply(convert_surface)
df['RoofType'] = df['RoofType'].apply(convert_roof_type)

#Save the processed DataFrame to a new CSV file
df.to_csv('processed_ALL1.csv', index=False)
