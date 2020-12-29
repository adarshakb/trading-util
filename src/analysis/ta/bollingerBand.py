import pandas
import talib
import numpy
from src.analysis.ta import keltnerChannel
from src.analysis.ta.keltnerChannel import KeltnerChannel


class BolingerBand():
    def __init__(self, ticker, column='Close', timeperiod=20, nbdevup=2, nbdevdn=2, matype=0):
        """
        :param ticker: the market ticker
        :param column: Column in the data frame csv
        :param timeperiod: input for BBANDS
        :param nbdevup: input for BBANDS
        :param nbdevdn: input for BBANDS
        :param matype: input for BBANDS
        """
        self.ticker = ticker
        self.column = column
        self.timeperiod = timeperiod
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn
        self.matype = matype
        self.df = pandas.read_csv("../../../resources/tickerList/" + ticker + "/history.csv", float_precision="round_trip")

    def getBBANDS(self):
        """
        :return: upper, middle, lower bands
        """
        return talib.BBANDS(self.df[self.column].values, timeperiod=self.timeperiod, nbdevup=self.nbdevup,
                            nbdevdn=self.nbdevdn, matype=self.matype)

    def getBBANDSForAll(self):
        result = []
        companiesList = pandas.read_csv("../../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
        for index, row in companiesList.iterrows():
            company = row['Ticker']
            result.append({
                company: BolingerBand(company).getBBANDS()
            })
        return result

    def getSignals(self, keltnerChannel: KeltnerChannel):
        """

        generate signals when stock price is above upper band or below lower bands
        :return:
        """

        # below are 1d numpy.ndarray
        upperBand, middleBand, lowerBand = self.getBBANDS()
        columnPrices = self.df[self.column].values

        keltnerUpperBand = None
        keltnerrMiddleBand = None
        keltnerLowerBand = None
        if keltnerChannel:
            keltnerUpperBand, keltnerrMiddleBand, keltnerLowerBand = keltnerChannel.getKeltnerChannel()

        for idx, price in numpy.ndenumerate(columnPrices):
            if idx[0] >= self.timeperiod - 1:
                # print(idx[0], price, upperBand[idx], middleBand[idx], lowerBand[idx])
                if ((keltnerChannel is None and price > upperBand[idx]) or
                        (keltnerChannel is not None and price > upperBand[idx] > keltnerUpperBand[idx])): #verify if this right
                    yield {
                        'index': idx[0],
                        'type': 'CROSS_UPPER_BAND',
                        'price': price,
                        'upperBand': upperBand[idx],
                        'middleBand': middleBand[idx],
                        'lowerBand': lowerBand[idx],
                        'keltnerUpperBand': (keltnerUpperBand[idx] if keltnerChannel is not None else None),
                        'keltnerrMiddleBand': (keltnerrMiddleBand[idx] if keltnerChannel is not None else None),
                        'keltnerLowerBand': (keltnerLowerBand[idx] if keltnerChannel is not None else None),
                        'history': self.df.iloc[idx[0]].values.tolist()
                    }
                if ((keltnerChannel is None and price < lowerBand[idx]) or
                        (keltnerChannel is not None and price < lowerBand[idx] < keltnerLowerBand[idx])): #verify if this right
                    yield {
                        'index': idx[0],
                        'type': 'CROSS_LOWER_BAND',
                        'price': price,
                        'upperBand': upperBand[idx],
                        'middleBand': middleBand[idx],
                        'lowerBand': lowerBand[idx],
                        'keltnerUpperBand': (keltnerUpperBand[idx] if keltnerChannel is not None else None),
                        'keltnerrMiddleBand': (keltnerrMiddleBand[idx] if keltnerChannel is not None else None),
                        'keltnerLowerBand': (keltnerLowerBand[idx] if keltnerChannel is not None else None),
                        'history': self.df.iloc[idx[0]].values.tolist()
                    }
#
# for signal in BolingerBand('aapl').getSignals(keltnerChannel=KeltnerChannel('aapl')):
#     print(signal)
