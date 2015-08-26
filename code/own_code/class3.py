# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 19:22:08 2015

@author: user
"""

movies = ['tt0111161', 'tt1856010', 'tt0096694', 'tt0088763', 'tt1375666']

numbers = [];
for i in movies:
    numbers.append(i[2:])
print(numbers)

numbers2 = [int(i[1:]) for i in movies];
print(numbers2)

int_numbers = [int(i) for i in numbers2];
sum(int_numbers[0:3])
sum(int_numbers)

#####################

f = open('airlines.csv', 'rU')
file_string = f.read()
f.close()

with open('airlines.csv', 'rU') as f:
    file_string = f.read()

