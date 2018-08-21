# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:28:11 2018

@author: Sumin Lee

Calculate estimated distance, and average fuel level in minute.
"""

import pandas as pd
import numpy as np



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



    
df = pd.read_csv("re_data.csv", sep = ",")

time_split = []
time_in_sec = []

len_data = 2055

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

print ("time_in_sec calculated")

fuel = list(df["Fuel.Level"][:len_data])
vspeed = list(df["Vehicle.Speed"][:len_data])


#exclude "nan"
i = 0
while i < len_data:
    if np.isnan(fuel[i]) or np.isnan(vspeed[i]):
        vspeed = vspeed[:i] + vspeed[i+1:]
        fuel = fuel[:i] + fuel[i+1:]
        time_in_sec = time_in_sec[:i] + time_in_sec[i+1:]
        time_split = time_split[:i] + time_split[i+1:]
        len_data = len_data - 1
        i = i -1
    i = i + 1
    
print ("NaN data excluded")



'''
#makes sure 'nan' data excluded
print (vspeed[1230])
print (len_data)
'''

#calculate estimated distance
dist = [0]
for i in range(1, len_data):
    tdiff = time_in_sec[i] - time_in_sec[i-1]
    speed = vspeed[i]
    speed0 = vspeed[i-1]    
    dist.append(dist[i-1] + tdiff*(speed+speed0)/2)

print ("Dist calculated")

print(len(time_split))  
#calculate average fuel level in minute scale
   
#initialize the list with 1    
fuel_minavg = []
for i in range(len_data):
   fuel_minavg.append(-1) 
    
i = 0
while i < len_data:
    stt = i
    fuelavg = fuel[i]
    i = i + 1
    if i >= len_data:
        break
    
    while time_split[stt][4] == time_split[i][4]:
        fuelavg = fuelavg + fuel[i]
        i = i + 1
        if i >= len_data:
            break
    stop = i
    fuelavg = fuelavg/(stop-stt)

    for j in range(stt, i):
        fuel_minavg[j] = fuelavg
        
print ("avg fuel level(in minute) calculated")
 
#store datas into csv file
distances = pd.Series(dist)
timeinsec = pd.Series(time_in_sec)
timedist = pd.DataFrame({'Time(sec)' : timeinsec,
                         'Dist': dist,
                         'Vehicle speed' : vspeed,
                         'Fuel Level' : fuel})
                         
timedist.to_csv('data1.csv', index = False)

    