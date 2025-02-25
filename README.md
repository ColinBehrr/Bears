
# Un-Bear-able Offense: Bad Play Calling meets Machine Learning

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
├── API Call.py                     # Fetches weather data via Visual Crossing API
├── Game Coords Adding.py           # Adds game coordinates for weather calls
├── Hourly Weather Datasheet Creation.py # Creates hourly weather data entries (i.e., 3 hours for 1 full game)
├── NFL Passing O.py                # Scrapes ALL NFL passing offense stats
├── NFL Rushing O.py                # Scrapes ALL NFL rushing offense stats
├── datasets/                       # all datasets used to create ALL.csv/xlsx
│   ├── ALL.csv                     #FINAL dataset containing all game data
│   ├── NFL Stadium Latitude and Longitude.csv
├── exports/
│   ├── nfl_passing_stats.xlsx/csv
│   ├── nfl_rushing_stats.xlsx/csv
│   ├── nfl_passing_scores.xlsx/csv
│   ├── nfl_rushing_scores.xlsx/csv
│   └── defense_scoring.xlsx/csv

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
