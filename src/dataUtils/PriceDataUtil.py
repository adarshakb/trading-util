import pandas


class PriceColumnFormats:
    DATE_FORMAT = "%Y-%m-%d"


class PriceData:
    price_date_cache = {}
    @classmethod
    def get_price_data(cls, ticker):
        if ticker in cls.price_date_cache:
            return cls.price_date_cache[ticker]

        df = pandas.read_csv("../../resources/tickerList/" + ticker + "/history.csv",
                               float_precision="round_trip")
        df['Date'] = pandas.to_datetime(df['Date'])

        cls.price_date_cache[ticker] = df
        return cls.price_date_cache[ticker]

    @staticmethod
    def get_all_tickers():
        df = pandas.read_csv("../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
        return df
