#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 00:31:42 2024

@author: colinbehr
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Set the working directory
import os
os.chdir('/Users/colinbehr/Desktop/RESEARCH')

# Load the data
df = pd.read_excel('ALL Bears Data.xlsx', sheet_name='ALL')

# Define success based on 'ToGo'
df['Successful Play'] = df['Yards Gained'] >= (df['ToGo'] / 2)

# Simplify 'Surface' into 'Turf' and 'Grass'
df['Surface'] = df['Surface'].apply(lambda x: 'Turf' if 'turf' in x.lower() else 'Grass')

# Categorize 'Hourly Temp' into 10-degree ranges
temp_bins = range(int(df['Hourly Temp'].min()), int(df['Hourly Temp'].max()) + 10, 10)
temp_labels = [f"{i} - {i + 9}" for i in temp_bins[:-1]]
df['Temp Range'] = pd.cut(df['Hourly Temp'], bins=temp_bins, labels=temp_labels, right=False)

# Convert 'Dark' to numeric if it's not already
# df['Dark Numeric'] = df['Dark'].astype(int)

# Preprocess and prepare the dataset (encode categorical variables, etc.)
categorical_features = ['Hourly Conditions', 'Surface', 'Dark'] # Add all categorical features
numeric_features = ['Hourly Temp', 'Hourly Precip', 'Hourly Wind Speed'] # Add all numeric features

# Extract the full list of categories in 'Hourly Conditions' from the entire dataset
full_condition_categories = df['Hourly Conditions'].unique()

# Initialize the OneHotEncoder with all possible categories
categorical_transformer = OneHotEncoder(categories=[full_condition_categories], drop='first')
numeric_transformer = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Identify unique seasons and sort the games within each season for training data selection
seasons = df['SeasonID'].unique()
training_games_ids = []

for season in seasons:
    season_games = df[df['SeasonID'] == season].sort_values(by='GameID')
    first_game = season_games['GameID'].iloc[0]
    middle_game = season_games['GameID'].iloc[len(season_games) // 2]
    last_game = season_games['GameID'].iloc[-1]
    training_games_ids.extend([first_game, middle_game, last_game])

# Create training and testing datasets
training_data = df[df['GameID'].isin(training_games_ids)]
testing_data = df[~df['GameID'].isin(training_games_ids)]

X_train = training_data[numeric_features + categorical_features]
y_train = training_data['Play Type'] # This is the target variable
X_test = testing_data[numeric_features + categorical_features]
y_test = testing_data['Play Type']

# Create the model pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', RandomForestClassifier())])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Now, you can use `pipeline.predict()` to make new predictions and recommendations.
