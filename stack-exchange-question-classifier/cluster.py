#!/usr/bin/env python

# Solution for HackerRank problem:
# https://www.hackerrank.com/challenges/stack-exchange-question-classifier/problem
# David Di Valentino, 2018

import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time

from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.utils.extmath import density
from sklearn import metrics

from pprint import pprint
import pandas as pd
import json

# For splitting data into training / testing samples.
from sklearn.model_selection import train_test_split

################################################################################
def read_from_file(filename) :
    f = open(filename);
    #Read number of records.
    nrecords = int(f.readline());
    # Read in all the json objects into a pandas dataframe.
    data = pd.DataFrame(json.loads(line, encoding='utf-8') for line in f)
    return data

def read_from_input() :
    file = open("testcase.json","w") 
    nrecords = int(raw_input());
    file.write("%i \n" % (nrecords))
    for x in range(nrecords) :
        test = raw_input()
        file.write(test+'\n')
    file.close()
    return read_from_file("testcase.json")

# Reading JSON directly from terminal to a DF is SUPER SLOW, for whatever reason.
# It's literally faster to just dump terminal input to file, then read it
# back in using python's json encoder.
#data     = pd.read_json(raw_input(),typ='series').to_frame().transpose();
#for x in range(nrecords-1) :
#    line = raw_input()
#    ldat = pd.read_json(raw_input(),typ='series').to_frame().transpose();
#    data = data.append(ldat)
#    print ldat
#return data;
################################################################################

doTesting = False

# Get training and testing data.
data      = read_from_file("training.json");

# Test case data.
test_case_data = read_from_input();

################################################################################
#Encode the categories numerically.
################################################################################

le = preprocessing.LabelEncoder();
le.fit(data['topic']);
#y_train = le.transform(data['topic']);
#pprint(list(y_train))

# Split into training and testing samples.
train_data = data;
if doTesting :
    train_data, test_data = train_test_split(data, test_size=0.5);
    y_test  = le.transform(test_data ['topic']);
y_train = le.transform(train_data['topic']);
# Create a new element in the DF composed of the merged question
# and excerpt.
def merge_question_excerpt(df) :
    df['question'] = df['question'].map(lambda x: x.encode('unicode-escape').decode('utf-8'));
    df['excerpt']  = df['excerpt'].map(lambda x: x.encode('unicode-escape').decode('utf-8'));
    df['merged']   = df['question'].map(str) + " " + df['excerpt'].map(str);
    return df;

# We can get a better fit by concatenating the question and excerpt.
# We don't care about syntax here, just the correlation of a given set of
# words to the topic.
train_data     = merge_question_excerpt(train_data);
test_case_data = merge_question_excerpt(test_case_data);
if doTesting :
    test_data      = merge_question_excerpt(test_data);

################################################################################
#Vectorize the input data using term frequency-inverse document frequency.
################################################################################

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')

X_train    = vectorizer.fit_transform(train_data['merged'])
X_testcase = vectorizer.transform(test_case_data['merged'])
if doTesting :
    X_test     = vectorizer.transform(test_data['merged'])

def benchmark(clf):
    #Run the training.
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)
    #Apply to the test sample.
    pred = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)
    
    #pred_cats = le.inverse_transform(pred);
    #for cat in pred_cats :
    #   print cat;

if doTesting :
    benchmark(MultinomialNB(alpha=.2));
    benchmark(SGDClassifier(alpha=.00002, n_iter=50, penalty="l2"));
else :
    mnb_fitter = SGDClassifier(alpha=.00002, n_iter=50, penalty="l2");
    mnb_fitter.fit(X_train,y_train)

    # Apply to the test case.
    pred_testcase = mnb_fitter.predict(X_testcase);
    pred_testcase_cat = le.inverse_transform(pred_testcase);
    for cat in pred_testcase_cat :
        print cat;

# *** Next step would be hyperparameter tuning of alpha, or trying use of
# SGDClassifier in place of multinomial NB
