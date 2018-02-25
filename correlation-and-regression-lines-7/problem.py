#!/usr/bin/env python

from scipy import stats
import numpy as np

phys_scores = [15,  12,  8,   8,   7,   7,   7,   6,   5,   3];
his_scores  = [10,  25,  17,  11,  13,  17,  20,  13,  9,   15];

slope, intercept, r_value, p_value, std_err = stats.linregress(phys_scores,his_scores)

print round(10*slope + intercept,3)
