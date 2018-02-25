#!/usr/bin/env python

# Check out here: https://machinelearningmastery.com/handle-missing-data-python/
# for imputation in Python + scikit

import pandas as pd
from pandas import read_csv
from sklearn.preprocessing import Imputer
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

    day += 1;
    
    # Only want to keep measurements with tmin and tmax for
    # fitting. Then we can fill in the gaps later.
    if 'Missing' in line[2] or 'Missing' in line[3] :
        tmax_missing.append(my_tmax)
        tmin_missing.append(my_tmin)
        days_missing.append(day)
    else :
        tmax.append(my_tmax)
        tmin.append(my_tmin)
        days.append(day);

#print "# of missing points: %i " % (nmissing)
   
################################################################################
# Try simple polynomial interpolation instead. We know a priori that temperature
# tends to vary "smoothly" over time, so a high-enough degree polynomial should
# be able to capture this effect.
################################################################################

model_tmin = interpolate.interp1d(days,tmin,kind='cubic',fill_value='extrapolate');
model_tmax = interpolate.interp1d(days,tmax,kind='cubic',fill_value='extrapolate');

# Print out estimates for the missing dates.
for i in range(len(days_missing)) :
   if (np.isnan(tmax_missing[i])) :
       print(round(model_tmax(days_missing[i]),2));
   elif (np.isnan(tmin_missing[i])) :
       print(round(model_tmin(days_missing[i]),2));
