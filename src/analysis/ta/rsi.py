import pandas
import talib as ta


def getRSI(ticker, column='Close', timeperiod=14):
    df = pandas.read_csv("../../../resources/tickerList/" + ticker + "/history.csv")
    return ta.RSI(df[column].values, timeperiod)


def getRSIForAll(column='Close', timeperiod=14):
    result = []
    df = pandas.read_csv("../../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
    for index, row in df.iterrows():
        company = row['Ticker']
        result.append({
            company: getRSI(company, column, timeperiod)
        })
    return result


getRSIForAll()