
# Un-Bear-able Offense: Using Machine Learning for Chicago Bears Play Calling

## Author
Colin Behr  
*Depressed Bears Fan*

## Overview
This project integrates machine learning into play-calling decisions for the Chicago Bears. By analyzing historical game data, weather conditions, and team performance metrics, 
the aim is to implement them to recommend optimal plays (i.e., pass deep left) for any in-game situations.


## Structure
```
├── README.md                       # Project overview and instructions
├── PFR                             # Various scraping files to get play-by-play from profootballreference
├── ALS_NOTWORKING.py               # ALS model pipeline (currently pseudocode/in development)
├── API Call.py                     # Fetches weather data via Visual Crossing API
├── Game Coords Adding.py           # Adds game coordinates for weather calls
├── Hourly Weather Datasheet Creation.py # Creates hourly weather data entries (i.e., 3 hours for 1 full game)
├── NFL Passing O.py                # Scrapes ALL NFL passing offense stats
├── NFL Rushing O.py                # Scrapes ALL NFL rushing offense stats
├── RF Model v1.py                  # Random Forest model for predicting play type (i.e., pass or run)
├── ToGo_Sort.py                    # Categorizes plays by yards-to-go situations (i.e., 3rd and 9 = Long)
├── preprocessing.py                # Various data preprocessing 
├── conversions.py                  # Converts categorical data to numeric values
├── datasets/                       # all datasets used to create ALL.csv/xlsx
│   ├── ALL Bears Data.xlsx
│   ├── nfl_passing_stats.xlsx
│   ├── nfl_rushing_stats.xlsx
│   ├── nfl_Dpassing_sscores.xlsx
│   ├── nfl_rushing_sscores.xlsx
│   └── defense_scoring.xlsx

```


### Data Collection
- **Play-by-play** Run files in PFR folder as needed to collect all game specifics from ProFootballReference (start with `Scraping PFR.py`)
- **Weather**: Run `API Call.py` to collect weather data for games.(reference stadium locations csv as needed)
- **NFL Statistics**: Run `NFL Passing O.py` and `NFL Rushing O.py` to scrape ALL TEAMS' offense stats.

### Modeling
**Random Forest Model**:  
Train and evaluate play-type prediction

**Linear Regression**:
See ALS Model for various linear regressions used to predict yardage gained vs actual yards on past plays.

**ALS Model (Experimental)**:  
Work in progress; refer to `ALS(5).py` and other models in testing branch.

### Evaluation
Check outputs for RMSE values and ALS modeling potential success

## Features
- **Play Type Prediction**: Pass vs. Run decisions based on game context.
- **Weather Consideration**: Factors in real-time and historical weather data.
- **Defense/Offense Weighting**: Incorporates team performance metrics into recommendations.

## Dependencies/Packages
- Python 3.7+
- PySpark
- pandas
- scikit-learn
- requests
- misc. built-in packages

## Acknowledgments
- NFL and profootballreference for public data access
- Visual Crossing Weather for weather data API.
- Open-source contributors to PySpark and scikit-learn

## Contribute to the Repo & Models! #BearDown
