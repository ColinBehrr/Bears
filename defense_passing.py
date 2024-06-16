#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:20:11 2024

@author: colinbehr
"""

import pandas as pd
import requests
from lxml import html
import time
from random import randint

import os
os.chdir('/Users/colinbehr/Downloads') #change wd to downloads


def scrape_nfl_defense_passing_stats(year):
    #placekeeper URL
    url = f'https://www.nfl.com/stats/team-stats/defense/passing/{year}/reg/all'
    
    #request 
    response = requests.get(url)
    
    #parse
    tree = html.fromstring(response.content)
    
    #XPath to find all teams except the Bears
    team_rows_xpath = "//tr[.//div[contains(@class, 'd3-o-club-fullname')]]"
    team_rows = tree.xpath(team_rows_xpath)
    
    all_teams_stats = []
    
    for row in team_rows:
        #td elements
        team_stats = [td.text_content().strip() for td in row.findall('td')]
        
        #extract all team names (first element)
        team_name = team_stats.pop(0)

        #adjust for columns on page
        expected_columns = 14
        if len(team_stats) == expected_columns:
            #team + year as first two columns
            team_stats.insert(0, year)
            team_stats.insert(1, team_name)
            all_teams_stats.append(team_stats)
        else:
            print(f"Unexpected number of columns for {team_name} in year {year}")

    return all_teams_stats

#headers
headers = ["Year", "Team", "Att", "Cmp", "Cmp%", "Yds/Att", "Yds", "TD", "INT", "Rate", "1st", "1st%", "20+", "40+", "Lng", "Sck"]

#initialize empty list to store stats by year
all_years_data = []

#increment season
for year in range(2012, 2023):
    try:
        print(f"Scraping data for year: {year}")
        yearly_stats = scrape_nfl_defense_passing_stats(year)
        all_years_data.extend(yearly_stats)  #add all stats for respective year
        #print(yearly_stats)
    
        #being a polite guest :)
        time.sleep(randint(5, 10))
    except Exception as e:
        print(f"An error occurred for year {year}: {e}")

#df
df = pd.DataFrame(all_years_data, columns=headers)

#export
df.to_excel('bears_defense_passing.xlsx', index=False)
