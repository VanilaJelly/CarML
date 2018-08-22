# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:58:50 2018

@author: Sumin Lee

learn classificated data using Soft Vector Machine learn and Deep learn
"""

import pandas as pd
import numpy.random as ran

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

#plt: 3D plot
#pl: 2D plot
import matplotlib.pyplot as plt

def accuracy(test_y, output_y, testcases):
    #count : number of right guesses
    count = 0

    for i in range(testcases):
        if output_y[i] == test_y[i]:
            count = count + 1
            acc = float(count/testcases)
    
    print ("The number of right guesses is", count, "among", testcases, "testcases.")
    print ("Accuracy is: ", acc)
    
    return acc
        

def plot_3D(test_X, output_y, testcases):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    for i in range(testcases):
        
        xs = test_X[i][0]
        ys = test_X[i][1]
        zs = test_X[i][2]
        if output_y[i] == -1:            
            c = 'r'
            m = '+'
        else:
            c = 'g'
            m = 'o'
        ax.scatter(xs, ys, zs, c=c, marker=m)
    plt.show()
        
        

    
        
def svmlearn(train_X, train_y, test_X, test_y, testcases, d):
    clf = svm.SVC(degree = d)
    clf.fit(train_X, train_y)
    
    output_y = clf.predict(test_X)

    print ("\n\n===SVM Learn===")
    plot_3D(test_X, output_y, testcases)
    return accuracy(test_y, output_y, testcases)
    
       
def deeplearn(train_X, train_y, test_X, test_y, testcases):
    clf = MLPClassifier()
    clf.fit(train_X, train_y)
    
    output_y = (clf.predict(test_X))
    
    print ("\n\n===Deep Learn===")
    plot_3D(test_X, output_y, testcases)
    return accuracy(test_y, output_y, testcases)
    
    
def logisticRegression(train_X, train_y, test_X, test_y, testcases):
    logR = LogisticRegression(C = 1.0)
    logR.fit(train_X, train_y)
    
    output_y = logR.predict(test_X)
    
    print ("\n\n===Logiscic Regression===")
    plot_3D(test_X, output_y, testcases)
    return accuracy(test_y, output_y, testcases)

    
    

df = pd.read_csv("classification.csv", sep = ",")
len_data = 2044

vsoverrpm = df["Vehicle speed over RPM"]
troverrpm = df["Throttle P. over RPM"]
load = df["Engine Load"]
label = df["Label"]



numlearn = 100

svmacc = 0
deepacc = 0
logacc = 0
for j in range(numlearn):
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

    svmacc = svmacc + svmlearn(train_X, train_y, test_X, test_y, testcases, 3)
    deepacc = deepacc + deeplearn(train_X, train_y, test_X, test_y, testcases)
    logacc = logacc + logisticRegression(train_X, train_y, test_X, test_y, testcases)

svmacc = svmacc/numlearn
deepacc = deepacc/numlearn
logacc = logacc / numlearn

print ("The average accuracy for SVM learning is: ", svmacc)
print ("The average accuracy for Deep learning is: ", deepacc)
print ("The average accuracy for Logistic learning is: ", logacc)