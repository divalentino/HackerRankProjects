#!/bin/bash

#cat test.txt | ./temperature.py
#cat temperature-predictions-testcases/input/input00.txt | ./temperature.py

cat temperature-predictions-testcases/input/input00.txt | ./regress_temp.py
