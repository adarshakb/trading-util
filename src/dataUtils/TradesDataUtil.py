from pathlib import Path

import pandas

from src.analysis.trade.trade import TradeTypes
from src.dataUtils.PriceDataUtil import PriceColumnFormats


class TradesDataUtil:
    _repo_root = Path(__file__).resolve().parents[2]
    _resources_root = _repo_root / "resources" / "trades" / "ticker"

    @staticmethod
    def read_trades_data(strategy):
        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy) / "trades.csv"

        trade_type_lambda = lambda trade_type: TradeTypes[trade_type.split(".")[1]]
        df = pandas.read_csv(
            trades_resource_path,
            converters={"trade_type": trade_type_lambda},
            float_precision="round_trip",
        )
        df["entry_time"] = pandas.to_datetime(df["entry_time"])
        return df

    @staticmethod
    def save_trades_data(strategy, trades_df):
        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy)
        trades_resource_path.mkdir(parents=True, exist_ok=True)
        trades_df.to_csv(trades_resource_path / "trades.csv")

    @staticmethod
    def save_analysis_data(strategy, analysis_df):
        trades_resource_path = TradesDataUtil.get_trades_resource_path(strategy)
        trades_resource_path.mkdir(parents=True, exist_ok=True)
        analysis_df.to_csv(trades_resource_path / "analysis.csv")

    @staticmethod
    def save_ticker_analysis_data(ticker, analysis_df):
        trades_resource_path = TradesDataUtil.get_ticker_level_resource_path(ticker)
        trades_resource_path.mkdir(parents=True, exist_ok=True)
        analysis_df.to_csv(trades_resource_path / "analysis.csv")

    @staticmethod
    def save_all_combined_analysis_data(analysis_df):
        trades_resource_path = TradesDataUtil.get_resource_path()
        trades_resource_path.mkdir(parents=True, exist_ok=True)
        analysis_df.to_csv(trades_resource_path / "analysis.csv")

    # Backward-compatible aliases for existing misspelled names
    save_analysys_data = save_analysis_data
    save_ticker_analysys_data = save_ticker_analysis_data
    save_all_combined_analysys_data = save_all_combined_analysis_data

    @staticmethod
    def get_trades_resource_path(strategy):
        info = strategy.to_dict()
        trades_resource_path = (
            TradesDataUtil.get_ticker_level_resource_path(info["ticker"])
            / info["strategy_type"].value
            / str(info["trade_time_in_days"])
        )
        if strategy.start_time is None and strategy.end_time is None:
            trades_resource_path = trades_resource_path / "ALL"
        else:
            start = ""
            end = ""
            if strategy.start_time is not None:
                start = strategy.start_time.strftime(PriceColumnFormats.DATE_FORMAT)
            if strategy.end_time is not None:
                end = strategy.end_time.strftime(PriceColumnFormats.DATE_FORMAT)
            trades_resource_path = trades_resource_path / f"{start}_to_{end}"
        return trades_resource_path

    @staticmethod
    def get_ticker_level_resource_path(ticker):
        return TradesDataUtil.get_resource_path() / ticker

    @staticmethod
    def get_resource_path():
        return TradesDataUtil._resources_root
