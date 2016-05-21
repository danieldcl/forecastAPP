"""
Functions were written by Dramane and Olivier
Edited by Ding Chao Liao
"""

import numpy as np
import pandas as pd
import xgboost as xgb
import csv
import random
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import cross_validation
from sklearn.cross_validation import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
import ast


def Clean_Data(filename, vars):
    # remove redundancy, normalize, and preprocess the data
    # Convert Categorical values into numerical values
    na_values = ['NO CLUE', 'N/A', '']
    df = pd.read_csv(filename, na_values=na_values, parse_dates=True)
    data = df[vars]
    data = data.dropna(axis=1, how='all')
    cols = data.columns
    for i in cols:
        if data[i].dtypes == 'object':
            data[i] = data[i].astype('category').cat.codes

        if data[i].isnull().any().any():
            data[i].fillna(data[i].mean(), inplace=True)

    return data


def Generate_Prediction(model, filename, xvars, yvar, num):
    # This function calls the predicting models to generate predictions

    # convert xvars from string to list
    xvars = ast.literal_eval(xvars)
    if yvar not in xvars:
        xvars.append(yvar)

    # clean the data, filtering the columns that are selected by the user
    df = Clean_Data(filename, xvars)
    try:
        cols = list(df.columns)
        cols.remove(yvar)
        xdata = df[cols]
        ydata = df[yvar]
        model= model.lower()

        # run predicting model accordingly
        if model== 'xgboost':
            return xgboost_model(xdata, ydata, num)

        elif model== 'randomforest':
            # RandomForestClassifier can take a lot of RAM base on the max_depth and the number of attributes selected in the data
            m = RandomForestClassifier(n_estimators=1000, max_depth=5, n_jobs=-1)
            return Selected_Model(m, xdata, ydata, num)

        elif model== 'decisiontree':
            m = DecisionTreeClassifier(splitter='random', max_depth=10)
            return Selected_Model(m, xdata, ydata, num)

        elif model== 'linearregression':
            m = LinearRegression()
            return Selected_Model(m, xdata, ydata, num)
    except TypeError:
        return -1


def Selected_Model(model, xdata, ydata, num):
    #Generic function for making a classification model and accessing performance

    # split the dataset into training and testing subsets, test size = 0.2 with random state 50.
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(
        xdata, ydata, test_size=0.2, random_state=50)

    #train the model:
    predicting_model = model.fit(x_train,y_train)

    #Make predictions on test set, using n from user input:
    predictions = predicting_model.predict(x_test[-num:])

    # return predictions and the real values a tuple
    return (predictions.tolist(), y_test[-num:].values.tolist())

    # return metrics.classification_report(y_test, predictions)
    # accuracy = metrics.accuracy_score(y_test, predictions)
    # return accuracy





def xgboost_model(xdata, ydata, num):
    # the function uses xgboost to generate the predictions

    # splits the data, and almost  one third are submit to the system as training data.
    x_train, x_test, y_train, y_test = train_test_split(xdata, ydata,
                                                    test_size=0.2, random_state=30)

    data = np.random.rand(5,10) # 5 entities, each contains 10 features
    label = np.random.randint(2, size=5) # binary target

    # xgboost requires the data in matrix format
    dtrain = xgb.DMatrix( data, label=label)
    dtrain = xgb.DMatrix(x_train, y_train)
    dtest = xgb.DMatrix(x_test, y_test)

    # train the data for 1000 rounds to increase accuracy. the more rounds to train the more accurate
    num_round = 1000
    evallist = [(dtrain, 'train'), (dtest, 'test')]

    # list of parameters that xgboost model takes, objective is chose to be linear
    param = {'bst:max_depth':12,
         'bst:eta':0.0095,
         'subsample':0.8,
         'colsample_bytree':0.7,
         'silent':1,
         'objective':'reg:linear',
         'nthread':6,
         'seed':42}
    plst = param.items()

    # train the model
    bst1 = xgb.train(plst, dtrain, num_round, evallist, verbose_eval=50, early_stopping_rounds=200)

    # convert test data into matrix
    xgb_x_test = xgb.DMatrix(x_test[-num:])

    # make predictions
    predictions = bst1.predict(xgb_x_test)
    return (predictions.tolist(), y_test[-num:].values.tolist())

# This is for testing purposes
# if __name__=='__main__':
#     filename = 'citibike.csv'
#     fcolumns = ['the_geom','tripduration', 'starttime', 'stoptime']
#     print Generate_Prediction('LinearRegression', filename, str(fcolumns), 'tripduration', num=10)
