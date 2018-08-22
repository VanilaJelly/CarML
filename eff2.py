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
    plt.plot(data_X, data_y2, color='red', linewidth = 3)

    plt.xlabel('time')
    plt.xticks(())
    plt.yticks(())
    
    plt.show()



d1 = pd.read_csv("data1.csv", sep = ",")

fuel = np.array(d1["Fuel Level"])
dist = np.array(d1["Dist"])
speed = np.array(d1["Vehicle speed"])
time_sec_0 = np.array(d1["Time(sec)"])

test_X = []
test_y = []
train_X = []
train_y = []
time_sec = []
testcases = 0
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


deg = 1
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
   

print (len(predfuel))
   
predfuel = pd.Series(predfuel)



timedist = pd.DataFrame({'Time(sec)' : d1["Time(sec)"],
                         'Dist': d1["Dist"],
                         'Vehicle speed' : d1["Vehicle speed"],
                         'Fuel Level' : d1["Fuel Level"],
                         'Acc': d1["Acc"],
                         'Predicted Fuel level': predfuel})
                         

timedist.to_csv('data2.csv', index = False)