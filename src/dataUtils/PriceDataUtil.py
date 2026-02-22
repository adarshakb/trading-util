from pathlib import Path

import pandas


class PriceColumnFormats:
    DATE_FORMAT = "%Y-%m-%d"


class PriceData:
    price_date_cache = {}
    _repo_root = Path(__file__).resolve().parents[2]
    _resources_root = _repo_root / "resources"

    @classmethod
    def get_price_data(cls, ticker, start_time=None, end_time=None):
        if ticker in cls.price_date_cache:
            df = cls.price_date_cache[ticker]
        else:
            history_path = cls._resources_root / "tickerList" / ticker / "history.csv"
            df = pandas.read_csv(history_path, float_precision="round_trip")
            df["Date"] = pandas.to_datetime(df["Date"])
            cls.price_date_cache[ticker] = df

        if start_time is not None:
            df = df[df["Date"] >= start_time]
        if end_time is not None:
            df = df[df["Date"] <= end_time]
        return df

    @classmethod
    def get_all_tickers(cls):
        tickers_path = cls._resources_root / "tickerList" / "NASDAQ-100-Stock-Tickers-List.csv"
        return pandas.read_csv(tickers_path)
