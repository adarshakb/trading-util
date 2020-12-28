import pandas
import talib


def getKeltnerChannel(ticker, column='Close', timeperiod=20, atrMultiple=2):
    """
    Keltner channel https://www.investopedia.com/terms/k/keltnerchannel.asp
    :param ticker: the market ticker
    :param column: Column in the data frame csv
    :param timeperiod: input for EMA and ATR
    :return: lower band, middle band, upper band
    """
    df = pandas.read_csv("../../../resources/tickerList/" + ticker + "/history.csv")
    ema = talib.EMA(df[column].values, timeperiod)
    atr = talib.ATR(df['High'].values, df['Low'].values, df['Close'].values, timeperiod)
    return ema - (atrMultiple * atr), ema, ema + (atrMultiple * atr)


def getKeltnerChannelForAll(column='Close', timeperiod=20, atrMultiple=2):
    result = []
    df = pandas.read_csv("../../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
    for index, row in df.iterrows():
        company = row['Ticker']
        result.append({
            company: getKeltnerChannel(company, column, timeperiod, atrMultiple)
        })
    return result

# print(getKeltnerChannel('aapl'))