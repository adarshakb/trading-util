import os

import pandas

from src.analysis.trade.trade import TradeTypes


class TradesDataUtil:
    trades_data_cache = {}

    @classmethod
    def read_trades_data(cls, strategy):
        if strategy.ticker in cls.trades_data_cache:
            return cls.trades_data_cache[strategy.ticker]

        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy) + 'trades.csv'

        trade_type_lambda = lambda type: TradeTypes[type.split(".")[1]]
        df = pandas.read_csv(trades_resource_path, converters={'trade_type': trade_type_lambda},
                             float_precision="round_trip")
        df['entry_time'] = pandas.to_datetime(df['entry_time'])

        cls.trades_data_cache[strategy.ticker] = df
        return cls.trades_data_cache[strategy.ticker]

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
    def get_trades_resource_path(strategy):
        info = strategy.to_dict()
        trades_resource_path = "../../resources/trades/ticker/" + info['ticker'] + "/" + info[
            'strategy_type'].value + "/" + str(info['trade_time_in_days']) + "/"
        if strategy.start_time is None and strategy.end_time is None:
            trades_resource_path += "ALL/"
        else:
            trades_resource_path += strategy.start_time + "_to_" + strategy.end_time
        return trades_resource_path
