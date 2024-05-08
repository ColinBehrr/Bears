#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:25:46 2024

@author: colinbehr
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

#wd
os.chdir('/Users/colinbehr/Downloads')

#data
df = pd.read_excel('nfl_rushing_stats.xlsx')  

#get rid of "touchdown" in Lng cells
df['Lng'] = df['Lng'].str.extract('(\d+)').astype(float)

#all columns
columns_to_standardize = ['Att', 'Rush Yds', 'YPC', 'TD', '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%', 'Rush FUM']

scaler = StandardScaler()
df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

# weighting
weights = {
    'YPC': 0.3, #most important
    'TD': 0.2,
    '20+': 0.05,
    '40+': 0.05,
    'Lng': 0.05,
    'Rush 1st': 0.15,
    'Rush 1st%': 0.2,
    'Rush FUM': -0.2  #bad
}

#overall score
df['Rushing Score'] = (
    (df['YPC'] * weights['YPC']) +
    (df['TD'] * weights['TD']) +
    (df['20+'] * weights['20+']) +
    (df['40+'] * weights['40+']) +
    (df['Lng'] * weights['Lng']) +
    (df['Rush 1st'] * weights['Rush 1st']) +
    (df['Rush 1st%'] * weights['Rush 1st%']) +
    (df['Rush FUM'] * weights['Rush FUM'])
)

from sklearn.preprocessing import MinMaxScaler

#standardize score 1-10 
scaler = MinMaxScaler(feature_range=(1, 10))

#function to scale
def scale_rushing_score(group):
    group['Rushing Score Scaled'] = scaler.fit_transform(group[['Rushing Score']])
    return group

#group by season
df = df.groupby('Year', group_keys=True).apply(scale_rushing_score)  # Assigning back to df


print(df[['Year', 'Team', 'Rushing Score', 'Rushing Score Scaled']])

#save
output_file_name = 'nfl_rushing_sscores.xlsx'
df.to_excel(output_file_name, index=False)