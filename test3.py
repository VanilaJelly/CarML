# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 10:30:42 2018

@author: 이수민
"""

import numpy as np
import pandas as pd

d1 = pd.read_csv("data1.csv", sep = ",")

fuel = d1["Fuel Level"]
dist = d1["Dist"]

fuel_1 = []

eff = []

#dlen = 12269
dlen = 2044


for i in range(2, dlen-2):
    fuel0 = float(fuel[i-2][:-1])
    fuel1 = float(fuel[i-1][:-1])
    fuel2 = float(fuel[i][:-1])
    
    fuel_1.append((fuel0+fuel1+fuel2)/3)
