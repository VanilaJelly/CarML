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

def instanteff(fuel, dist, ndata):
    eff = -1
    nowfuel = fuel[ndata]
    nowdist = dist[ndata]
    while ndata > 0:
        ndata = ndata - 1
        sfuel = fuel[ndata]
        sdist = dist[ndata]
        if sfuel > nowfuel:
            eff = ((nowdist - sdist) / ((sfuel - nowfuel)))
            break
    return eff
        

d1 = pd.read_csv("data1.csv", sep = ",")


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
'''
fuel_1 = fuel[:partition[0]]
fuel_2 = fuel[partition[0]:partition[1]]
fuel_3 = fuel[partition[1]:]
'''
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

print ("car stops during", stoplist)


def fueleffgap1(partition, stoplist, fuel):
    #calculate fuel efficiency (start~stop) 
    startdist = dist[0]
    startfuel = fuel[0]
    startpair = [0, 0]
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
for i in range(1, len_data):
    insteff.append(instanteff(fuel, dist, i))
   
insteff_1 = []
len_eff = len_data
avg = 0
for i in range(len(insteff)):
    e = insteff[i]
    if e < 0:
        len_eff = len_eff -1
        continue
    avg = avg + e
    insteff[i] = insteff[i]

avg = avg /len_eff
print ("\n\navg of instant fuel efficiency is : ", avg, "\n")

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

plot_2D(time_sec, insteff, speed, len_data)

    
