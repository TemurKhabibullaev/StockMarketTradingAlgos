import sys
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from datetime import date
today = date.today()
today = today.strftime("%Y-%m-%d")
tickerName = str(input("Ticker name:\n"))
tickerName = tickerName.upper()


def loadFinancialFata(symbol, start_date, end_date):
    print('Pending...')
    df = data.DataReader(symbol, 'yahoo', start_date, end_date)
    return df


tickerData = loadFinancialFata(tickerName, start_date='2000-01-01', end_date=today)


def turtleTrading(financialData, window_size):
    signals = pd.DataFrame(index=financialData.index)
    signals['orders'] = 0
    signals['high'] = financialData['Adj Close'].shift(1).\
        rolling(window=window_size).max()
    signals['low'] = financialData['Adj Close'].shift(1).\
        rolling(window=window_size).min()
    signals['avg'] = financialData['Adj Close'].shift(1).\
        rolling(window=window_size).mean()
    signals['long_entry'] = financialData['Adj Close'] > signals.high
    signals['short_entry'] = financialData['Adj Close'] < signals.low
    signals['long_exit'] = financialData['Adj Close'] < signals.avg
    signals['short_exit'] = financialData['Adj Close'] > signals.avg
    position = 0
    for k in range(len(signals)):
        if signals['long_entry'][k] and position == 0:
            signals.orders.values[k] = 1
            position =1
        elif signals['short_entry'][k] and position == 0:
            signals.orders.values[k] = -1
            position = -1
        elif signals['short_exit'][k] and position > 0:
            signals.orders.values[k] = -1
            position = 0
        elif signals['long_exit'][k] and position < 0:
            signals.orders.values[k] = 1
            position = 0
        else:
            signals.orders.values[k] = 0
    return signals


turtleStrategy = turtleTrading(tickerData, 50)
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel=f'{tickerName} in $')
tickerData["Adj Close"].plot(ax=ax1, color='g', lw=.5)
turtleStrategy["high"].plot(ax=ax1, color='g', lw=.5)
turtleStrategy["low"].plot(ax=ax1, color='r', lw=.5)
turtleStrategy["avg"].plot(ax=ax1, color='b', lw=.5)
ax1.plot(turtleStrategy.loc[turtleStrategy.orders == 1.0].index, tickerData["Adj Close"][turtleStrategy.orders == 1.0], '^', markersize=7, color='g')
ax1.plot(turtleStrategy.loc[turtleStrategy.orders == -1.0].index, tickerData["Adj Close"][turtleStrategy.orders == -1.0], 'v', markersize=7, color='r')
plt.legend(["Price", "Highs", "Lows", "Average", "Buy", "Sell"])
plt.title("Turtle Trading Algorithm")
plt.show()
sys.exit(0)

