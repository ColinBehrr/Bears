#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:14:27 2024

@author: colinbehr
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import numpy as np

#df
data = pd.read_csv("/Users/colinbehr/Desktop/RESEARCH/ALL.csv")

#Preprocess data
#data['TotalTimeSeconds'] = data['TotalTime'].apply(lambda x: int(x * 60)) for ALS since no floats

data['SituationID'] = (data['Location Actual'] +
                       data['TotalTime'] +
                       data['ToGo'] * 10 +
                       data['Down'] * 100 +
                       data['Lead Num'] * 1000 +
                       data['TotalTimeSeconds'] * 10000)

#binary
data['Play Type'] = np.where(data['Play Type'] == 'Pass', 1, 0)

#use Pass / Rush respectivelly
features_pass = ['SituationID', 'Pass D']
features_rush = ['SituationID', 'Rush D']
data = data.dropna(subset=['SituationID'])

#binary
pass_data = data[data['Play Type'] == 1]
rush_data = data[data['Play Type'] == 0]

#target
target_column = 'Yards Gained'

#train test for both
X_train_pass, X_test_pass, y_train_pass, y_test_pass = train_test_split(
    pass_data[features_pass], pass_data[target_column], test_size=0.2, random_state=42)
X_train_rush, X_test_rush, y_train_rush, y_test_rush = train_test_split(
    rush_data[features_rush], rush_data[target_column], test_size=0.2, random_state=42)

#RF
rf_pass = RandomForestRegressor(n_estimators=100, random_state=42)
rf_rush = RandomForestRegressor(n_estimators=100, random_state=42)
rf_pass.fit(X_train_pass, y_train_pass)
rf_rush.fit(X_train_rush, y_train_rush)

#pred & calc RF
predictions_rf_pass = rf_pass.predict(X_test_pass)
predictions_rf_rush = rf_rush.predict(X_test_rush)
rmse_rf_pass = sqrt(mean_squared_error(y_test_pass, predictions_rf_pass))
rmse_rf_rush = sqrt(mean_squared_error(y_test_rush, predictions_rf_rush))
print("RF RMSE for Pass Model =", rmse_rf_pass)
print("RF RMSE for Rush Model =", rmse_rf_rush)

#XBG
xgb_pass = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, seed=42)
xgb_rush = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, seed=42)
xgb_pass.fit(X_train_pass, y_train_pass)
xgb_rush.fit(X_train_rush, y_train_rush)

#pred & calc XGB
predictions_xgb_pass = xgb_pass.predict(X_test_pass)
predictions_xgb_rush = xgb_rush.predict(X_test_rush)
rmse_xgb_pass = sqrt(mean_squared_error(y_test_pass, predictions_xgb_pass))
rmse_xgb_rush = sqrt(mean_squared_error(y_test_rush, predictions_xgb_rush))
print("XGBoost RMSE for Pass Model =", rmse_xgb_pass)
print("XGBoost RMSE for Rush Model =", rmse_xgb_rush)
