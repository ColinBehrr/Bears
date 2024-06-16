#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 13:21:08 2024

@author: colinbehr
"""

import pandas as pd
import os
os.chdir('/Users/colinbehr/Desktop/RESEARCH')
df = pd.read_excel('ALL Bears Data.xlsx', sheet_name = "ALL")

#create bins
df['ToGo_Category'] = pd.cut(df['ToGo'], bins=[0, 3, 6, float('inf')], labels=['Short', 'Medium', 'Long'])

#group
play_success = df.groupby(['ToGo_Category', 'Play'])['Yards Gained'].mean().reset_index()

#rank plays
play_success['Rank'] = play_success.groupby('ToGo_Category')['Yards Gained'].rank(method='max', ascending=False)

#play type
top_plays = play_success[play_success['Rank'] <= 3]  # This filters for the top 3 plays

top_short_plays = top_plays[top_plays['ToGo_Category'] == 'Short']
top_med_plays = top_plays[top_plays['ToGo_Category'] == 'Medium']
top_long_plays = top_plays[top_plays['ToGo_Category'] == 'Long']

print(top_short_plays.sort_values(by='Yards Gained', ascending=False))
print(top_med_plays.sort_values(by='Yards Gained', ascending=False))
print(top_long_plays.sort_values(by='Yards Gained', ascending=False))




