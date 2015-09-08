# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 18:52:49 2015

@author: vyang91
"""
# %reset
# cd ~/Desktop/DAT8/data

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 8)
plt.style.use('ggplot')

movies = pd.read_csv('imdb_1000.csv')

# 979 rows, 6 columns
movies.shape

# star rating is a column of floats
# duration is a column of ints
# title, content rating, genre, and actors list are objects
movies.dtypes

# average movie duration is a little over 2 hours
round(movies.duration.mean(), 2)

# 5 shortest and 5 longest movies
movies.sort('duration').head()
movies.sort('duration', ascending=0).head()

# histogram of movie durations using default bin amounts
movies.duration.plot(kind='hist')
plt.xlabel('Movie Duration (mins)')
plt.ylabel('Count')

# boxplot of movie durations
movies.boxplot(column='duration')

# count of each content rating
movies.content_rating.value_counts(dropna=0)

# bar plot of value counts
movies.content_rating.value_counts(dropna=0).plot(kind='bar')
plt.xlabel('Content Rating')
plt.ylabel('Count')

# convert 'not rated', 'approved', 'passed', 'gp' to 'unrated'
movies.content_rating[movies.content_rating.isin(['NOT RATED', 'APPROVED', 'PASSED', 'GP'])] = 'UNRATED'

# convert 'x', 'tv-ma' to 'nc-17'
movies.content_rating[movies.content_rating.isin(['X', 'TV-MA'])] = 'NC-17'

# count missing values in each column
movies.isnull().sum()

# examine movies with null content rating
movies[movies.content_rating.isnull()]
# originally rated US:M, now considered PG (https://en.wikipedia.org/wiki/Motion_Picture_Association_of_America_film_rating_system#From_M_to_GP_to_PG)
movies.content_rating[movies.content_rating.isnull()] = 'PG'

# 7.95 average rating for movies >= 2 hours vs. 7.84 rating for movies < 2 hours
round(movies[movies.duration >= 120].star_rating.mean(), 2)
round(movies[movies.duration < 120].star_rating.mean(), 2)

# scatter plot of duration vs. star rating seems to indicate some relationship between the two
movies.plot(kind='scatter', x='duration', y='star_rating', alpha=.3)

# average durations for each genre, also sorted by length descending
movies.groupby('genre').duration.mean()
movies.groupby('genre').duration.agg(['mean']).sort('mean', ascending=0)

# boxplots of movie durations by content rating
movies.boxplot(column='duration', by='content_rating')

# highest star rated movie for each genre
movies = movies.sort('star_rating', ascending=0)
movies[~movies.genre.duplicated()]
# compare with
genre_max = movies.groupby('genre').star_rating.agg(['max']).sort('max', ascending=0)
genre_max['genre'] = genre_max.index.values
pd.merge(genre_max, movies, left_on=['genre', 'max'], right_on=['genre', 'star_rating']).sort('star_rating', ascending=0)

# movies with duplicated titles sorted alphabetically then by star rating; they appear to be distinct movies
movies[movies.title.isin(movies[movies.title.duplicated()].title.tolist())].sort(['title','star_rating'], ascending=[1, 0])

# identify genres with count >= 10 then subset dataframe and find grouped means
genre_10 = movies.genre.value_counts() >= 10
genre_10 = genre_10[genre_10 == 1].index
movies[movies.genre.isin(genre_10)].groupby('genre').star_rating.mean()
movies[movies.genre.isin(genre_10)].groupby('genre').star_rating.agg(['mean']).sort('mean', ascending=0)

# clean actors list
actors = movies.actors_list.tolist()
actors = [actor.replace('[', '').replace('u\'', '').replace('u\"', '').replace('\'', '').replace('\"', '').replace(']', '') for actor in actors]
actors = [actor.split(', ') for actor in actors]
test = [len(i) for i in actors]
float(sum(test))/len(test) == 3.0 # check that each list is made of three actors

# which actor appears the most in the top 3 actors list of top 1000 movies
actors_flat = [item for sublist in actors for item in sublist]
from collections import Counter
actors_count = Counter(actors_flat)
actors_count.most_common(5)

# which actor has the highest average rating in the top 1000 movies
#movies['actors_list_clean'] = actors
#movies['actors_clean_str'] = [', '.join(actor) for actor in actors]

movies['actor_1'] = [actor[0] for actor in actors]
movies['actor_2'] = [actor[1] for actor in actors]
movies['actor_3'] = [actor[2] for actor in actors]

# which two actors work together the most often in top 1000 movies
