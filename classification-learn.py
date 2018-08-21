# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:58:50 2018

@author: Sumin Lee

learn classificated data using Soft Vector Machine
"""

import pandas as pd
import numpy.random as ran

from sklearn import svm

#plt: 3D plot
#pl: 2D plot
import matplotlib.pyplot as plt
import pylab as pl

        
def svmlearn(train_X, train_y, test_X, test_y, testcases, d):
    clf = svm.SVC(degree = d)
    clf.fit(train_X, train_y)
    output_y = clf.predict(test_X)

    #number of correct guesses   
    count = 0

    #plot data
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    for i in range(testcases):
        if output_y[i] == test_y[i]:
            count = count + 1
        xs = test_X[i][0]
        ys = test_X[i][1]
        zs = test_X[i][2]
        if output_y[i] == -1:            
            c = 'r'
            m = '+'
        else:
            c = 'g'
            m = 'o'
        pl.scatter(test_X[i][1], test_X[i][2], c=c, s=50, marker=m)
        ax.scatter(xs, ys, zs, c=c, marker=m)
    pl.show()
    plt.show()
    
    print ("The number of right guesses is", count, "among", testcases, "testcases.")
    print ("Accuracy is: ", float(count)/(testcases))
    

df = pd.read_csv("classification.csv", sep = ",")
len_data = 2044

vsoverrpm = df["Vehicle speed over RPM"]
troverrpm = df["Throttle P. over RPM"]
load = df["Engine Load"]
label = df["Label"]

train_X = []
train_y = []
test_X = []
test_y= []
testcases = 0
for i in range(len_data):
    #if Vehicle Speed is 0, pass
    if vsoverrpm[i] == -1:
        continue
    rnum = ran.random()
    if rnum > 0.75:
        test_X.append([vsoverrpm[i], troverrpm[i], load[i]])
        test_y.append(label[i])
        testcases = testcases + 1
    else:
        train_X.append([vsoverrpm[i], troverrpm[i], load[i]])
        train_y.append(label[i])
        
svmlearn(train_X, train_y, test_X, test_y, testcases, 3)

