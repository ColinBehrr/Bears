#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:22:28 2024

@author: colinbehr
"""

import pandas as pd

# Load data, setting low_memory to False to handle mixed types
data = pd.read_csv("/Users/colinbehr/Desktop/RESEARCH/ALL.csv", low_memory=False)

# Convert fields to numeric, assuming they should be numeric.
# Adjust 'coerce' based on how you want to handle invalid parsing - 'coerce' will set invalid parsing to NaN
columns_to_convert = ['Location Actual', 'ToGo', 'Down', 'Lead Num', 'TotalTime', 'Pass D', 'Rush D', 'RoofType Num', 'Surface Num']
for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Fill NaNs (resulting from conversion or existing) with 0 or appropriate value
data.fillna(0, inplace=True)

# Now, construct 'SituationID' and 'WeatherID' safely
data['TotalTimeSeconds'] = data['TotalTime'] * 60  # Assuming TotalTime is in minutes
data['SituationID'] = (data['Location Actual'] +
                       data['ToGo'] * 10 +
                       data['Down'] * 100 +
                       data['Lead'] * 1000 +
                       data['TotalTime'] * 1000 +
                       data['Pass D'] * 100 +
                       data['Rush D'] * 1000 +
                       data['RoofType'] * 10000 +
                       data['Surface'] * 100000)

data['WeatherID'] = (data['Hourly Feels Like'].astype(int) * 10000 +
                     data['Hourly Wind Gust'].astype(int) * 1000 +
                     data['Hourly Wind Speed'].astype(int) * 100 +
                     data['Hourly Icon Num'].astype(int) * 10 +
                     data['Dark'].astype(int))


# Preprocess 'Play Type' to be consistent with your Spark code conversion
data['Play Type'] = data['Play Type'].apply(lambda x: 1 if x == 'Pass' else 2)

# Select relevant features for LightFM (we assume 'PlayID' is a unique identifier for plays)
feature_cols = ['SituationID', 'PlayID', 'Yards Gained', 'Play Type']


def split_train_test_pandas(df):
    train_frames = []  # Empty lists for train and test DataFrames
    test_frames = []
    
    for season in range(2013, 2023):  # Iterate through each season
        season_data = df[df['SeasonID'] == season]  # Filter by season
        next_season_data = df[df['SeasonID'] == season + 1]  # Data for the next season
        
        first_game_id = season_data['GameID'].min()  # Get the first GameID of the current season
        first_game_data = season_data[season_data['GameID'] == first_game_id]  # First game data
        test_frames.append(first_game_data)
        
        # Initialize last_game_id for safety
        last_game_id = season_data['GameID'].max()  # Default to last game if next season's first game isn't found
        
        # Get the last game of the season by finding the first game of the next season and subtracting one
        if not next_season_data.empty:  # If not the last season available
            next_first_game_id = next_season_data['GameID'].min()
            last_game_data = season_data[season_data['GameID'] == next_first_game_id - 1]
        else:  # If it is the last season, just take the last game directly
            last_game_data = season_data[season_data['GameID'] == last_game_id]
        
        # Add the last game data to the test frames
        test_frames.append(last_game_data)
        
        # All other games go into the training set
        remaining_season_data = season_data[(season_data['GameID'] != first_game_id) & (season_data['GameID'] != last_game_id)]
        train_frames.append(remaining_season_data)
    
    # Combine all the frames for training and testing
    train_df = pd.concat(train_frames, ignore_index=True)
    test_df = pd.concat(test_frames, ignore_index=True)
    
    return train_df, test_df

# Create train and test datasets
train_df, test_df = split_train_test_pandas(data)
print(len(train_df), len(test_df))
# Get the set of SituationIDs that were present during training
seen_situation_ids = set(train_df['SituationID'].unique())

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Assuming 'data' is your DataFrame loaded with correct splits and 'SituationID'

# Preparing data: Separate features and targets for Rush and Pass
X_rush = train_df[train_df['Play Type'] == 2][['SituationID', 'PlayID']]  # Add more features as needed
y_rush = train_df[train_df['Play Type'] == 2]['Yards Gained']
X_pass = train_df[train_df['Play Type'] == 1][['SituationID', 'PlayID']]  # Add more features as needed
y_pass = train_df[train_df['Play Type'] == 1]['Yards Gained']

# Preparing the test sets
X_test_rush = test_df[test_df['Play Type'] == 2][['SituationID', 'PlayID']]  # Ensure same features as training
y_test_rush = test_df[test_df['Play Type'] == 2]['Yards Gained']
X_test_pass = test_df[test_df['Play Type'] == 1][['SituationID', 'PlayID']]
y_test_pass = test_df[test_df['Play Type'] == 1]['Yards Gained']

# Initialize and train models
model_rush = LinearRegression()
model_rush.fit(X_rush, y_rush)
model_pass = LinearRegression()
model_pass.fit(X_pass, y_pass)

# Predict and calculate RMSE
predictions_rush = model_rush.predict(X_test_rush)
rmse_rush = np.sqrt(mean_squared_error(y_test_rush, predictions_rush))
predictions_pass = model_pass.predict(X_test_pass)
rmse_pass = np.sqrt(mean_squared_error(y_test_pass, predictions_pass))

print(f'RMSE for Rush plays: {rmse_rush}')
print(f'RMSE for Pass plays: {rmse_pass}')



#

# Prepare the dataset
#dataset = Dataset()
#dataset.fit(
#    (x for x in pd.concat([train_df['SituationID'], test_df['SituationID']])),  # All unique situations from both sets
#    (x for x in pd.concat([train_df['PlayID'], test_df['PlayID']]))  # All unique plays from both sets
#)

# Build interactions for train and test
#(interactions_train, weights_train) = dataset.build_interactions(
#   ((row['SituationID'], row['PlayID'], row['Yards Gained']) for idx, row in train_df.iterrows())
#)
#(interactions_test, weights_test) = dataset.build_interactions(
#    ((row['SituationID'], row['PlayID'], row['Yards Gained']) for idx, row in test_df.iterrows())
#)#

#from lightfm import LightFM
#from lightfm.evaluation import auc_score

# Initialize and train the model
#model = LightFM(loss='warp')
#model.fit(interactions_train, epochs=10, num_threads=2)

# Evaluate the model
#from lightfm.evaluation import precision_at_k, recall_at_k

# Compute and print the AUC score for the test set
#auc = auc_score(model, interactions_test).mean()
#print(f'Test AUC: {auc}')

# Compute and print Precision at k for the test set (e.g., k=5)
#precision = precision_at_k(model, interactions_test, k=5).mean()
#print(f'Test Precision at 5: {precision}')


