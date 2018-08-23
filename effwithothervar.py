# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 23:50:53 2018

@author: Sumin Lee
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

def plot_2D(data_X, data_y, data_y2, cases, label1, label2):

    plt.plot(data_X, data_y, color='blue', linewidth = 3, label = label1)
    plt.plot(data_X, data_y2, color='red', linewidth = 3, label = label2)
    
    plt.xlabel('time')
    plt.xticks(())
    plt.yticks(())
    
    plt.legend()
    plt.show()


len_data = 2055
df = pd.read_csv("data2.csv", sep = ",")
d0 = pd.read_csv("re_data.csv", sep = ",")

eff = list(df["Instant Fuel Efficiency"])
time = list(df["Time(sec)"])

Variables = [[list(d0["Engine.Load"]), "Engine.Load"],
            [list(d0["Vehicle.Speed"]), "Vehicle.Speed"],
            [list(d0["Throttle.Position"]), "Throttle.Position"],
            [list(d0["Air.Intake.Temperature"]), "Air Intake Temperature"],
            [list(d0["Air.Fuel.Ratio"]),  "Air Fuel Ratio"],
            [list(d0["Engine.Coolant.Temperature"]), "Engine Coolant Temp"],
            [list(d0["Engine.RPM"]), "Engine RPM"],
            [list(d0["Intake.Manifold.Pressure"]), "Intake Manifold Pressure"]]

i = -1
nanlist = []
while i < len_data-1:
    i = i + 1
    for var in Variables:
        if np.isnan(var[0][i]):
            nanlist.append(i)
            break

nanlist.reverse()
for i in nanlist:
    for j in range(len(Variables)):
        Variables[j][0] = Variables[j][0][:i] + Variables[j][0][i+1:]

len_data = len(Variables[0][0])

for i in range(len_data):
    eff[i] = eff[i]/30    
    
for var in Variables:
    plot_2D(time, eff, var[0], len_data, "Fuel Efficicncy", var[1])