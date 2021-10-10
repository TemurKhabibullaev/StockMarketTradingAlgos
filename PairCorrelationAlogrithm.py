import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")

np.random.seed(123)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
symbolsIds = ['SPY', 'AAPL', 'ADBE', 'LUV', 'MSFT', 'SKYW', 'QCOM', 'HPQ', 'JNPR', 'AMD', 'IBM']


def loadFinancialData(symbols, start_date, end_date):
    print('Pending...')
    df = data.DataReader(symbols, 'yahoo', start_date, end_date)

    return df


def zscore(series):
    return (series - series.mean()) / np.std(series)


data = loadFinancialData(symbolsIds, start_date='2001-01-01', end_date=today)
print(symbolsIds)
first = str(input("Choose your first symbol from the list above:\n")).upper()
second = str(input("Choose your second symbol from the list above:\n")).upper()
FirstSymbolPrices = data['Adj Close'][first]
SecondSymbolPrices = data['Adj Close'][second]
ratios = FirstSymbolPrices / SecondSymbolPrices
ratios.plot()
buy = ratios.copy()
sell = ratios.copy()
buy[zscore(ratios) > -1] = 0
sell[zscore(ratios) < 1] = 0
buy.plot(color="g", linestyle="None", marker="^")
sell.plot(color="r", linestyle="None", marker="v")
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, ratios.min(), ratios.max()))
plt.legend(["Ratio", "Buy Signal", "Sell Signal"])
plt.show()


FirstSymbolBuy = FirstSymbolPrices.copy()
FirstSymbolSell = FirstSymbolPrices.copy()
SecondSymbolBuy = SecondSymbolPrices.copy()
SecondSymbolSell = SecondSymbolPrices.copy()

FirstSymbolPrices.plot()
FirstSymbolBuy[zscore(ratios) > -1] = 0
FirstSymbolSell[zscore(ratios) < 1] = 0
FirstSymbolBuy.plot(color="g", linestyle="None", marker="^")
FirstSymbolSell.plot(color="r", linestyle="None", marker="v")

pairCorrelationTradingAlgo = pd.DataFrame(index=FirstSymbolPrices.index)
pairCorrelationTradingAlgo['symbol1_price'] = FirstSymbolPrices
pairCorrelationTradingAlgo['symbol1_buy'] = np.zeros(len(FirstSymbolPrices))
pairCorrelationTradingAlgo['symbol1_sell'] = np.zeros(len(FirstSymbolPrices))
pairCorrelationTradingAlgo['symbol2_buy'] = np.zeros(len(FirstSymbolPrices))
pairCorrelationTradingAlgo['symbol2_sell'] = np.zeros(len(FirstSymbolPrices))

SecondSymbolPrices.plot()
SecondSymbolBuy[zscore(ratios) < 1] = 0
SecondSymbolSell[zscore(ratios) > -1] = 0
SecondSymbolBuy.plot(color="g", linestyle="None", marker="^")
SecondSymbolSell.plot(color="r", linestyle="None", marker="v")

x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, FirstSymbolPrices.min(), SecondSymbolPrices.max()))
plt.legend([f"{first}", "Buy Signal", "Sell Signal", f"{second}"])
plt.show()