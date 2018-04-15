"""Used to create dataset of a particular company which is listed in S&P 500. The data is extracted from data_stocks.csv and stored in a csv file"""
# Import
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Import data
data = pd.read_csv('data_stocks.csv')

#data = data[:,0:1]

# Drop date variable
data = data.drop(data.columns[14:], axis = 1)
data = data.drop(data.columns[2:13], axis = 1)
data = data.drop(data.columns[1], axis = 1)
print data.head(10)
n = data.shape[0]

#Creating a new data frame
stock_df = data.copy(deep = True)
stock_df = stock_df.drop(stock_df.columns[1], axis = 1)

#Adding new columns
stock_df["t+6"] = ""
stock_df["t+1"] = ""
stock_df["t+2"] = ""
stock_df["t+3"] = ""
stock_df["t+4"] = ""
stock_df["t+5"] = ""
print stock_df


k = 0
i = 1
while(k < n - 10):
	stock_df.iloc[k, 2] =  data.iloc[k, 1]
	stock_df.iloc[k, 3] =  data.iloc[k+1, 1]
	stock_df.iloc[k, 4] =  data.iloc[k+2, 1]
	stock_df.iloc[k, 5] =  data.iloc[k+3, 1]
	stock_df.iloc[k, 6] =  data.iloc[k+4, 1]
	stock_df.iloc[k, 1] =  data.iloc[k+5, 1]
	k= k + 1
	if(k %2000 == 0):
		print("Iteration - "+ str(i*2000))
		i = i + 1
#Remove last row which don't have any entries
stock_df = stock_df[:-2]
print stock_df
stock_df.to_csv("AMAZON.csv", encoding='utf-8', index=False)
