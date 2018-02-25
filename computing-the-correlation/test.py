#!/usr/bin/env python

import numpy as np

phys=[15,  12,  8,   8,   7,   7,   7,   6,   5,   3];
hist=[10,  25,  17,  11,  13,  17,  20,  13,  9,   15];

print round(np.corrcoef(phys,hist)[0][1],3)
