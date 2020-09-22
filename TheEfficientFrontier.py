# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:12:08 2018

@author: peirmah
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = r'Z:\Devin Project\Data\Data.xlsx'

row_data = pd.read_excel(file_path)

price_data = row_data.drop(['Date'], axis=1)

# return calculation
returns = price_data.pct_change()
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()

#set number of runs of random portfolio weights
num_portfolios = 5000

#set up array to hold results
results = np.zeros((3,num_portfolios))


for i in range(num_portfolios):
    #select random weights for portfolio holdings
    weights = np.random.random(3)
    #rebalance weights to sum to 1
    weights /= np.sum(weights)
    
    #calculate portfolio return and volatility
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252)
    
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = results[0,i] / results[1,i]

#convert results array to Pandas DataFrame
results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe'])

#create scatter plot coloured by Sharpe Ratio
plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
plt.colorbar()
