from src.analysis.signals.strategies import BandStrategy, StrategyTypes
from src.analysis.trade.trade import TradeUtil
from src.dataUtils.TradesDataUtil import TradesDataUtil


def produce_trades(ticker, strategy_type: StrategyTypes, number_of_days=45):
    print("Running produce_trades on ", ticker, strategy_type, number_of_days)
    tradeUtil = TradeUtil()
    strategy = BandStrategy(strategy_type=strategy_type, ticker=ticker, trade_time_in_days=number_of_days)
    tradesList = strategy.potentialTrades()
    finaltrades = tradeUtil.convert_trades(trades_list=tradesList)
    TradesDataUtil.save_trades_data(strategy=strategy, trades_df=finaltrades)


def analyse_trade(ticker, strategy_type: StrategyTypes, number_of_days=45):
    print("Running analyse_trade on ", ticker, strategy_type, number_of_days)
    strategy = BandStrategy(strategy_type=strategy_type, ticker=ticker, trade_time_in_days=number_of_days)
    trades = TradesDataUtil.read_trades_data(strategy=strategy)
    analysys = TradeUtil.get_analysis_from_trades(trades_list=trades)
    TradesDataUtil.save_analysys_data(strategy=strategy, analysys_df=analysys)


def produce_all_trades_for(ticker):
    for strategy_type in StrategyTypes:
        for number_of_days in [45, 60]:
            produce_trades(ticker, strategy_type=strategy_type, number_of_days=number_of_days)

def analyse_all_trade_for(ticker):
    for strategy_type in StrategyTypes:
        for number_of_days in [45, 60]:
            analyse_trade(ticker, strategy_type=strategy_type, number_of_days=number_of_days)

# produce_all_trades_for('aapl')
analyse_all_trade_for(ticker='aapl')
