#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 19:06:18 2024

@author: colinbehr
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 17:55:22 2024

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
    #url
    url = f'https://www.nfl.com/stats/team-stats/defense/interceptions/{year}/reg/all'
    
    #request
    response = requests.get(url)
    
    #parse
    tree = html.fromstring(response.content)
    
    #xpath for all NFL defenses EXCEPT Bears
    team_rows_xpath = "//tr[.//div[contains(@class, 'd3-o-club-fullname') and not(contains(text(), 'Bears'))]]"
    team_rows = tree.xpath(team_rows_xpath)
    
    all_teams_stats = []
    
    for row in team_rows:
        #extract all td's
        team_stats = [td.text_content().strip() for td in row.findall('td')]
        
        #get team names
        team_name = team_stats.pop(0)

        #adjust for total columns
        expected_columns = 4
        if len(team_stats) == expected_columns:
            #make team+ year first two cells in row
            team_stats.insert(0, year)
            team_stats.insert(1, team_name)
            all_teams_stats.append(team_stats)
        else:
            print(f"Unexpected number of columns for {team_name} in year {year}")

    return all_teams_stats

#ALL headers
headers = ["Year", "Team", "INT", "INT TD", "INT Yds", "Lng"]

#initialize empty list
all_years_data = []

#seasons
for year in range(2012, 2023):
    try:
        print(f"Scraping data for year: {year}")
        yearly_stats = scrape_nfl_defense_passing_stats(year)
        all_years_data.extend(yearly_stats)  # Add all teams' stats for the year
        #print(yearly_stats)
    
        #being a polite guest :)
        time.sleep(randint(5, 10))
    except Exception as e:
        print(f"An error occurred for year {year}: {e}")

#df
df = pd.DataFrame(all_years_data, columns=headers)

#export
df.to_excel('defense_ints.xlsx', index=False)
