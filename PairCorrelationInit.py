import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import coint
import seaborn
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# Input symbols that you want to compare
symbolsIds = ['SPY', 'AAPL', 'ADBE', 'LUV', 'MSFT',\
              'SKYW', 'QCOM', 'HPQ', 'JNPR', 'AMD', 'IBM']


def loadFinancialData(symbols, start_date, end_date):
    print('Creating a graph...')
    df = data.DataReader(symbols, 'yahoo', start_date, end_date)

    return df


data = loadFinancialData(symbolsIds, start_date='2001-01-01', end_date=today)


def findCointegratedPairs(data):
    n = data.shape[1]
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            result = coint(data[keys[i]], data[keys[j]])
            pvalue_matrix[i, j] = result[1]
            if result[1] < 0.02:
                pairs.append((keys[i], keys[j]))
    return pvalue_matrix, pairs


pvalues, pairs = findCointegratedPairs(data['Adj Close'])
print(pairs)
seaborn.heatmap(pvalues, xticklabels=symbolsIds, yticklabels=symbolsIds, cmap='RdYlGn_r', mask=(pvalues >= 0.98))
plt.show()


