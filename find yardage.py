#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 16:47:59 2023

@author: colinbehr
"""

import pandas as pd
import re
import os

os.chdir('/Users/colinbehr/Desktop/RESEARCH')


df = pd.read_excel('ALL Bears Data.xlsx', sheet_name='ALL')


def extract_yardage(row):
    # Check if 'Detail' is a string
    if isinstance(row['Detail'], str):
        detail = row['Detail'].lower()
        if row['Play Type'] in ['Run', 'Pass']:  # offense
            # Check for incomplete pass, penalty, or no play
            if "pass incomplete" in detail or "no play" in detail:
                return 0
            else:
                # Search for yardage in the detail
                match = re.search(r'(-?\d+) yard(s)?', detail) #any digit +/- with yard(s)
                
                if match:
                    return int(match.group(1))
                else:
                    return 0  # no gain
        else:
            return "N/A"  # not an offensive play
    else:
        # If 'Detail' is not a string, return a default value
        return "N/A"

# Apply the function to the DataFrame
df['Yards Gained'] = df.apply(extract_yardage, axis=1)

#save
df.to_excel('yards.xlsx', index=False)
