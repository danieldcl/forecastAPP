import pandas as pd
import numpy as np
import matplotlib.pylab as plt
%matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
#Now, we can load the data set and look at some initial rows and data types of the columns:
data = pd.read_csv('C:/Users/olivier/Desktop/AirPassenger.csv')
data.head()
data.dtypes
#The data contains a particular month and number of 
#passergers travelling in that month But is still not read as a Ts  object as the data types are object and int In order to read the data as a time series, we have to pass special arguments to the read_csv command:
dateparse = lambda dates: pd.datetime.strptime(dates,'%Y-%m')
data = pd.read_csv('C:/Users/olivier/Desktop/AirPassenger.csv', parse_dates='Month', index_col='Month',date_parser=dateparse)
def test_stationarity(timeseries):
     #Determining rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)
    
    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue', label='original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label= 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block = False)

        #Perform Dickey_Fuller test
    print('Result of Dickey-Fuller Test: ')
    dftest = adfuller(timeseries, autolag = 'AIC')
    dfoutput = pd.Series(dftest[0:4],index=['Test Statistic','p-value','#Lags Used','Number of Observation Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value(%s)' %key]=value
    return 

#How to make a Time Series Stationry
ts_log = np.log(ts)
moving_avg = pd.rolling_mean(ts_log,12)
ts_log_moving_avg_diff =ts_log - moving_avg
ts_log_moving_avg_diff.head(12)
ts_log_moving_avg_diff.dropna(inplace =True)
#exponentially weighted moving average
expwighted_avg = pd.ewma(ts_log, halflife=12)
ts_log_ewma_diff =ts_log - expwighted_avg
ts_log_diff =ts_log - ts_log.shift()
ts_log_diff.dropna(inplace = True)
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(ts_log)

seasonal = decomposition.seasonal
residual = decomposition.resid
plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
#ACF and PACF plots:
from statsmodels.tsa.stattools import acf, pacf
lag_acf = acf(ts_log_diff, nlags=20)
lag_pacf = pacf(ts_log_diff, nlags=20, method ='ols')
#plot ACF:
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')

#plot Pacf
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(ts_log,order =(2,1,0))
results_AR = model.fit(disp =-1)
plt.plot(ts_log_diff)
plt.plot(results_AR.fittedvalues,color='red')
plt.title('RSS: %.4f'% sum((results_AR.fittedvalues - ts_log_diff)**2))

#MA model
model = ARIMA(ts_log, order= (0,1,2))
results_MA = model.fit(disp = -1)
plt.plot(ts_log_diff)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('RSS: %.4f'%  sum((results_MA.fittedvalues -ts_log_diff)**2))
#Combined Model

model = ARIMA(ts_log, order=(2,1,2))
results_ARIMA =model.fit(disp=-1)
plt.plot(ts_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues - ts_log_diff)**2))
predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy= True)
print(predictions_ARIMA_diff.head())