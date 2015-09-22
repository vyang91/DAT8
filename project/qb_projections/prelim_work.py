# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 04:01:34 2015

@author: user
"""

import nflgame
import glob
import pandas as pd

# cd ~/Desktop/DAT8/project/qb_projections/data/temp/attempt_1
# games_all = nflgame.games(range(2009, 2014), kind='REG')

# cd ~/Desktop/DAT8/project/qb_projections/data/temp/attempt_2/2014
games_all = nflgame.games(2013)
for game in games_all:
    p = game.players.filter(passing_att=lambda x:x>1).csv('%s.csv' % game)
#    p = game.players.filter(passing_att=lambda x:x>0).csv('%s.csv' % game.gamekey)

    
path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\temp\attempt_0'
allFiles = glob.glob(path + "/*.csv")
len(allFiles)

dfs = []
for file_ in allFiles:
    dfs.append(pd.read_csv(file_))
    
dfs1 = []
for file_ in allFiles[0:len(allFiles)/4]:
    dfs1.append(pd.read_csv(file_))
    
dfs2 = []
for file_ in allFiles[len(allFiles)/4:len(allFiles)/2]:
    dfs2.append(pd.read_csv(file_))
    
dfs3 = []
for file_ in allFiles[len(allFiles)/2:3*len(allFiles)/4]:
    dfs3.append(pd.read_csv(file_))

dfs4 = []
for file_ in allFiles[3*len(allFiles)/4:len(allFiles)]:
    dfs4.append(pd.read_csv(file_))

dfs5 = pd.concat([dfs3[0], dfs4[0]])
dfs6 = pd.concat([dfs3[1], dfs4[1]])

cols = ['name','id','home','team','pos','passing_att','passing_cmp',
'passing_ints','passing_tds','passing_twopta','passing_twoptm','passing_yds',
'rushing_att', 'rushing_tds', 'rushing_twopta', 'rushing_twoptm', 'rushing_yds'
]

test_frame = pd.concat(dfs1)
test_frame[cols]
    
big_frame = pd.concat(dfs, ignore_index=True)
big_frame[cols].head()
#frame = pd.concat(list_)
#
#
#for df in dfs:
#    df_max 

# cd ~/Desktop/DAT8/project/qb_projections/data/lines_csv
path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\lines_csv'
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
bigDfLines['year'] = bigDfLines.Date.str[-4:]
bigDfLines.Line.hist()
bigDfLines.Line.boxplot(by='year')
bigDfLines.groupby('year').Line.plot(kind='box')


# cd ~/Desktop/DAT8/project/qb_projections/data/stats_csv
path =r'C:\Users\user\Desktop\DAT8\project\qb_projections\data\stats_csv'
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
dir(cm)

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