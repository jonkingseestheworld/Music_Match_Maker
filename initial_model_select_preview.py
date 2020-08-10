#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Created on Mon 10Aug 2020

@author: JKLau
"""

# Import required libraries
import os
import pandas as pd
import numpy as np
#from scipy import stats

from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score

from sklearn.pipeline import Pipeline

# models
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC, SVC, NuSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier

from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import f1_score, confusion_matrix, precision_score, recall_score


DATAPATH = ""

# Read in personal Streaming History data
SH0_df = pd.read_csv(os.path.join(DATAPATH, "partner0_StreamingHist.csv")) #data from partner0 that will be used for building/training the ML models
#SH1_df = pd.read_csv(os.path.join(DATAPATH, "partner1_StreamingHist.csv")) #data from partner1 that will be used in final predictions

# Read in Song Attributes data
df_attr = pd.read_csv(os.path.join(DATAPATH, "song_attributes.csv"))

# Some data cleaning 
# remove some special characters ([,],',") in the 'artists' column in the 'song attributes' dataset
df_attr['artists'] = df_attr['artists'].replace({r'\[|\]|\'|\"':''}, regex=True)
df_attr = df_attr.rename(columns={'name':'track'})
SH0_df = SH0_df.rename(columns={'artistName':'artists', 'trackName':'track'}).drop('Unnamed: 0', axis=1)


# Shortlist only songs from SH0_df that also have 'song attributes' information
sl_df0 = pd.merge(SH0_df, df_attr[['track', 'artists']], how='inner', on=['track', 'artists'])
# Count the number of occurences of each song in the shortlisted data
df0_freq = sl_df0.groupby(['track', 'artists'])['track'].count().to_frame('count').reset_index()

# Save songs with 5 or more listens as 1 ('favourite')
df0_freq['favourite'] = np.where(df0_freq['count'] >= 5, 1, 0)
df0_freq = df0_freq.drop('count', axis=1)

# merging 'favourite' column into the 'song attributes' datafile (this returns only songs that parter0 had listened to in the previous year)
df0 = pd.merge(df0_freq, df_attr, how='inner', on=['track', 'artists'])
#drop columns that will not be used in training the models
df0.drop(columns = ['id', 'key', 'mode', 'release_date', "explicit", "year"], inplace=True)


# Split Data into Train sets and Test sets
X_train, X_test, y_train, y_test = train_test_split(df0.drop(columns=["track", "artists", "favourite"]), df0["favourite"], test_size=.25)

# Balancing Classes with SMOTE
X_trainS,y_trainS = SMOTE().fit_resample(X_train,y_train)

# Re-scale Features to reduce potential biases towards certain features during learning 
# to prevent data leakage into Test set, transformation (rescaling) is first learnt and done with Train set before applying it onto the Test set
mmscaler = MinMaxScaler()



# Prediction time!
linear_models = []

linear_models.append(("LogisticRegression",LogisticRegression()))

kernel_models = []

kernel_models.append(("Linear Support Vector Classifier", LinearSVC()))
kernel_models.append(("Support Vector Classifier", SVC(kernel="rbf", probability=True)))
kernel_models.append(("Nu Support Vector Classifer", NuSVC(probability=True)))

neighbor_models = [("K-nearest neighbours Ball", KNeighborsClassifier(algorithm='ball_tree'))]

gaussian_models = [("Gaussian Process", GaussianProcessClassifier())]
deTree_models = [("Decision Tree", DecisionTreeClassifier())]


ensemble_models = []

ensemble_models.append(("Random forest", RandomForestClassifier()))
ensemble_models.append(("AdaBoost", AdaBoostClassifier()))
ensemble_models.append(("GradientBoosting", GradientBoostingClassifier()))

mlpNetwork_models = [("MLP NNetwork", MLPClassifier())]


model_families = [("Linear Models",linear_models), ("Kernel Methods", kernel_models), 
                  ("Neighbour", neighbor_models), ("Gaussian Methods",gaussian_models), 
                  ("Decision Tree", deTree_models), ("Ensemble methods",ensemble_models),
                  ("mlpNetwork", mlpNetwork_models)]




# save outputs in .txt file
outputs = open('init_outputs.txt', 'w')


for family_name, models in model_families:
    print('******{}******'.format(family_name))
    outputs.write('******{}******'.format(family_name)+ "\n")
    
    for name, model in models:
        print("---{}---".format(name))
        outputs.write("---{}---".format(name)+ "\n")

        print(model)
        
        print(model.get_params())
        outputs.write(str(model.get_params())+ "\n")
       
        clf = Pipeline(steps=[('mmscaler', mmscaler), ('classifier', model)])
        
        clf_scores = cross_val_score(clf, X_trainS, y_trainS, scoring = "f1", n_jobs=-1, 
                                        verbose=2)
        
        print(clf_scores)
        outputs.write(str(clf_scores)+ "\n")

        print(np.mean(clf_scores))
        outputs.write(str(np.mean(clf_scores))+ "\n")

        clf.fit(X_trainS, y_trainS)
        y_pred = clf.predict(X_test)

        print("f1_score_test: {}".format(f1_score(y_test, y_pred)), "\n")
        outputs.write("f1_score_test: {}".format(str(f1_score(y_test, y_pred))) + "\n\n")

        
outputs.close()