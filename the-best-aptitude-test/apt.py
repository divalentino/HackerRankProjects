#!/usr/bin/env python

from pearson import pearson
import re
import numpy as np
import sys

# Get # of cases.
ns = int(raw_input());

for itest in range(ns) :

    # Get # of tests.
    nt = int(raw_input());

    # Get GPA scores.
    gpas = [];
    line_arr = re.split(r' ', raw_input());
    for line in line_arr :
        gpas.append(float(line));

    #print gpas
        
    # Read each line in.
    scores = []
    #for x in range(nt) :
    for x in range(0,5) :
        test     = []
        line     = raw_input()
        line_arr = re.split(r' ', line)
        for line in line_arr :
            test.append(float(line))
        scores.append(test)

    # For each set of test scores, determine the correlation
    # to the GPA scores.
    best       = 0;
    best_index = 0;
    it         = 0;
    for test in scores :
        it = it+1;
        coeff = pearson(gpas,test);
        #print "Predictor: %i , correlation coefficient: %5.3f" % (it,coeff)    
        if (coeff>best) :
            best       = coeff;
            best_index = it;

    print best_index
