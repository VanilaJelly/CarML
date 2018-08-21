# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 22:28:11 2018

@author: Sumin Lee

Tried to find out polynomial formula for f(x),
where speed = f(time)
"""

import numpy as np
import pandas as pd

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

import matplotlib.pyplot as plt




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




df = pd.read_csv("d1-r-data.csv", sep = ",")
df_array = df.as_matrix()

time_split = []
time_in_sec = []

len_data = 3000
len_train = 2000
len_test = 1000


for i in range(0, len_data):
    time = df["time_slot"][i]
    time1 = df["time_slot"][i+1]
    time_split.append([])
    time_split[i].append(int(time[:4]) - 2018)  #year
    time_split[i].append(int(time[5:7]))        #month
    time_split[i].append(int(time[8:10]))       #day
    time_split[i].append(int(time[11:13]))      #hour
    time_split[i].append(int(time[14:16]))      #min
    time_split[i].append(float(time[17:-1]))    #sec


t0 = conv_to_sec(time_split[0])
for i in range(0, len_data):
    t1 = conv_to_sec(time_split[i])
    
    time_in_sec.append(t1-t0)


orig_x = np.linspace(0, time_in_sec[len_data-1], 100000)
sample_x = []
for i in range(10000):
    sample_x.append([orig_x[i]])

#change shape of datas
timespeed_X = []
timespeed_Y = []
for i in range(1, len_data):
    timespeed_X.append([time_in_sec[i]])
    timespeed_Y.append([df["Vehicle Speed"][i]])
    


timespeed_X_train = timespeed_X

timespeed_Y_train = timespeed_Y

deg = 10
poly = PolynomialFeatures(degree=deg)
train_X = poly.fit_transform(timespeed_X_train)
train_Y = poly.fit_transform(timespeed_Y_train)
sample_X = poly.fit_transform(sample_x)

ridg = linear_model.Ridge()
    
ridg.fit(train_X, train_Y)

'''
timespeed_Y_pred = ridg.predict(test_X)

pred = []
for i in range(len_test-1):
   pred.append(timespeed_Y_pred[i][deg])

print(test_X.shape)

print ("MSE : ", mean_squared_error(timespeed_Y_test, pred))
'''
timespeed_Y_pred = ridg.predict(sample_X)

pred1 = []
for i in range(10000):
   pred1.append(timespeed_Y_pred[i][deg])

plt.scatter(timespeed_X_train, timespeed_Y_train, color = 'black', linewidth = 1)
plt.plot(sample_x, pred1, color='blue', linewidth = 3)

plt.xlabel('time')
plt.ylabel('speed')

plt.xlim([0, time_in_sec[len_data-1]])

plt.legend()

plt.xticks(())
plt.yticks(())

plt.show()