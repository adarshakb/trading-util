import pandas
import talib
import numpy
from src.analysis.ta import keltnerChannel
from src.analysis.ta.keltnerChannel import KeltnerChannel
from src.analysis.ta.rsi import RSI
from src.dataUtils.PriceDataUtil import PriceData


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
        self.df = PriceData.get_price_data(ticker=ticker)
        self.upperBand = None
        self.middleBand = None
        self.lowerBand = None

    def getName(self):
        return "BolingerBand"

    def getBBANDS(self):
        """
        :return: upper, middle, lower bands
        """

        if self.upperBand is None:
            upper, middle, lower = talib.BBANDS(self.df[self.column].values, timeperiod=self.timeperiod,
                                                nbdevup=self.nbdevup,
                                                nbdevdn=self.nbdevdn, matype=self.matype)
            self.upperBand = upper
            self.middleBand = middle
            self.lowerBand = lower

        return self.upperBand, self.middleBand, self.lowerBand

    def getBBANDSForAll(self):
        result = []
        companiesList = PriceData.get_all_tickers()
        for index, row in companiesList.iterrows():
            company = row['Ticker']
            result.append({
                company: BolingerBand(company).getBBANDS()
            })
        return result

    def compare_greter_than(self, idx, price, upperBand, keltnerUpperBand, rsi_indicator: RSI, rsi):
        if keltnerUpperBand is not None:
            if price <= keltnerUpperBand[idx]:
                return False
        if rsi_indicator is not None:
            if rsi[idx] <= rsi_indicator.high:
                return False
        if price <= upperBand[idx]:
            return False
        return True

    def compare_less_than(self, idx, price, lowerBand, keltnerLowerBand, rsi_indicator: RSI, rsi):
        if keltnerLowerBand is not None:
            if price >= keltnerLowerBand[idx]:
                return False
        if rsi_indicator is not None:
            if rsi[idx] >= rsi_indicator.low:
                return False
        if price >= lowerBand[idx]:
            return False
        return True

    def getSignals(self, keltnerChannel: KeltnerChannel = None, rsi_indicator: RSI = None):
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

        rsi = None
        if rsi_indicator:
            rsi = rsi_indicator.getRSI()

        for idx, price in numpy.ndenumerate(columnPrices):
            if idx[0] >= self.timeperiod - 1:
                # print(idx[0], price, upperBand[idx], middleBand[idx], lowerBand[idx])
                if self.compare_greter_than(idx, price, upperBand, keltnerUpperBand, rsi_indicator, rsi):
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
                        'rsi' : (rsi[idx] if rsi_indicator is not None else None),
                        'history': self.df.iloc[idx[0]].values.tolist()
                    }
                if self.compare_less_than(idx, price, lowerBand, keltnerLowerBand, rsi_indicator, rsi):  # verify if this right
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
                        'rsi' : (rsi[idx] if rsi_indicator is not None else None),
                        'history': self.df.iloc[idx[0]].values.tolist()
                    }

# for signal in BolingerBand('aapl').getSignals(keltnerChannel=None, rsi_indicator=RSI('aapl')):
#     print(signal)
