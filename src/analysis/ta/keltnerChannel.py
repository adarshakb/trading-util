import pandas
import talib
import numpy

from src.dataUtils.PriceDataUtil import PriceData


class KeltnerChannel():
    def __init__(self, ticker, column='Close', timeperiod=20, atrMultiple=2):
        """
        Keltner channel https://www.investopedia.com/terms/k/keltnerchannel.asp
        :param ticker: the market ticker
        :param column: Column in the data frame csv
        :param timeperiod: input for EMA and ATR
        """
        self.ticker = ticker
        self.column = column
        self.timeperiod = timeperiod
        self.atrMultiple = atrMultiple
        self.df = PriceData.get_price_data(ticker=ticker)

    def getName(self):
        return "KeltnerChannel"

    def getKeltnerChannel(self):
        """
        :return: upper band, middle band, lower band
        """
        ema = talib.EMA(self.df[self.column].values, self.timeperiod)
        atr = talib.ATR(self.df['High'].values, self.df['Low'].values, self.df['Close'].values, self.timeperiod)
        return ema + (self.atrMultiple * atr), ema, ema - (self.atrMultiple * atr)

    def getKeltnerChannelForAll(self):
        result = []
        df = PriceData.get_all_tickers()
        for index, row in df.iterrows():
            company = row['Ticker']
            result.append({
                company: KeltnerChannel(company).getKeltnerChannel()
            })
        return result
    def getSignals(self):
        """

        generate signals when stock price is above upper band or below lower bands
        :return:
        """

        # below are 1d numpy.ndarray
        upperBand, middleBand, lowerBand = self.getKeltnerChannel()
        columnPrices = self.df[self.column].values

        for idx, price in numpy.ndenumerate(columnPrices):
            if idx[0] >= self.timeperiod - 1:
                # print(idx[0], price, upperBand[idx], middleBand[idx], lowerBand[idx])
                if price > upperBand[idx]:
                    yield {
                        'index' : idx[0],
                        'type': 'CROSS_UPPER_BAND',
                        'price': price,
                        'upperBand': upperBand[idx],
                        'middleBand': middleBand[idx],
                        'lowerBand': lowerBand[idx],
                        'history': self.df.iloc[idx[0]].values.tolist()
                    }
                if price < lowerBand[idx]:
                    yield {
                        'index' : idx[0],
                        'type': 'CROSS_LOWER_BAND',
                        'price': price,
                        'upperBand': upperBand[idx],
                        'middleBand': middleBand[idx],
                        'lowerBand': lowerBand[idx],
                        'history': self.df.iloc[idx[0]].values.tolist()
                    }



# print(KeltnerChannel('aapl').getKeltnerChannel())

# for signal in KeltnerChannel('aapl').getSignals():
#     print(signal)