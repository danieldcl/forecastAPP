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
    # data = df[xvars]
    data = data.dropna(axis=1, how='all')
    cols = data.columns
    for i in cols:
        if data[i].dtypes == 'object':
            data[i] = data[i].astype('category').cat.codes

        if data[i].isnull().any().any():
            data[i].fillna(data[i].mean(), inplace=True)

    return data


def Generate_Prediction(model, filename, xvars, yvar, num):
    xvars = ast.literal_eval(xvars)
    #the system generate the prediction result
    if yvar not in xvars:
        xvars.append(yvar)

    df = Clean_Data(filename, xvars)
    cols = list(df.columns)
    cols.remove(yvar)
    xdata = df[cols]
    ydata = df[yvar]

    model= model.lower()
    if model== 'xgboost':
        return xgboost_model(xdata, ydata, num)

    elif model== 'randomforest':
        m = RandomForestClassifier(n_estimators=10)
        return Selected_Model(m, xdata, ydata, num)

    elif model== 'decisiontree':
        m = DecisionTreeClassifier()
        return Selected_Model(m, xdata, ydata, num)

    elif model== 'linearregression':
        m = LinearRegression()
        return Selected_Model(m, xdata, ydata, num)


def Selected_Model(model, xdata, ydata, num):
    #Generic function for making a classification model and accessing performance:
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(
        xdata, ydata, test_size=0.2, random_state=10)

    #Fit the model:
    predicting_model = model.fit(x_train,y_train)

    #Make predictions on training set:
    predictions = predicting_model.predict(x_test[-num:])

    return predictions

    # return metrics.classification_report(y_test, predictions)
    # accuracy = metrics.accuracy_score(y_test, predictions)
    # return accuracy



def ToWeight(y):
    w = np.zeros(y.shape, dtype=float)
    ind = y != 0
    w[ind] = 1./(y[ind]**2)
    return w
def rmspe(yhat, y):
    w = ToWeight(y)
    rmspe = np.sqrt(np.mean( w * (y - yhat)**2 ))
    return rmspe
def rmspe_xg(yhat, y):
    # y = y.values
    y = y.get_label()
    y = np.exp(y) - 1
    yhat = np.exp(yhat) - 1
    w = ToWeight(y)
    rmspe = np.sqrt(np.mean(w * (y - yhat)**2))
    return "rmspe", rmspe

def xgboost_model(xdata, ydata, num):
    #the system generate the prediction result

    #our system splits the data, and almost  one third are submit to the system as training data.
    x_train, x_test, y_train, y_test = train_test_split(xdata, ydata,
                                                    test_size=0.2, random_state=10)

    data = np.random.rand(5,10) # 5 entities, each contains 10 features
    label = np.random.randint(2, size=5) # binary target
    dtrain = xgb.DMatrix( data, label=label)


    dtrain = xgb.DMatrix(x_train, y_train)
    dtest = xgb.DMatrix(x_test, y_test)

    num_round = 500
    evallist = [(dtrain, 'train'), (dtest, 'test')]

    param = {'bst:max_depth':12,
         'bst:eta':0.0095,
         'subsample':0.8,
         'colsample_bytree':0.7,
         'silent':1,
         'objective':'reg:linear',
         'nthread':6,
         'seed':42}
    plst = param.items()
    bst1 = xgb.train(plst, dtrain, num_round, evallist, verbose_eval=50, early_stopping_rounds=200)
    xgb_x_test = xgb.DMatrix(x_test)
    predictions = bst1.predict(xgb_x_test[-num:])
    return predictions

if __name__=='__main__':
    filename = 'citibike.csv'
    fcolumns = ['the_geom','tripduration', 'starttime', 'stoptime']
    print Generate_Prediction('LinearRegression', filename, str(fcolumns), 'tripduration', num=10)
