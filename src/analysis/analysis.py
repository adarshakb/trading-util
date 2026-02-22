from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas

from src.analysis.signals.strategies import BandStrategy, StrategyTypes
from src.analysis.trade.trade import TradeUtil
from src.dataUtils.PriceDataUtil import PriceData
from src.dataUtils.TradesDataUtil import TradesDataUtil


def _concat_frames(base: Optional[pandas.DataFrame], frame: pandas.DataFrame) -> pandas.DataFrame:
    if base is None:
        return frame
    return pandas.concat([base, frame], ignore_index=True)


def produce_trades(
    ticker: str,
    strategy_type: StrategyTypes,
    number_of_days: int = 45,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> None:
    print("Running produce_trades on", ticker, strategy_type, number_of_days, start_time, end_time)
    trade_util = TradeUtil()
    strategy = BandStrategy(
        strategy_type=strategy_type,
        ticker=ticker,
        trade_time_in_days=number_of_days,
        start_time=start_time,
        end_time=end_time,
    )
    trades_list = strategy.potentialTrades()
    final_trades = trade_util.convert_trades(
        trades_list=trades_list,
        start_time=start_time,
        end_time=end_time,
    )
    TradesDataUtil.save_trades_data(strategy=strategy, trades_df=final_trades)


def analyse_trade(
    ticker: str,
    strategy_type: StrategyTypes,
    number_of_days: int = 45,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> pandas.DataFrame:
    print("Running analyse_trade on", ticker, strategy_type, number_of_days, start_time, end_time)
    strategy = BandStrategy(
        strategy_type=strategy_type,
        ticker=ticker,
        trade_time_in_days=number_of_days,
        start_time=start_time,
        end_time=end_time,
    )
    trades = TradesDataUtil.read_trades_data(strategy=strategy)
    analysis = TradeUtil.get_analysis_from_trades(trades_list=trades)
    analysis["ticker"] = ticker
    analysis["strategy_type"] = strategy_type
    analysis["strategy_number_of_days"] = number_of_days
    analysis["strategy_start_time"] = start_time
    analysis["strategy_end_time"] = end_time
    TradesDataUtil.save_analysis_data(strategy=strategy, analysis_df=analysis)
    return analysis


def produce_all_trades_for(ticker: str) -> None:
    for strategy_type in StrategyTypes:
        for number_of_days in [45, 60]:
            produce_trades(ticker, strategy_type=strategy_type, number_of_days=number_of_days)


def analyse_all_trade_for(ticker: str) -> pandas.DataFrame:
    combined_analysis: Optional[pandas.DataFrame] = None
    for strategy_type in StrategyTypes:
        for number_of_days in [45, 60]:
            analysis = analyse_trade(ticker, strategy_type=strategy_type, number_of_days=number_of_days)
            combined_analysis = _concat_frames(combined_analysis, analysis)

    if combined_analysis is None:
        combined_analysis = pandas.DataFrame()

    TradesDataUtil.save_ticker_analysis_data(ticker=ticker, analysis_df=combined_analysis)
    return combined_analysis


def produce_all_trades(limit: int = 2) -> None:
    df = PriceData.get_all_tickers().head(limit)
    for _, row in df.iterrows():
        ticker = row["Ticker"]
        print("produce_all_trades", ticker)
        produce_all_trades_for(ticker)


def analyse_all_trade(limit: int = 2) -> None:
    df = PriceData.get_all_tickers().head(limit)
    combined_analysis: Optional[pandas.DataFrame] = None
    for _, row in df.iterrows():
        ticker = row["Ticker"]
        print("analyse_all_trade", ticker)
        analysis = analyse_all_trade_for(ticker)
        combined_analysis = _concat_frames(combined_analysis, analysis)

    if combined_analysis is None:
        combined_analysis = pandas.DataFrame()

    TradesDataUtil.save_all_combined_analysis_data(combined_analysis)


def main() -> None:
    analyse_all_trade()


if __name__ == "__main__":
    main()

# Example usage:
# produce_trades('aapl', strategy_type=StrategyTypes.BOLINGER_KELTNER_RSI, number_of_days=45, start_time=datetime(2015,1,1))
# analyse_trade('aapl', strategy_type=StrategyTypes.BOLINGER_KELTNER_RSI, number_of_days=45, start_time=datetime(2015,1,1))
# produce_all_trades_for('aapl')
# print(analyse_all_trade_for(ticker='aapl'))
# produce_all_trades()
