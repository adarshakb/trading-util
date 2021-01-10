import pandas


class PriceColumnFormats:
    DATE_FORMAT = "%Y-%m-%d"


class PriceData:
    price_date_cache = {}

    @classmethod
    def get_price_data(cls, ticker, start_time=None, end_time=None):
        df = None
        if ticker in cls.price_date_cache:
            df = cls.price_date_cache[ticker]
        else:
            df = pandas.read_csv("../../resources/tickerList/" + ticker + "/history.csv",
                                 float_precision="round_trip")
            df['Date'] = pandas.to_datetime(df['Date'])
            cls.price_date_cache[ticker] = df

        if start_time is not None:
            df = df[df['Date'] >= start_time]
        if end_time is not None:
            df = df[df['Date'] <= end_time]
        # print(df)
        return df

    @staticmethod
    def get_all_tickers():
        df = pandas.read_csv("../../resources/tickerList/NASDAQ-100-Stock-Tickers-List.csv")
        return df
