import os

import pandas

from src.analysis.trade.trade import TradeTypes
from src.dataUtils.PriceDataUtil import PriceColumnFormats


class TradesDataUtil:

    @staticmethod
    def read_trades_data(strategy):

        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy) + 'trades.csv'

        trade_type_lambda = lambda type: TradeTypes[type.split(".")[1]]
        df = pandas.read_csv(trades_resource_path, converters={'trade_type': trade_type_lambda},
                             float_precision="round_trip")
        df['entry_time'] = pandas.to_datetime(df['entry_time'])

        return df

    @staticmethod
    def save_trades_data(strategy, trades_df):
        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy)
        if not os.path.exists(trades_resource_path):
            os.makedirs(trades_resource_path)
        trades_df.to_csv(trades_resource_path + 'trades.csv')

    @staticmethod
    def save_analysys_data(strategy, analysys_df):
        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy)
        if not os.path.exists(trades_resource_path):
            os.makedirs(trades_resource_path)
        analysys_df.to_csv(trades_resource_path + 'analysys.csv')

    @staticmethod
    def save_ticker_analysys_data(ticker, analysys_df):
        trades_resource_path = TradesDataUtil.get_ticker_level_resource_path(ticker)
        if not os.path.exists(trades_resource_path):
            os.makedirs(trades_resource_path)
        analysys_df.to_csv(trades_resource_path + 'analysys.csv')

    @staticmethod
    def save_all_combined_analysys_data(analysys_df):
        trades_resource_path = TradesDataUtil.get_resource_path()
        if not os.path.exists(trades_resource_path):
            os.makedirs(trades_resource_path)
        analysys_df.to_csv(trades_resource_path + 'analysys.csv')

    @staticmethod
    def get_trades_resource_path(strategy):
        info = strategy.to_dict()
        trades_resource_path = TradesDataUtil.get_ticker_level_resource_path(info['ticker']) + info[
            'strategy_type'].value + "/" + str(info['trade_time_in_days']) + "/"
        if strategy.start_time is None and strategy.end_time is None:
            trades_resource_path += "ALL/"
        else:
            if strategy.start_time is not None:
                trades_resource_path += strategy.start_time.strftime(PriceColumnFormats.DATE_FORMAT)
            trades_resource_path += "_to_"
            if strategy.end_time is not None:
                trades_resource_path += strategy.end_time.strftime(PriceColumnFormats.DATE_FORMAT)
            trades_resource_path += "/"
        return trades_resource_path

    @staticmethod
    def get_ticker_level_resource_path(ticker):
        return TradesDataUtil.get_resource_path() + ticker + "/"

    @staticmethod
    def get_resource_path():
        return "../../resources/trades/ticker/"
