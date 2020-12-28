import pandas
import talib


def getBBANDS(ticker, column='Close', timeperiod=20, nbdevup=2, nbdevdn=2, matype=0):
    """
    :param ticker: the market ticker
    :param column: Column in the data frame csv
    :param timeperiod: input for BBANDS
    :param nbdevup: input for BBANDS
    :param nbdevdn: input for BBANDS
    :param matype: input for BBANDS
    :return: upper, middle, lower bands
    """
    df = pandas.read_csv("../../../resources/tickerList/" + ticker + "/history.csv")
    return talib.BBANDS(df['Close'].values, timeperiod, nbdevup, nbdevdn, matype)


def getBBANDSForAll(column='Close', timeperiod=20, nbdevup=2, nbdevdn=2, matype=0):
    result = []
    df = pandas.read_csv("../../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
    for index, row in df.iterrows():
        company = row['Ticker']
        result.append({
            company: getBBANDS(company, column, timeperiod, nbdevup, nbdevdn, matype)
        })
    return result


print(getBBANDSForAll())
