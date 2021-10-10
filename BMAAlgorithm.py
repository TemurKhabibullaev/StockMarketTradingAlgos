import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import sys
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")
tickerName = str(input("Ticker name:\n"))
tickerName = tickerName.upper()


def loadFinancialFata(symbol, start_date, end_date):
    print('Searching...')
    df = data.DataReader(symbol, 'yahoo', start_date, end_date)

    return df


TickerData = loadFinancialFata(tickerName, start_date='2015-01-01', end_date=today)


def basicMomentumTrading(financialData, conseqDays):
    signals = pd.DataFrame(index=financialData.index)
    signals['orders'] = 0
    consDay = 0
    priorPrice = 0
    init = True
    for k in range(len(financialData['Adj Close'])):
        price = financialData['Adj Close'][k]
        if init:
            priorPrice = price
            init = False
        elif price > priorPrice:
            if consDay < 0:
                consDay = 0
            consDay += 1
        elif price < priorPrice:
            if consDay > 0:
                consDay = 0
            consDay -= 1
        if consDay == conseqDays:
            signals['orders'][k] = 1
        elif consDay == -conseqDays:
            signals['orders'][k] = - 1

    return signals


ts = basicMomentumTrading(TickerData, 5)
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel=f'{tickerName} in $')
TickerData["Adj Close"].plot(ax=ax1, color='g', lw=.5)
ax1.plot(ts.loc[ts.orders == 1.0].index, TickerData["Adj Close"][ts.orders == 1], '^', markersize=7, color='g')
ax1.plot(ts.loc[ts.orders == -1.0].index, TickerData["Adj Close"][ts.orders == -1], 'v', markersize=7, color='r')
plt.legend(["Price", "Buy", "Sell"])
plt.title("Basic Momentum Trading Algorithm")
plt.show()
sys.exit(0)