Kaggle Data Forecast Team

Group Members:
	Ding Chao Liao
  Dramane Diakite
  Moustafa Elshaabiny
  Olivier Dounla

Overview of the application:

	Our program works best for numerical data analysis.
	Each predicting model works differently.
	XGBoost: accurate, moderate to long.
	DecisionTree: moderate.
	RandomForest: 10 trees, slow, requires RAM.
	LinearRegression: fast, best for linear data.


To use:

	1. import a data set, the application currently only takes small data sets, if the data set is large, consider the amount of RAM in your computer.

	2. select dependent attribute and independent attributes.
	3. pick a predicting model and specify the number of predictions.
	4. run prediction and see the results.


Required Machine Learning Python Libraries:

	scikit-learn
	pandas
	numpy
	matplotlib
	xgboost

Required Graphical Library:

	Tkinter
	ttk
