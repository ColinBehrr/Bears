#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 23:43:45 2024

@author: colinbehr
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

#wd
os.chdir('/Users/colinbehr/Downloads')

#data
df = pd.read_excel('nfl_passing_stats.xlsx')  

#get rid of "touchdown" in Lng cells
df['Lng'] = df['Lng'].str.extract('(\d+)').astype(float)

#all columns
columns_to_standardize = [ "Att", "Cmp", "Cmp %", "Yds/Att", "Pass Yds", "TD", "INT", "Rate", "1st", "1st%", "20+", "40+", "Lng", "Sck", "SckY"]

scaler = StandardScaler()
df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

# weighting
weights = {
    'Cmp %': 0.4, #most important
    'Rate': 0.3,
    '1st%': 0.2,
    'TD': 0.15,
    '20+': 0.05,
    '40+': 0.05,
    'Lng': 0.05,
    'INT': -0.2  #bad
}

#overall score
df['Passing Score'] = (
    (df['Cmp %'] * weights['Cmp %']) +
    (df['Rate'] * weights['Rate']) +
    (df['1st%'] * weights['1st%']) +
    (df['TD'] * weights['TD']) +
    (df['20+'] * weights['20+']) +
    (df['40+'] * weights['40+']) +
    (df['Lng'] * weights['Lng']) +
    (df['INT'] * weights['INT'])
)

from sklearn.preprocessing import MinMaxScaler

#standardize score 1-10 
scaler = MinMaxScaler(feature_range=(1, 10))

#function to scale
def scale_rushing_score(group):
    group['Passing Score Scaled'] = scaler.fit_transform(group[['Passing Score']])
    return group

#group by season
df = df.groupby('Year', group_keys=True).apply(scale_rushing_score)  # Assigning back to df


print(df[['Year', 'Team', 'Passing Score', 'Passing Score Scaled']])

#save
output_file_name = 'nfl_passing_sscores.xlsx'
df.to_excel(output_file_name, index=False)