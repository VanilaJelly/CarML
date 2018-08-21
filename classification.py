# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:02:06 2018

@author: Sumin Lee
"""

import pandas as pd
import numpy as np


df = pd.read_csv("re_data.csv", sep = ",")

RPM = list(df["Engine.RPM"])
load = list(df["Engine.Load"])
speed = list(df["Vehicle.Speed"])
throttle = list(df["Throttle.Position"])

len_data = 2055
print ("File opened!")

#exclude "nan"
i = 0
while i < len_data:
    flag = 0
    if np.isnan(RPM[i]) :
        flag =1
    elif np.isnan(load[i]):
        flag = 1
    elif np.isnan(speed[i]):
        flag = 1
    elif np.isnan(throttle[i]):
        flag = 1
    if flag == 1:
        RPM = RPM[:i] + RPM[i+1:]
        load = load[:i] + load[i+1:]
        speed = speed[:i] + speed[i+1:]
        throttle = throttle[:i] + throttle[i+1:]
        len_data = len_data - 1
        i = i -1
    i = i + 1
    
print ("NaN data excluded. Now the length of dataset is:", len_data)

vsoverrpm = []
thoverrpm = []
fload = []
zerolist = []
for i in range(len_data):
    fload.append(load[i])
    if RPM[i] == 0 or speed[i] == 0:
        vsoverrpm.append(-1)
        thoverrpm.append(-1)
        zerolist.append(i)
        continue
    vsoverrpm.append(float(speed[i])/float(RPM[i]))
    thoverrpm.append(float(throttle[i])/float(RPM[i]))
    
zerolist.reverse()

for i in zerolist:
    del fload[i]
    

print ("The ratios calcualted")

def freqcounter(target):
    cnt = []
    for i in range(11):
        cnt.append(0)
    for i in range(len_data):
        if target[i] < 0:
            continue
        index = int(target[i]*100)
        cnt[index] = cnt[index] + 1
    print (cnt)
    
def freqcounter2(target):
    cnt = []
    for i in range(11):
        cnt.append(0)
    for i in range(1275):
        index = int(target[i]/10)
        cnt[index] = cnt[index] + 1
    print (cnt)

print ("Vehicle speed over RPM - freq")
freqcounter(vsoverrpm)

print ("Throttle over RPM - freq")
freqcounter(thoverrpm)

print ("Engine Load - freq")
freqcounter2(fload)

label = []
for i in range(len_data):
    if speed[i] == 0:
        label.append(0)
        continue
    if vsoverrpm[i] >= 0.05:
        label.append(-1)
    elif thoverrpm[i] >= 0.02:
        label.append(-1)
    elif load[i] >= 90:
        label.append(-1)
    else:
        label.append(1)
        
print ("Label made. The number of 1s and -1s are")
print (label.count(1), label.count(-1))

Label = pd.Series(label)
VoverRPM = pd.Series(vsoverrpm)
ToverRPM = pd.Series(thoverrpm)


classification = pd.DataFrame({'Vehicle Speed' : df["Vehicle.Speed"],
                         'Throttle Position': df["Throttle.Position"],
                         'Engine Load' : df["Engine.Load"],
                         'Vehicle speed over RPM' : VoverRPM,
                         'Throttle P. over RPM' : ToverRPM,
                         'Label' : Label})
                         
               
classification.to_csv('classification.csv', index = False)

print ("Saved")
