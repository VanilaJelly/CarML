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
def longestdecsubs(X, l):
    P = np.zeros(l, 1)
    M = np.zeros(l, 1)

    L = 0
    for i in range(dlen):
        #binary search for the smallest positive
        lo = 1
        hi = L
        while lo <= hi:
            mid = ceil((lo+hi)/2)
            if X[M[mid]] < X[i]:
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo

        P[i] = M[newL-1]
        M[newL] = i

        if newL > L:
            L = newL

        result = []
        k = M[L]
        i = L-1
        while i >= 0:
            result = X[k] + result
            k = P[k]
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
speed = np.array(d1["Vehicle speed"])

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
'''
fuel_1_smt = smoother(fuel_1, partition[0])
fuel_2_smt = smoother(fuel_2, partition[1])
fuel_3_smt = smoother(fuel_3, partition[2])
'''

i = -1
stoplist = []
while i < partition[0]:
    i = i + 1
    if speed[i] == 0:
        cnt = 0
        start = i
        i = i + 1
        while speed[i] == 0:
            i = i + 1
            cnt = cnt + 1
            end = i
        if cnt > 5:
            stoplist.append([start, end])
            
            
print (stoplist)

startdist = dist[0]
startfuel = fuel_1[0]

for pair in stoplist:
    nowfuel = fuel_1[pair[0]]
    nowdist = dist[pair[0]]
    
    noweff = (startfuel - nowfuel) / (nowdist - startdist)
    
    eff.append(noweff)
    
    startfuel = fuel_1[pair[1]]
    startdist = dist[pair[1]]
    
    
print (eff)

print ("----------")
startdist = dist[0]
startfuel = fuel_1[0]

partition.append(len_data-1)
for time in partition:
    fueldiff = startfuel - fuel[time-1]
    distdiff = dist[time-1]- startdist
    bigeff = (fueldiff/ distdiff)
    print (startfuel, fuel[time-1], startdist, dist[time-1])
    print (time, partition, fueldiff, distdiff, bigeff)
    startfuel = fuel[time]
    startdist = dist[time]
    
'''
i = -1
distorig = dist[0]
fuelorig = fuel_1[0]
while i < partition[0]:
    i = i + 1
    if speed[i] == 0:
        sfuel = fuelorig - fuel_1[i]
        sdist = dist[i]- distorig
        print ("Fuel \t", sfuel)
        print ("Dist \t", sdist)
        if sdist != 0:
            seff = sfuel/sdist
        eff.append(seff)
        print ("Efficiency \t", seff)
        while speed[i] == 0:
            i = i + 1
            distorig = dist[i]
            fuelorig = fuel_1[i]


print (eff)

'''