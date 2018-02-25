#!/usr/bin/env python

# Solution for HackerRank problem:
# https://www.hackerrank.com/challenges/predicting-house-prices/problem
# David Di Valentino, 2018

import numpy as np
import sys

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from pprint import pprint
import pandas as pd

################################################################################
# Read input
################################################################################

# Get initial # of features and entries.
nfeat, nentries = raw_input().split()
nfeat    = int(nfeat)
nentries = int(nentries)

# nfeat features first, then price is at the end.
features = []
prices   = []
for i in range(nentries) :
    feature = []
    line = raw_input().split();
    for j in range(nfeat) :
        feature.append(float(line[j]))
    features.append(feature)
    prices.append(float(line[nfeat]))

#print features
#print prices

# Now read in the testing values.
test_features = []
ntest = int(raw_input())
for i in range(ntest) :
    line = raw_input().split();
    feature = []
    for j in range(nfeat) :
        feature.append(float(line[j]))
    test_features.append(feature)

#print test_features
    
# Create the linear model.
reg = linear_model.LinearRegression();
reg.fit (features, prices);
#print reg.coef_

test_prices = reg.predict(test_features)
for test_price in test_prices :
    print round(test_price,2)
