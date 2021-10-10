import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
from datetime import date
today = date.today()
today = today.strftime("%Y-%m-%d")
tickerName = str(input("Ticker name:\n"))
tickerName = tickerName.upper()


def financialData(symbol, start_date, end_date):
    print('Processing your request')
    df = data.DataReader(symbol, 'yahoo', start_date, end_date)
    return df


tickerData = financialData(tickerName, start_date='2019-01-01', end_date=today)


def doubleMovingAverage(financial_data, short_window, long_window):
    signals = pd.DataFrame(index=financial_data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = financial_data['Close'].\
        rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = financial_data['Close'].\
        rolling(window=long_window, min_periods=1, center=False).mean()
    signals['signal'][short_window:] =\
        np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['orders'] = signals['signal'].diff()
    return signals


ts = doubleMovingAverage(tickerData, 20, 100)
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel=f'{tickerName} in $')
tickerData["Adj Close"].plot(ax=ax1, color='g', lw=.5)
ts["short_mavg"].plot(ax=ax1, color='y', lw=2.)
ts["long_mavg"].plot(ax=ax1, color='b', lw=2.)
ax1.plot(ts.loc[ts.orders == 1.0].index, tickerData["Adj Close"][ts.orders == 1.0], '^', markersize=7, color='g')
ax1.plot(ts.loc[ts.orders == -1.0].index, tickerData["Adj Close"][ts.orders == -1.0], 'v', markersize=7, color='r')
plt.legend(["Price", "Short MA", "Long MA", "Bought", "Sold"])
plt.title("Double Moving Average Trading Algorithm")
plt.show()
