import pandas
import talib
import numpy

from src.dataUtils.PriceDataUtil import PriceData


class RSI():
    def __init__(self, ticker, column='Close', timeperiod=14, low=30, high=70):
        self.ticker = ticker
        self.column = column
        self.timeperiod = timeperiod
        self.low = low
        self.high = high
        self.df = PriceData.get_price_data(ticker=ticker)

    def getRSI(self):
        """

        :return: numpy.ndarray
        """
        return talib.RSI(self.df[self.column].values, self.timeperiod)

    def getRSIForAll(self):
        result = []
        companiesList = PriceData.get_all_tickers()
        for index, row in companiesList.iterrows():
            company = row['Ticker']
            result.append({
                company: RSI(company, self.column, self.timeperiod).getRSI()
            })
        return result

    def getSignals(self):
        """
        generate signal when RSI is above given low and high values
        :param low:
        :param high:
        :return:
        """
        rsiSignals = self.getRSI()
        indexs = numpy.argwhere(numpy.logical_or(rsiSignals < self.low, rsiSignals > self.high))
        for index in indexs:
            if rsiSignals[index[0]] < self.low:
                yield {
                    'type' : 'CROSS_LOWER_BAND',
                    'index' : index[0],
                    'rsiValue' : rsiSignals[index[0]],
                    'history' : self.df.iloc[index[0]].values.tolist()
                }
            else:
                yield {
                    'type' : 'CROSS_UPPER_BAND',
                    'index' : index[0],
                    'rsiValue' : rsiSignals[index[0]],
                    'history' : self.df.iloc[index[0]].values.tolist()
                }


# print(RSI(ticker='aapl').getSignals())
#
# for signal in RSI(ticker='aapl').getSignals():
#     print(signal)