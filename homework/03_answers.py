# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:14:02 2015

@author: yang
"""
# cd ~/Desktop/DAT8/data
# %reset
import csv
with open('chipotle.tsv', 'rU') as f:
    dialect = csv.Sniffer().sniff(f.read(1024))
    f.seek(0)
    file_nested_list = [row for row in csv.reader(f, dialect)]

header = file_nested_list[0]
data = file_nested_list[1:]

lst_prices = [float(i[4][1:]) for i in data]
sum_prices = sum(lst_prices)
lst_order_ids = [int(i[0]) for i in data]
num_orders = len(set(lst_order_ids))
avg_order_price = sum_prices/num_orders

lst_canned = [item_order[3] for item_order in data if item_order[2].lower().find('canned') >= 0]
lst_canned_unique = set(lst_canned)

lst_burrito_topping = [item_order[3] for item_order in data if item_order[2].lower().find('burrito') >= 0]
count_burrito_topping = [i.count(',') + 1 for i in lst_burrito_topping]
avg_burrito_topping = float(sum(count_burrito_topping))/len(lst_burrito_topping)

lst_chip_names = set([item_order[2] for item_order in data if item_order[2].lower().find('chip') >= 0])
lst_chip_count = []
for chip_name in lst_chip_names:
    int_chip_count = 0
    for item_order in data:
        if item_order[2] == chip_name:
            int_chip_count += 1 * int(item_order[1])
    lst_chip_count.append(int_chip_count)
dict_chip_count = dict(zip(lst_chip_names, lst_chip_count))