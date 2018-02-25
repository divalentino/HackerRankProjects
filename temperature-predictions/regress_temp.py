#!/usr/bin/env python

# Try a multivariate regression to see if that provides any more
# sensitivity based on year and date.

import pandas as pd
from pandas import read_csv
from sklearn.preprocessing import Imputer
from sklearn import datasets, linear_model
import numpy as np
from scipy import interpolate

# Make a hash table for months to treat them numerically.
keys = ['January','February','March','April','May', 'June','July','August',
        'September','October','November','December'];
values = [1,2,3,4,5,6,7,8,9,10,11,12];
hash   = {k:v for k, v in zip(keys, values)}

################################################################################
# Read in data.
################################################################################

#Get # points and skip header.
npoints = int(raw_input());
raw_input();

tmax  = []
tmin  = []
data  = []
days  = []

days_missing = []
tmin_missing = []
tmax_missing = []

features_tmax = []
features_tmin = []

nmissing=0
day=0
for i in range(npoints) :
    #Get the measurement.
    line  = raw_input().split()
    year  = float(line[0]);
    month = float(hash[line[1]]);
    # Get # of missing entries for later.
    if 'Missing' in line[2] :
        nmissing += 1;
    if 'Missing' in line[3] :
        nmissing += 1;
    #Increment the date index.

    # Get tmin and tmax, and fill with nan as necessary.
    my_tmax = np.NaN if 'Missing' in line[2] else float(line[2])
    my_tmin = np.NaN if 'Missing' in line[3] else float(line[3])

    # Only want to keep measurements with tmin and tmax for
    # fitting. Then we can fill in the gaps later.
    if 'Missing' in line[2] or 'Missing' in line[3] :
        tmax_missing.append(my_tmax);
        tmin_missing.append(my_tmin);
        days_missing.append([year,month]);
    else :
        tmax.append(my_tmax);
        tmin.append(my_tmin);
        days.append([year,month]);
        features_tmax.append([year,month,my_tmin]);
        features_tmin.append([year,month,my_tmax]);

################################################################################
# Try a multivariate regression which takes into account year, date, and
# min (max) temperature as features to figure out the target max (min) temp.
################################################################################

# Find that gradient boosting eeks out a few more % accuracy.
from sklearn.ensemble import GradientBoostingRegressor
reg_tmin = GradientBoostingRegressor(loss='ls', learning_rate=0.05, n_estimators=120, max_depth=3)
reg_tmax = GradientBoostingRegressor(loss='ls', learning_rate=0.075, n_estimators=100, max_depth=4)

# Create the linear models.
#reg_tmax = linear_model.Lasso(alpha = 0.25);
reg_tmax.fit (features_tmax, tmax);

#reg_tmin = linear_model.Lasso(alpha = 0.25);
reg_tmin.fit (features_tmin, tmin);

for i in range(len(days_missing)) :
   if (np.isnan(tmax_missing[i])) :
       print round(reg_tmax.predict([[days_missing[i][0],days_missing[i][1],tmin_missing[i]]])[0],2);
   elif (np.isnan(tmin_missing[i])) :
       print round(reg_tmin.predict([[days_missing[i][0],days_missing[i][1],tmax_missing[i]]])[0],2);
