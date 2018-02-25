#! /usr/bin/env python

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn

import re

# Create a new dataframe in which to read four elements:
# date (month, day, year) and score
# Feed these into a multivariate regression (?) to estimate
# the score on a given day.

# Get initial number of lines.
m = raw_input();
print "Got "+m+" entries"

# Read each line in.
for x in range(int(m)) :
    line     = raw_input()
    line_arr = re.split(r'\t+', line)
    date     = re.split(r' ', line_arr[0])
    date_arr = re.split(r'/', date[0])
    score    = line_arr[1]
    if re.split(r'_',score)[0] == "Missing" :
        score = "NaN";
    var_arr  = [float(date_arr[0]),float(date_arr[1]),float(date_arr[2]),float(score)]
    print var_arr


    
# Open the text file and read into a dataframe.
# files   = ['input/input00.txt'];
# headers = ['date','score'];
# dtypes  = {'date' : 'str', 'score' : 'float'};
# parse_dates = [ 'date' ];
# for file in files :
#     stock_df=pd.read_csv(file,skiprows=[0],sep='\t',
#                              header=None,
#                              names=headers,
#                              dtype=dtypes,
#                              parse_dates=parse_dates);
#stock_df.columns = ['date','score'];
#print pd.to_datetime(stock_df.iloc[0,0]).date()
#stock_df['date'] =
#print stock_df

# Perform a linear regression.
