# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import nflgame

games = nflgame.games(range(2009, 2016))
len(games) #1553 when 2009-2015

players = nflgame.combine_game_stats(games)

for p in players.rushing().sort("rushing_yds").limit(10):
    print p, p.rushing_yds

# cd ~/Desktop/DAT8/project/qb_projections
nflgame.combine(games).csv('season2009_2015.csv')

test = games[1552]
test.players.filter(passing_yds=lambda x:x>0).csv('qb_test.csv')

