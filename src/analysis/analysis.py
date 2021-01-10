from datetime import datetime

import pandas

from src.analysis.signals.strategies import BandStrategy, StrategyTypes
from src.analysis.trade.trade import TradeUtil
from src.dataUtils.PriceDataUtil import PriceData
from src.dataUtils.TradesDataUtil import TradesDataUtil


def produce_trades(ticker, strategy_type: StrategyTypes, number_of_days=45, start_time=None, end_time=None):
    print("Running produce_trades on ", ticker, strategy_type, number_of_days, start_time, end_time)
    tradeUtil = TradeUtil()
    strategy = BandStrategy(strategy_type=strategy_type, ticker=ticker, trade_time_in_days=number_of_days,
                            start_time=start_time, end_time=end_time)
    tradesList = strategy.potentialTrades()
    finaltrades = tradeUtil.convert_trades(trades_list=tradesList, start_time=start_time, end_time=end_time)
    TradesDataUtil.save_trades_data(strategy=strategy, trades_df=finaltrades)


def analyse_trade(ticker, strategy_type: StrategyTypes, number_of_days=45, start_time=None, end_time=None):
    print("Running analyse_trade on ", ticker, strategy_type, number_of_days, start_time, end_time)
    strategy = BandStrategy(strategy_type=strategy_type, ticker=ticker, trade_time_in_days=number_of_days,
                            start_time=start_time, end_time=end_time)
    trades = TradesDataUtil.read_trades_data(strategy=strategy)
    analysys = TradeUtil.get_analysis_from_trades(trades_list=trades)
    analysys['ticker'] = ticker
    analysys['strategy_type'] = strategy_type
    analysys['strategy_number_of_days'] = number_of_days
    analysys['strategy_start_time'] = start_time
    analysys['strategy_end_time'] = end_time
    TradesDataUtil.save_analysys_data(strategy=strategy, analysys_df=analysys)
    return analysys


def produce_all_trades_for(ticker):
    for strategy_type in StrategyTypes:
        for number_of_days in [45, 60]:
            produce_trades(ticker, strategy_type=strategy_type, number_of_days=number_of_days)


def analyse_all_trade_for(ticker):
    combined_analysis = None
    for strategy_type in StrategyTypes:
        for number_of_days in [45, 60]:
            analysys = analyse_trade(ticker, strategy_type=strategy_type, number_of_days=number_of_days)
            if combined_analysis is None:
                combined_analysis = analysys
            else:
                combined_analysis = combined_analysis.append(analysys, ignore_index=True)
    TradesDataUtil.save_ticker_analysys_data(ticker=ticker, analysys_df=combined_analysis)
    return combined_analysis

def produce_all_trades():
    df = PriceData.get_all_tickers()
    df = df.head(2)
    for index, row in df.iterrows():
        ticker = row['Ticker']
        print("produce_all_trades", ticker)
        produce_all_trades_for(ticker)

def analyse_all_trade():
    df = PriceData.get_all_tickers()
    df = df.head(2)
    combined_analysis = None
    for index, row in df.iterrows():
        ticker = row['Ticker']
        print("analyse_all_trade", ticker)
        analysys = analyse_all_trade_for(ticker)
        if combined_analysis is None:
            combined_analysis = analysys
        else:
            combined_analysis = combined_analysis.append(analysys, ignore_index=True)
    TradesDataUtil.save_all_combined_analysys_data(combined_analysis)


# produce_trades('aapl', strategy_type=StrategyTypes.BOLINGER_KELTNER_RSI, number_of_days=45, start_time=datetime(2015,1,1))
# analyse_trade('aapl', strategy_type=StrategyTypes.BOLINGER_KELTNER_RSI, number_of_days=45, start_time=datetime(2015,1,1))
# produce_all_trades_for('aapl')
# print(analyse_all_trade_for(ticker='aapl'))

# produce_all_trades()
analyse_all_trade()
