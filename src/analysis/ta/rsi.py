import pandas
import talib
import numpy


class RSI():
    def __init__(self, ticker, column='Close', timeperiod=14):
        self.ticker = ticker
        self.column = column
        self.timeperiod = timeperiod
        self.df = pandas.read_csv("../../../resources/tickerList/" + ticker + "/history.csv", float_precision="round_trip")

    def getRSI(self):
        """

        :return: numpy.ndarray
        """
        return talib.RSI(self.df[self.column].values, self.timeperiod)

    def getRSIForAll(self):
        result = []
        companiesList = pandas.read_csv("../../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
        for index, row in companiesList.iterrows():
            company = row['Ticker']
            result.append({
                company: RSI(company, self.column, self.timeperiod).getRSI()
            })
        return result

    def getSignals(self, low=30, high=70):
        """
        generate signal when RSI is above given low and high values
        :param low:
        :param high:
        :return:
        """
        rsiSignals = self.getRSI()
        indexs = numpy.argwhere(numpy.logical_or(rsiSignals < low, rsiSignals > high))
        for index in indexs:
            yield {
                'index' : index[0],
                'rsiValue' : rsiSignals[index[0]],
                'history' : self.df.iloc[index[0]].values.tolist()
            }


# print(RSI(ticker='aapl').getSignals())

# for signal in RSI(ticker='aapl').getSignals():
#     print(signal)