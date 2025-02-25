#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:22:07 2023

@author: colinbehr
"""

import pandas as pd
import os

os.chdir('/Users/colinbehr/Desktop/RESEARCH')


df = pd.read_excel('ALL Bears Data.xlsx', sheet_name='Play-By-Play')


# Function to check for 'touchdown'
def check_touchdown(detail):
    if pd.isna(detail):
        return "No"  # Return "No" if detail is NaN
    return "Yes" if "touchdown" in detail.lower() else "No"

# Apply the function to create the new column
df['TD'] = df['Detail'].apply(check_touchdown)

# Save the updated DataFrame to a new Excel file
df.to_excel('td.xlsx', index=False)
