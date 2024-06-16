#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 22:45:31 2024

@author: colinbehr
"""

import pandas as pd
import os
os.chdir('/Users/colinbehr/Desktop/RESEARCH')

#df
df = pd.read_excel('ALL.xlsx', engine='openpyxl')  

#separate
pass_plays = df[df['Play Type'] == 'Pass']
run_plays = df[df['Play Type'] == 'Run']

#avg
average_yards_pass = pass_plays['Yards Gained'].mean()
average_yards_run = run_plays['Yards Gained'].mean()

#print
print(f'Average Yards Gained on Pass Plays: {average_yards_pass}')
print(f'Average Yards Gained on Run Plays: {average_yards_run}')
