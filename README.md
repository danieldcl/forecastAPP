Kaggle Data Forecast Team

Group Members:
	
  Ding Chao Liao
  
  Dramane Diakite
  
  Moustafa Elshaabiny
  
  Olivier Dounla

Overview of the application:

	This program was intended to forecast store sales for Rossmann Drug Stores. We generalized the program so that the program could be used for other data sets.

	Our program works best for numerical data analysis. Predicting string data will produce numerical outputs.
	Each predicting model works differently and fits different types of data.
	XGBoost: This model trains the data 1000 times. Produces most accurate results in the available list of models, moderate run time.
	RandomForest: By default the maximum tree depth is set to 5 to reduce runtime and 1000 estimator, less accurate and long run time, RAM consuming.
	DecisionTree: max tree depth is set to 10, moderate speed and accuracy.
	LinearRegression: fast, best for linear data.


To use:

	1. import a data set, the application currently takes small data sets, if the data set is big/large, consider the amount of RAM in your computer.
	2. select dependent attribute (what you are predicting) and independent attributes (other than what you are predicting).
	3. pick a predicting model and specify the number of predictions.
	4. run prediction and see the results.


Required Machine Learning Python Libraries:

	scikit-learn
	pandas
	numpy
	matplotlib
	xgboost

 * xgboost installation differs in different machines, refer to the following link for instructions. https://www.kaggle.com/c/liberty-mutual-group-property-inspection-prediction/forums/t/15742/clear-instructions-to-install-xgboost-in-python

Required Graphical Library:

	Tkinter
	ttk
