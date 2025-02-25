#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:47:48 2023

@author: colinbehr
"""

import pandas as pd
import re
import os
os.chdir('/Users/colinbehr/Desktop/RESEARCH') #change wd to downloads

file = 'ALL Bears Data.xlsx'

df = pd.read_excel(file, sheet_name='Play-By-Play Data')

def determine_play_type(detail):
    if pd.isna(detail):
        return None
    elif re.search(r"left tackle|left end|right tackle|right end|up the middle|left guard|right guard", detail, re.IGNORECASE):
        return "Run"
    elif re.search(r"pass complete|pass incomplete", detail, re.IGNORECASE):
        return "Pass"
    else:
        return "Not a Play"

#function ignored certain pass/run plays 
#def is_valid_play(row):
#    required_columns = ['Quarter', 'Time', 'Down', 'ToGo', 'Location', 'Away Score', 'Home Score', 'Detail']
#    return all(pd.notna(row[col]) for col in required_columns)

#valid play type ignored touchdown plays
#df['Play Type'] = df.apply(lambda row: "Not a Play" if not is_valid_play(row) else determine_play_type(row['Detail']), axis=1)

df['Play Type'] = df['Detail'].apply(determine_play_type)


with pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='Play-By-Play Data', index=False)