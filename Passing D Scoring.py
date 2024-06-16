#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:53:45 2024

@author: colinbehr
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

#wd
os.chdir('/Users/colinbehr/Downloads')

#data
df = pd.read_excel('bears_defense_passing.xlsx')  

#get rid of "touchdown" in Lng cells
df['Lng'] = df['Lng'].str.extract('(\d+)').astype(float)

#all columns
columns_to_standardize = [ "Att", "Cmp", "Cmp%", "Yds/Att", "Yds", "TD", "INT", "Rate", "1st", "1st%", "20+", "40+", "Lng", "Sck"]

scaler = StandardScaler()
df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

# weighting
weights = {
    'Yds/Att': -0.25,  #lot of yards per pass is bad
    'TD': -0.3,        #lot of TDs bad
    'INT': 0.25,       #ints good
    'Rate': -0.2,      #large QBR is bad
    'Sck': 0.2,        #sacks is good
    '1st%': -0.15,     #a lot of first downs bad
    '20+': -0.1        #a lot of big plays bad
}

#overall score
df['Defense Passing Score'] = (
    (df['Yds/Att'] * weights['Yds/Att']) +
    (df['TD'] * weights['TD']) +
    (df['INT'] * weights['INT']) +  # Positive for defense
    (df['Rate'] * weights['Rate']) +
    (df['Sck'] * weights['Sck']) +  # Positive for defense
    (df['1st%'] * weights['1st%']) +
    (df['20+'] * weights['20+'])
)


from sklearn.preprocessing import MinMaxScaler

#standardize score 1-10 
scaler = MinMaxScaler(feature_range=(1, 10))

#function to scale
def scale_rushing_score(group):
    group['Defense Passing Score Scaled'] = scaler.fit_transform(group[['Defense Passing Score']])
    return group

#group by season
df = df.groupby('Year', group_keys=True).apply(scale_rushing_score)  # Assigning back to df


print(df[['Year', 'Team', 'Defense Passing Score', 'Defense Passing Score Scaled']])

#save
output_file_name = 'nfl_Dpassing_sscores.xlsx'
df.to_excel(output_file_name, index=False)