#!/usr/bin/env python

import re
import numpy as np

def pearson(x, y) :
    pearson = 0;
    n = len(x);

    # Some handy sums to keep around
    # to make calculation easier.
    sumx  = 0;
    sumy  = 0;
    sumx2 = 0;
    sumy2 = 0;
    sumxy = 0;

    for i in range(n) :
        sumx  += x[i]
        sumy  += y[i]
        sumx2 += pow(x[i],2)
        sumy2 += pow(y[i],2)
        sumxy += x[i]*y[i]

    # Compute the correlation coefficient.
    pearson = (n*sumxy - sumx*sumy) / np.sqrt(n*sumx2 - pow(sumx,2)) / np.sqrt(n*sumy2 - pow(sumy,2));
        
    return pearson;

################################################################################

math = []
phys = []
chem = []

# Get initial number of lines.
m = raw_input();
#print "Got "+m+" entries"

# Read each line in.
for x in range(int(m)) :
    line     = raw_input()
    line_arr = re.split(r'  ', line)

    math.append(float(line_arr[0]))
    phys.append(float(line_arr[1]))
    chem.append(float(line_arr[2]))

# Compute the pearson coefficient for math - phys.
print round(pearson(math,phys),2);

# Compute the pearson coefficient for phys - chem.
print round(pearson(phys,chem),2);

# Compute the pearson coefficient for chem - math.
print round(pearson(chem,math),2);
