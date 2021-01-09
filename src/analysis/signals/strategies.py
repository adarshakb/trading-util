from enum import Enum

from src.analysis.ta.bollingerBand import BolingerBand
from src.analysis.ta.keltnerChannel import KeltnerChannel
from src.analysis.ta.rsi import RSI
from src.analysis.trade.trade import Trade, TradeTypes, TradeUtil
import datetime

from src.dataUtils.PriceDataUtil import PriceColumnFormats, PriceData
class StrategyTypes(Enum):
    BOLINGER = 1
    KELTNER = 2
    BOLINGER_KELTNER = 3
    RSI = 4

class bandStrategy():
    # When stock prices continually touch the upper Band®, the prices are thought to be overbought; conversely, when they continually touch the lower band, prices are thought to be oversold, triggering a buy signal.
    def __init__(self, strategy_type : StrategyTypes, ticker='aapl'):
        self.ticker = ticker
        self.strategyband = None
        self.strategyArgs = []
        if strategy_type is StrategyTypes.BOLINGER:
            self.strategyband = BolingerBand(ticker=self.ticker)
        if strategy_type is StrategyTypes.KELTNER:
            self.strategyband = KeltnerChannel(ticker=self.ticker)
        if strategy_type is StrategyTypes.BOLINGER_KELTNER:
            self.strategyband = BolingerBand(ticker=self.ticker)
            self.strategyArgs.append(KeltnerChannel(ticker=self.ticker))
        if strategy_type is StrategyTypes.RSI:
            self.strategyband = RSI(ticker=self.ticker)

    def potentialTrades(self, trade_time_in_days=45):
        trades = []
        for signal in self.strategyband.getSignals(*self.strategyArgs):
            print(signal)
            if signal['type'] == 'CROSS_UPPER_BAND':
                # sell as its getting hot
                signal_date = signal['history'][0]
                exit_date = signal_date + datetime.timedelta(days=trade_time_in_days)
                trade = Trade(ticker=self.ticker,
                              trade_type=TradeTypes.SHORT,
                              entry_time=signal_date,
                              exit_time=exit_date,
                              target_execution_price=signal['middleBand'],
                              target_stop_loss=signal['upperBand'] + ((signal['upperBand'] - signal['middleBand']) / 2))
                trades.append(trade)
            if signal['type'] == 'CROSS_LOWER_BAND':
                # call
                signal_date = signal['history'][0]
                exit_date = signal_date + datetime.timedelta(days=trade_time_in_days)
                trade = Trade(ticker=self.ticker,
                              trade_type=TradeTypes.PUT,
                              entry_time=signal_date,
                              exit_time=exit_date,
                              target_execution_price=signal['middleBand'],
                              target_stop_loss=signal['lowerBand'] - ((signal['middleBand'] - signal['lowerBand']) / 2))
                trades.append(trade)
        return trades



# TradeUtil.convert_trades(trades_list=bandStrategy(strategy_type = StrategyTypes.BOLINGER, ticker='aapl').potentialTrades(45))
# TradeUtil.convert_trades(trades_list=bandStrategy(strategy_type = StrategyTypes.KELTNER, ticker='aapl').potentialTrades(45))
# TradeUtil.convert_trades(trades_list=bandStrategy(strategy_type = StrategyTypes.BOLINGER_KELTNER, ticker='aapl').potentialTrades(45))
TradeUtil.convert_trades(trades_list=bandStrategy(strategy_type = StrategyTypes.RSI, ticker='aapl').potentialTrades(45))


# tickers = PriceData.get_all_tickers()
# for ticker, name in tickers.itertuples(index=False):
#     print(ticker, name)
#     TradeUtil.convert_trades(trades_list=bolingerBandStrategy(ticker=ticker).potentialTrades(45))
#     TradeUtil.convert_trades(trades_list=bolingerBandStrategy(ticker=ticker).potentialTrades(60))
