# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 04:01:34 2015

@author: user
"""

# pip install nflgame
# conda install seaborn

import nflgame
import glob
import pandas as pd

# cd ~/DAT8/project/qb_projections/data/temp/attempt_2
games_all = nflgame.games(range(2009, 2014), kind='REG')

# cd ~/Desktop/DAT8/project/qb_projections/data/temp/attempt_2/2014
# games_all = nflgame.games(2013)
for game in games_all:
    p = game.players.filter(passing_att=lambda x:x>1).csv('%s.csv' % game)
#    p = game.players.filter(passing_att=lambda x:x>0).csv('%s.csv' % game.gamekey)


cols = ['name','id','home','team','pos','passing_att','passing_cmp',
'passing_ints','passing_tds','passing_twopta','passing_twoptm','passing_yds',
'rushing_att', 'rushing_tds', 'rushing_twopta', 'rushing_twoptm', 'rushing_yds',
'fumbles_lost'
]

path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/temp/attempt_2'
#path =r'~/DAT8/project/qb_projections/data/temp/attempt_2'
years = range(2009, 2014)
dfs = []
for year in years:
    files = glob.glob(path + "/" + str(year) + "/*.csv")
    for file_ in files:
#        print str(file_)
        tempdf = pd.read_csv(file_)
        missing_col = list(frozenset(cols) - frozenset(tempdf.columns))
        if len(missing_col) > 0:
#            print missing_col
            included_col = list(frozenset(cols) - frozenset(missing_col))
#            print included_col
            tempdf = tempdf[included_col]
            for col in missing_col:
                tempdf[col] = 0
        else:
            tempdf = tempdf[cols]
        tempdf = tempdf.fillna(0)
        tempdf['year'] = year
        home_team = tempdf.team[tempdf.home == 'yes'].unique().repeat(tempdf.shape[0])
        visitor = tempdf.team[tempdf.home == 'no'].unique().repeat(tempdf.shape[0])
        tempdf['home_team'] = home_team
        tempdf['visitor'] = visitor
        dfs.append(tempdf)

  
big_frame = pd.concat(dfs, ignore_index=True)
big_frame.isnull().sum()

# cd ~/Desktop/DAT8/project/qb_projections/data/lines_csv
#path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\lines_csv'
path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/lines_csv'
allFiles = glob.glob(path + "/*.csv")

dfLines = []
for file_ in allFiles:
    dfLines.append(pd.read_csv(file_))
    
bigDfLines = pd.concat(dfLines, ignore_index=True)
bigDfLines.dtypes
del bigDfLines['Unnamed: 7']
bigDfLines.isnull().sum()
del bigDfLines['Total Line']
del bigDfLines['Total Line ']
bigDfLines['year'] = bigDfLines.Date.str[-4:].astype(int)
bigDfLines.Line.hist()

bigDfLines[bigDfLines.year >= 2009].groupby('year').Line.boxplot()
bigDfLines[bigDfLines.year >= 2009].boxplot(column='Line', by='year')


# cd ~/Desktop/DAT8/project/qb_projections/data/stats_csv
#path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\stats_csv'
path =r'/Users/lindenthetree/DAT8/project/qb_projections/data/stats_csv'
allFiles = glob.glob(path + "/*.csv")

dfStats = []
for file_ in allFiles:
    dfStats.append(pd.read_csv(file_))
    
bigDfStats = pd.concat(dfStats, ignore_index=True)
bigDfStats.dtypes
del bigDfStats['Unnamed: 30']
del bigDfStats['Unnamed: 33']
del bigDfStats['Unnamed: 35']
bigDfStats['year'] = bigDfStats.Date.str[-4:]

bigDfStats.head()
len(bigDfStats.TeamName.unique())
team_names = bigDfStats.TeamName.unique()
dict_map = dict(zip(team_names,range(0, len(team_names))))
bigDfStats['team_int'] = bigDfStats.TeamName.map(dict_map)



bigStatsCopy = bigDfStats.dropna()
bigDfStats['paydof'] = bigDfStats.PassYdsOff.astype(int)

bigDfStats.plot(kind='scatter', x='paydof', y='ScoreDef')

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import cm
#dir(cm)

plt.rcParams['figure.figsize'] = (6, 4)
plt.rcParams['font.size'] = 14
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
bigDfStats.plot(kind='scatter', x='ScoreDef', y='ScoreOff', c='team_int', alpha=.3, colormap='spectral')
bigDfStats['ScoreDelta'] = bigDfStats.ScoreOff-bigDfStats.ScoreDef

test = bigDfStats.groupby(['year','team_int']).ScoreDelta.mean().reset_index()
test['year_int'] = test.year.astype(int)
test['team_int'] = test.team_int.astype(int)

test.plot(kind='scatter', x='year_int',y='ScoreDelta',
c='team_int', alpha=.3, colormap='spectral')

import seaborn as sns
sns.heatmap(big_frame[cols].corr())