# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 10:30:42 2018

@author: Sumin Lee

Calculate fuel efficiency in various scale
"""

import numpy as np
import pandas as pd

len_data = 2044


#avg of self and neighboor
def smoother(fuel, len_data):
    fuel_3avg = []
    for i in range(1, len_data-1):
        fuel0 = float(fuel[i-1])
        fuel1 = float(fuel[i])
        fuel2 = float(fuel[i+1])
        
        fuel_3avg.append((fuel0+fuel1+fuel2)/3)
    return fuel_3avg


d1 = pd.read_csv("data1.csv", sep = ",")

fuel = np.array(d1["Fuel Level"])
dist = np.array(d1["Dist"])
speed = np.array(d1["Vehicle speed"])


len_data = 2044


#find out when the fuel is charged
partition = []
for i in range(0, len_data-1):
    fuel[i] = fuel[i]
    fueldiff = fuel[i+1] - fuel[i]
    
    if fueldiff > 20:
        partition.append(i+1)

#partition = [199, 1550]

fuel_1 = fuel[:partition[0]]
fuel_2 = fuel[partition[0]:partition[1]]
fuel_3 = fuel[partition[1]:]

#find out when the car was stopped
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

print ("car stops during", stoplist)


#calculate fuel efficiency (start~stop)
startdist = dist[0]
startfuel = fuel_1[0]
eff = []
for pair in stoplist:
    nowfuel = fuel_1[pair[0]]
    nowdist = dist[pair[0]]
    
    noweff = (startfuel - nowfuel) / (nowdist - startdist)
    
    eff.append(noweff)
    
    startfuel = fuel_1[pair[1]]
    startdist = dist[pair[1]]
    
print (eff, "\n")

#calculate fuel efficiency(charge~recharge)
startdist = dist[0]
startfuel = fuel_1[0]
partition.append(len_data-1)

for time in partition:
    fueldiff = startfuel - fuel[time-1]
    distdiff = dist[time-1]- startdist
    bigeff = (fueldiff/ distdiff)
    
    print ("\ninitial fuel: ", startfuel, "final fuel: ", fuel[time-1], "diff: ", fueldiff)
    print ("initial dist: ", startdist, "final dist: ", dist[time-1], "diff: ", distdiff)
    print ("the efficiency is: ", bigeff)
    
    startfuel = fuel[time]
    startdist = dist[time]
    
