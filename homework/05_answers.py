# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 15:52:49 2015

@author: vyang91
"""

# cd ~/Desktop/DAT8/data
# %reset

import pandas as pd
import matplotlib.pyplot as plt

movies = pd.read_csv('imdb_1000.csv')

movies.shape
# 979 rows, 6 columns