# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:28:11 2018

@author: Sumin Lee
"""

import pandas as pd



#convert given date to second-scale
def conv_to_sec(time_split):
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 0]
    min_const = 60
    hour_const = 3600
    day_const = 60*60*24
    year_const = 60*60*24*365
    tinsec = time_split[5]
    tinsec = tinsec + min_const * time_split[4]
    tinsec = tinsec + hour_const * time_split[3]
    tinsec = tinsec + day_const * (time_split[2]-1)
    tinsec = tinsec + month[time_split[1]-2]*day_const + year_const * time_split[0]
    
    return tinsec



    
df = pd.read_csv("d1-n-data.csv", sep = ",")

time_split = []
time_in_sec = []

len_data = 2051


for i in range(0, len_data):
    time = df["time_slot"][i]
    time_split.append([])
    time_split[i].append(int(time[:4]) - 2018)  #year
    time_split[i].append(int(time[5:7]))        #month
    time_split[i].append(int(time[8:10]))       #day
    time_split[i].append(int(time[11:13]))      #hour
    time_split[i].append(int(time[14:16]))      #min
    time_split[i].append(float(time[17:-1]))    #sec
    
#fix t0 as 0
t0 = conv_to_sec(time_split[0])
for i in range(0, len_data):
    t1 = conv_to_sec(time_split[i])
    
    time_in_sec.append(t1-t0)

dist = [0]
for i in range(1, len_data):
    tdiff = time_in_sec[i] - time_in_sec[i-1]
    speed = float(df["Vehicle Speed"][i])
    speed0 = float(df["Vehicle Speed"][i-1])
    
    dist.append(dist[i-1] + tdiff*(speed+speed0)/2)
    
timeinsec = pd.Series(time_in_sec)
distances = pd.Series(dist)
fuel = df["Fuel Level"][:len_data]
vspeed = df["Vehicle Speed"][:len_data]

#except NODATA in fuellevel 
daterror = []
for i in range(len_data):
    try:
        float(fuel[i][:-1])
    except ValueError:
        daterror.append(i)

daterror.reverse()
        
for i in daterror:
    del timeinsec[i]
    del dist[i]
    del vspeed[i]
    del fuel[i]

timedist = pd.DataFrame({'Time(sec)' : timeinsec,
                         'Dist': dist,
                         'Vehicle speed' : vspeed,
                         'Fuel Level' : fuel})
                         
timedist.to_csv('data1.csv', index = False)

    
