#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:12:26 2024

@author: colinbehr
"""

import pandas as pd
import requests
from lxml import html
import time
from random import randint

import os
os.chdir('/Users/colinbehr/Downloads')

def scrape_nfl_rushing_stats(year):
    url = f'https://www.nfl.com/stats/team-stats/offense/rushing/{year}/reg/all'
    
    # Get server request
    response = requests.get(url)
    
    # Parse 
    tree = html.fromstring(response.content)
    
    # XPath to find all rows with team stats
    team_rows_xpath = "//tr[.//div[contains(@class, 'd3-o-club-shortname')]]"
    team_rows = tree.xpath(team_rows_xpath)
    
    all_teams_stats = []
    
    for row in team_rows:
        # Extract all td elements from the row
        team_stats = [td.text_content().strip() for td in row.findall('td')]
        
        # Exclude name cell and make sure number of columns match headers
        if len(team_stats) == 11:
            # Match with correct headers
            headers = ["Team", "Att", "Rush Yds", "YPC", "TD", "20+", "40+", "Lng", "Rush 1st", "Rush 1st%", "Rush FUM"]
            team_stats_dict = dict(zip(headers, team_stats))
            all_teams_stats.append(team_stats_dict)
        else:
            raise ValueError("The number of columns does not match the expected headers.")
    
    return all_teams_stats


# Headers for DataFrame
headers = ["Year", "Team", "Att", "Rush Yds", "YPC", "TD", "20+", "40+", "Lng", "Rush 1st", "Rush 1st%", "Rush FUM"]

# Create empty list to store data for all teams and years
all_years_data = []

# Increment season
for year in range(2012, 2023):
    try:
        print(f"Scraping data for year: {year}")
        yearly_stats = scrape_nfl_rushing_stats(year)
        for stats in yearly_stats:
            stats['Year'] = year  # Add year to data
            all_years_data.append(stats)  # Add stats to corresponding year
        print(f"Data for year {year} scraped successfully.")
        
        # Be a polite guest
        time.sleep(randint(5, 10))
        
    except Exception as e:
        print(f"An error occurred for year {year}: {e}")

# Make a DataFrame
df = pd.DataFrame(all_years_data, columns=headers)

# Save to Excel
df.to_excel('nfl_rushing_stats.xlsx', index=False)

print("Scraping complete. Data saved to nfl_rushing_stats.xlsx.")
