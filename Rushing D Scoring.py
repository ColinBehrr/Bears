#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:16:38 2024

@author: colinbehr
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

#wd
os.chdir('/Users/colinbehr/Downloads')

#data
df = pd.read_excel('defense_rushing1.xlsx')  

#get rid of "touchdown" in Lng cells
df['Lng'] = df['Lng'].str.extract('(\d+)').astype(float)

#all columns
columns_to_standardize = [ "Att", "Rush Yds", "YPC", "TD", "20+", "40+", "Lng", "Rush 1st", "Rush 1st%", "Rush FUM"]

scaler = StandardScaler()
df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

weights = {
    'YPC': -0.4,       # Lower YPC is better, highly indicative of rushing defense effectiveness.
    'TD': -0.3,        # Fewer rushing TDs is better, critical for scoring defense.
    'Rush 1st%': -0.25, # Lower first down percentage is better, shows efficiency in stopping runs on crucial downs.
    '20+': -0.15,      # Fewer 20+ yard runs is better, shows control over limiting big plays.
    'Rush FUM': 0.2    # More fumbles recovered is good, reflects positive defensive plays.
}

# Overall Rushing Defense Score
df['Defense Rushing Score'] = (
    (df['YPC'] * weights['YPC']) +
    (df['TD'] * weights['TD']) +
    (df['Rush 1st%'] * weights['Rush 1st%']) +
    (df['20+'] * weights['20+']) +
    (df['Rush FUM'] * weights['Rush FUM'])
)


from sklearn.preprocessing import MinMaxScaler

#standardize score 1-10 
scaler = MinMaxScaler(feature_range=(1, 10))

#function to scale
def scale_rushing_score(group):
    group['Defense Rushing Score Scaled'] = scaler.fit_transform(group[['Defense Rushing Score']])
    return group

#group by season
df = df.groupby('Year', group_keys=True).apply(scale_rushing_score)  # Assigning back to df


print(df[['Year', 'Team', 'Defense Rushing Score', 'Defense Rushing Score Scaled']])

#save
output_file_name = 'nfl_Rpassing_scores.xlsx'
df.to_excel(output_file_name, index=False)