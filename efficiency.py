# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 10:30:42 2018

@author: Sumin Lee

Calculate fuel efficiency in various scale
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

len_data = 2044

def plot_2D(data_X, data_y, data_y2, cases):

    plt.plot(data_X, data_y, color='blue', linewidth = 3)
    plt.plot(data_X, data_y2, color='red', linewidth = 3)
    
    plt.xlabel('time')
    plt.xticks(())
    plt.yticks(())
    
    plt.show()

        
        

#avg of self and neighboor
def smoother(fuel, len_data):
    fuel_3avg = [fuel[0]]
    for i in range(1, len_data-1):
        fuel0 = float(fuel[i-1])
        fuel1 = float(fuel[i])
        fuel2 = float(fuel[i+1])
        
        fuel_3avg.append((fuel0+fuel1+fuel2)/3)
    fuel_3avg.append(fuel[len_data-1])
    return fuel_3avg

def instanteff(stoplist, partition, fuel, dist, ndata):
    for stop in stoplist:
        if ndata>stop[0] and ndata<stop[1]:
            return -1
    eff = -1

    nowfuel = fuel[ndata]
    nowdist = dist[ndata]
    p = 0
    for i in range(3):
        if ndata>partition[i] and ndata<partition[i+1]:
            p = partition[i]
        
    while ndata >= p:
        ndata = ndata - 1
        sfuel = fuel[ndata]
        sdist = dist[ndata]
        if sfuel > nowfuel:
            eff = ((nowdist - sdist) / ((sfuel - nowfuel)))
            break
    return eff
        
def mineff(stoplist, time, partition, fuel, dist, ndata):
    for stop in stoplist:
        if ndata>stop[0] and ndata<stop[1]:
            return -2
    eff = -1

    cp = ndata
    nowfuel = fuel[ndata]
    nowdist = dist[ndata]
    p = 0
    for i in range(3):
        if ndata>partition[i] and ndata<partition[i+1]:
            p = partition[i]

    while ndata > p:
        if (time[cp] - time[ndata]) < 55:
            ndata = ndata -1
        else:
            break

    while ndata >= p:
        ndata = ndata - 1
        sfuel = fuel[ndata]
        sdist = dist[ndata]
        if sfuel > nowfuel:
            eff = ((nowdist - sdist) / ((sfuel - nowfuel)))
            break
    return eff    
    
    
d1 = pd.read_csv("data3.csv", sep = ",")


pfuel = np.array(d1["Predicted Fuel Level"])
fuel = np.array(d1["Fuel Level"])
dist = np.array(d1["Dist"])
speed = np.array(d1["Vehicle speed"])
time_sec = np.array(d1["Time(sec)"])

#find out when the fuel is charged
partition = []
for i in range(0, len_data-2):
    fuel[i] = fuel[i]
    fueldiff = fuel[i+1] - fuel[i]
    
    if fueldiff > 20*0.35:
        partition.append(i+1)

print (partition)

#find out when the car was stopped before 1st charge
i = -1
stoplist = []
while i < len_data:
    i = i + 1
    if speed[i] == 0 and i < len_data-1:
        cnt = 0
        start = i
        i = i + 1
        while i < len_data:
            if speed[i] != 0:
                break
            i = i + 1
            cnt = cnt + 1
            end = i
        if cnt > 5:
            if end == len_data:
                end = end - 1
            stoplist.append([start, end])



def fueleffgap1(partition, stoplist, fuel):
    
    p1 = partition[0]
    p2 = partition[1]
    p3 = len_data
    p = [0, p1, p2, p3]
    
    newstoplist = []
    for stop in stoplist:
        for i in range(3):
            if stop[0] > p[i] and stop[1] < p[i+1]:
                newstoplist.append(stop)
                break
            
    newstoplist = stoplist
    #calculate fuel efficiency (start~stop) 
    startdist = dist[0]
    startfuel = fuel[0]
    startpair = [0, 0]
    possibledist = []
    eff = []
    for pair in stoplist:
        nowfuel = fuel[pair[0]]
        nowdist = dist[pair[0]]
        
        for p in partition:
            if startpair[1] < p and pair[0] > p:
                nowfuel = nowfuel - fuel[p]
        
        if startfuel == nowfuel:
            startfuel = fuel[pair[1]]
            startdist = dist[pair[1]]
            continue
        noweff = ((nowdist - startdist) /( (startfuel - nowfuel)))
        if startfuel-nowfuel < 0.005:
            continue
        possdist = noweff*nowfuel
        possibledist.append(possdist)
        eff.append(noweff)
        
        startpair = pair
        startfuel = fuel[pair[1]]
        startdist = dist[pair[1]]

    avg = 0
    for e in eff:
        avg = avg + e
    avg = avg /len(eff)

    print ("\navg of small gap(between stops) fuel efficiency is: ", avg, "\n")
    
 
#print stoplist   
fueleffgap1(partition, stoplist, fuel)

#calculate fuel efficiency(charge~recharge)
startdist = dist[0]
startfuel = fuel[0]
partition.append(len_data-1)


print ("\n\n===efficiency in big gap(charge~recharge)==")

for time in partition:
    fueldiff = (startfuel - fuel[time-1])
    distdiff = dist[time-1]- startdist
    if distdiff == 0:
        continue
    bigeff = distdiff/fueldiff
    
    print ("\ninitial fuel: ", startfuel, "final fuel: ", fuel[time-1], "diff: ", fueldiff)
    print ("initial dist: ", startdist, "final dist: ", dist[time-1], "diff: ", distdiff)
    print ("the efficiency is: ", bigeff)
    
    startfuel = fuel[time]
    startdist = dist[time]

insteff = [-1] 

minueff = [-1]

for i in range(1, len_data):
    insteff.append(instanteff(stoplist, partition, pfuel, dist, i))
    minueff.append(mineff(stoplist, time_sec, partition, pfuel, dist, i))

avgeff = [0, ]
len_eff = len_data
len_eff1 = len_data
avg = insteff[0]
mvag = minueff[0]
for i in range(1, len(insteff)):
    e = insteff[i]
    e1 = minueff[i]
    if e < 0:
        len_eff = len_eff -1
    else:
        avg = avg + e    
    if e1 < 0:
        len_eff1 = len_eff1 -1
    else:
        mvag = mvag + e1

avg = avg /len_eff
mvag = mvag / len_eff1
print ("\n\navg of instant fuel efficiency is : ", avg, mvag, "\n")

fuel_1 = []
for i in range(len_data):
    fuel_1.append(pfuel[i])


for i in range(len_data):
    if i <= partition[0]:
        fuel_1[i] = fuel_1[i] + fuel_1[partition[0]] + fuel_1[partition[1]]
        fuel_1[i] = fuel_1[i] - fuel_1[partition[0]-1] - fuel_1[partition[1]-1]
    if i > partition[0] and i <= partition[1]:
        fuel_1[i] = fuel_1[i] + fuel_1[partition[1]] - fuel_1[partition[1]-1]

for i in range(1, len_data):
    avgeff.append(dist[i]/(fuel_1[0] - fuel_1[i]))

print ("Average fuel efficiency is: ", avgeff[len_data-1])


avgspd = 0
count = 0
for i in range(len_data):
    if speed[i] != 0:
        avgspd = avgspd + speed[i]
        count = count + 1
print (avgspd/count)
'''
fuel_smt = smoother(fuel, len_data)

insteff_smt = [-1]   
for i in range(1, len_data):
    insteff_smt.append(instanteff(fuel_smt, dist, i))
   
avg = 0
len_eff1 = len_data
for i in range(len_data):
    if insteff_smt[i] < 0:
        len_eff1 = len_eff-1
        continue
    avg = avg + e
avg = avg /len_eff1
print ("\n\navg of instant fuel(smt) efficiency is : ", avg, "\n")
'''
plot_2D(time_sec, insteff, speed, len_data)

insteff = pd.Series(insteff)
minueff = pd.Series(minueff)
avgeff = pd.Series(avgeff)


timedist = pd.DataFrame({'Time(sec)' : d1["Time(sec)"],
                         'Dist': d1["Dist"],
                         'Vehicle speed' : d1["Vehicle speed"],
                         'Fuel Level' : d1["Fuel Level"],
                         'Acc': d1["Acc"],
                         'Predicted Fuel Level':d1["Predicted Fuel Level"],
                         'Instant Fuel Efficiency': insteff,
                         '(Minute) Fuel Efficiency' : minueff,
                         'Average Fuel Efficiency': avgeff})
                         

timedist.to_csv('data2.csv', index = False)

