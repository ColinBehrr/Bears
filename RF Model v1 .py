#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 20:24:48 2024

@author: colinbehr
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

import os
os.chdir('/Users/colinbehr/Desktop/RESEARCH')

file_path = 'ALL Bears Data.xlsx'
play_by_play_data = pd.read_excel(file_path, sheet_name='Play-By-Play')

#filter for only Bears' offense
bears_plays = play_by_play_data[(play_by_play_data['Team'] == 'Bears') & play_by_play_data['Play Type'].isin(['Pass', 'Run'])]

#drop rows that don't show important play prediction info
bears_plays = bears_plays.dropna(subset=['Down', 'ToGo', 'Location', 'Play Type'])

#encode all categoricals
le = LabelEncoder()
bears_plays['Location'] = le.fit_transform(bears_plays['Location'])
bears_plays['Play Type'] = le.fit_transform(bears_plays['Play Type'])  #0 for Pass 1 for Run, etc. 

#define features & target
X = bears_plays[['Down', 'ToGo', 'Location', 'Away Score', 'Home Score']]  # Features
y = bears_plays['Play Type']  # Target

#splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#train RF Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

#make predictions
y_pred = rf_model.predict(X_test)
evaluation = classification_report(y_test, y_pred, target_names=le.classes_)

print(evaluation)
