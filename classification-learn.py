# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:58:50 2018

@author: Sumin Lee
"""

import pandas as pd
import numpy.random as ran

from sklearn import svm

import pylab as pl


df = pd.read_csv("classification.csv", sep = ",")
len_data = 2044

def svmlearn(train_X, train_y, test_X, test_y, testcases, d):
    clf = svm.SVC(degree = d)
    clf.fit(train_X, train_y)
    
    output_y = (clf.predict(test_X))
    
    for i in range(testcases):
        if output_y[i] == -1:
            c1 = pl.scatter(test_X[i][1], test_X[i][2], c='r', s=50, marker="+")
        else:
            c2 = pl.scatter(test_X[i][1], test_X[i][2], c='g', s=50 , marker="o")

    pl.show()
    
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
    if vsoverrpm[i] == -1:
        continue
    rnum = ran.random()
    if rnum > 0.5:
        test_X.append([vsoverrpm[i], troverrpm[i], load[i]])
        test_y.append(label[i])
        testcases = testcases + 1
    else:
        train_X.append([vsoverrpm[i], troverrpm[i], load[i]])
        train_y.append(label[i])
        
svmlearn(train_X, train_y, test_X, test_y, testcases, 3)
    