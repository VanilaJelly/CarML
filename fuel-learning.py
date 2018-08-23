# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 19:48:31 2018

@author: Sumin Lee

Trying to 
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import numpy.random as ran

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error


len_data = 2044

def plot_2D(data_X, data_y, data_y2, cases):

    plt.plot(data_X, data_y, color='blue', linewidth = 3)
    plt.scatter(data_X, data_y2, color='red')

    plt.xlabel('time')
    plt.xticks(())
    plt.yticks(())
    
    plt.show()


# Polynomial regression
def learn(time_sec_0, fuel, len_data, deg):
    
    if len_data < 10:
        return list(fuel)
    
    test_X = []
    test_y = []
    train_X = []
    train_y = []
    time_sec = []
    testcases = 0
    
    # Split train and testcases
    for i in range(len_data):
        rnum = ran.random()
        time_sec.append([time_sec_0[i]])
        if rnum > 0.75:
            test_X.append([time_sec_0[i]])
            test_y.append([fuel[i]])
            testcases = testcases + 1
        else:
            train_X.append([time_sec_0[i]])
            train_y.append([fuel[i]])
    
    
    poly = PolynomialFeatures(degree=deg)
    train_X = poly.fit_transform(train_X)
    train_Y = poly.fit_transform(train_y)
    test_X = poly.fit_transform(test_X)
    test_y = poly.fit_transform(test_y)
    time_sec_1 = poly.fit_transform(time_sec)
    
    ridg = linear_model.Ridge()
    ridg.fit(train_X, train_Y)
    pred_y = ridg.predict(test_X)
    
    print ("MSE : ", mean_squared_error(test_y, pred_y))
    
    pred1 = []
    for i in range(testcases):
       pred1.append(pred_y[i][deg])
    
    plt.scatter(test_X, test_y, color = 'black', linewidth = 1)
    plt.plot(test_X, pred_y, color='blue', linewidth = 3)
    
    plt.xlabel('time')
    plt.ylabel('fuel')
    
    
    plt.legend()
    
    plt.xticks(())
    plt.yticks(())
    
    plt.show()

    pred = ridg.predict(time_sec_1)
    
    predfuel = []
    for i in range(len_data):
       predfuel.append(pred[i][deg])
       
    
    return predfuel
    
    
d1 = pd.read_csv("data1.csv", sep = ",")

fuel = np.array(d1["Fuel Level"])
dist = np.array(d1["Dist"])
speed = np.array(d1["Vehicle speed"])
time_sec_0 = np.array(d1["Time(sec)"])



# Find out when the fuel is charged
partition = []
for i in range(0, len_data-2):
    fuel[i] = fuel[i]
    fueldiff = fuel[i+1] - fuel[i]
    
    if fueldiff > 20*0.35:
        partition.append(i+1)

print (partition)


# Find out stoplist
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
        if cnt > 10:
            if end == len_data:
                end = end - 1
            stoplist.append([start, end])

print ("car stops during", stoplist)



# Stablize the fuel level during car stops for (at least) a moment
for stop in stoplist:
    st = stop[0]
    en = stop[1]
    scale = int((en - st)/3)
    for i in range(st, en):
        fuel[i] = fuel[en-scale]




p1 = partition[0]
p2 = partition[1]
p3 = len_data
p = [0, p1, p2, p3]

# Check the partition each stoplist contained
stoplists = [[],[],[]]
for stop in stoplist:
    for i in range(3):
        if stop[0] > p[i] and stop[1] < p[i+1]:
            stoplists[i].append(stop)
            break

print (stoplists)


# Split, learn and merge
pred = []
for i in range(0, 3):
    po1 = p[i]
    po2 = p[i+1]
    print (i, "th charge: ", po1, po2)
    t2 = po1
    for stop in stoplists[i]:
        
        s1 = stop[0]
        s2 = stop[1]
        
        print ("t2, s1, s2: ", t2, s1, s2, "stop: ", stop)
        pred += learn(time_sec_0[t2:s1], fuel[t2:s1], s1-t2, 1)
        pred += list(fuel[s1:s2])
        
        t2 = s2
    pred = pred + learn(time_sec_0[t2:po2], fuel[t2:po2], po2-t2, 1)    
    print (t2, po2, "len: ", len(pred))
    
        
predfuel = list(pred)

plot_2D(time_sec_0, predfuel, fuel, len_data)

# Display the result
predfuel = pd.Series(predfuel)

timedist = pd.DataFrame({'Time(sec)' : d1["Time(sec)"],
                         'Dist': d1["Dist"],
                         'Vehicle speed' : d1["Vehicle speed"],
                         'Fuel Level' : d1["Fuel Level"],
                         'Acc': d1["Acc"],
                         'Predicted Fuel Level': predfuel})
                         

timedist.to_csv('data3.csv', index = False)
