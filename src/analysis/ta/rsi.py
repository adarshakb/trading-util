import pandas
import talib


def getRSI(ticker, column='Close', timeperiod=14):
    df = pandas.read_csv("../../../resources/tickerList/" + ticker + "/history.csv")
    return talib.RSI(df[column].values, timeperiod)


def getRSIForAll(column='Close', timeperiod=14):
    result = []
    df = pandas.read_csv("../../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
    for index, row in df.iterrows():
        company = row['Ticker']
        result.append({
            company: getRSI(company, column, timeperiod)
        })
    return result


# print(getRSIForAll())
