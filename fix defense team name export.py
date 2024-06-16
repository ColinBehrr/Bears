#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 18:41:20 2024

@author: colinbehr
"""

import pandas as pd
import os
os.chdir('/Users/colinbehr/Downloads') #change wd to downloads

# Load the Excel file
df = pd.read_excel('nfl_rushing_stats.xlsx')


# Remove the second name in each cell under 'Team'
df['Team'] = df['Team'].str.split().apply(lambda x: x[0])

# Save the modified DataFrame to a new Excel file
df.to_excel('rushmodified_.xlsx', index=False)
