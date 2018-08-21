# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 10:30:42 2018

@author: Sumin Lee

Trying to find out fuel efficiency
"""

import numpy as np
import pandas as pd



dlen = 2044
'''
def longestdecsubs(list):
    P = []
    M = []

    L = 0
    for i in range(dlen):
        #binary search for the smallest positive
        L = 0
'''

#avg of self and neighboor
def smoother(fuel, dlen):
    fuel_3avg = []
    for i in range(1, dlen-1):
        fuel0 = float(fuel[i-1])
        fuel1 = float(fuel[i])
        fuel2 = float(fuel[i+1])
        
        fuel_3avg.append((fuel0+fuel1+fuel2)/3)
    return fuel_3avg




d1 = pd.read_csv("data1.csv", sep = ",")

fuel = np.array(d1["Fuel Level"])
dist = np.array(d1["Dist"])

eff = []

len_data = 2044


#find out when the fuel is charged
partition = []
for i in range(0, dlen-1):
    fuel[i] = fuel[i]
    fueldiff = fuel[i+1] - fuel[i]
    
    if fueldiff > 20:
        partition.append(i+1)

#partition = [199, 1550]

fuel_1 = fuel[:partition[0]]
fuel_2 = fuel[partition[0]:partition[1]]
fuel_3 = fuel[partition[1]:]

fuel_1_smt = smoother(fuel_1, partition[0])
fuel_2_smt = smoother(fuel_2, partition[1])
fuel_3_smt = smoother(fuel_3, partition[2])



