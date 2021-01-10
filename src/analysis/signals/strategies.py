from enum import Enum

from src.analysis.ta.bollingerBand import BolingerBand
from src.analysis.ta.keltnerChannel import KeltnerChannel
from src.analysis.ta.rsi import RSI
from src.analysis.trade.trade import Trade, TradeTypes, TradeUtil
import datetime


class StrategyTypes(Enum):
    KELTNER = 'KELTNER'
    BOLINGER = 'BOLINGER'
    BOLINGER_KELTNER = 'BOLINGER_KELTNER'
    BOLINGER_RSI = 'BOLINGER_RSI'
    BOLINGER_KELTNER_RSI = 'BOLINGER_KELTNER_RSI'


class BandStrategy():
    # When stock prices continually touch the upper Band, the prices are thought to be overbought; conversely,
    # when they continually touch the lower band, prices are thought to be oversold, triggering a buy signal.
    def __init__(self, strategy_type: StrategyTypes, ticker='aapl', trade_time_in_days=45, start_time=None,
                 end_time=None):
        self.ticker = ticker
        self.strategy_type = strategy_type
        self.trade_time_in_days = trade_time_in_days
        self.start_time = start_time
        self.end_time = end_time
        self.strategyband = None
        self.strategyArgs = {}
        if strategy_type is StrategyTypes.KELTNER:
            self.strategyband = KeltnerChannel(ticker=self.ticker, start_time=start_time, end_time=end_time)
        if strategy_type is StrategyTypes.BOLINGER:
            self.strategyband = BolingerBand(ticker=self.ticker, start_time=start_time, end_time=end_time)
        if strategy_type is StrategyTypes.BOLINGER_KELTNER:
            self.strategyband = BolingerBand(ticker=self.ticker, start_time=start_time, end_time=end_time)
            self.strategyArgs['keltnerChannel'] = KeltnerChannel(ticker=self.ticker, start_time=start_time, end_time=end_time)
        if strategy_type is StrategyTypes.BOLINGER_RSI:
            self.strategyband = BolingerBand(ticker=self.ticker, start_time=start_time, end_time=end_time)
            self.strategyArgs['rsi_indicator'] = RSI(ticker=self.ticker, start_time=start_time, end_time=end_time)
        if strategy_type is StrategyTypes.BOLINGER_KELTNER_RSI:
            self.strategyband = BolingerBand(ticker=self.ticker, start_time=start_time, end_time=end_time)
            self.strategyArgs['keltnerChannel'] = KeltnerChannel(ticker=self.ticker, start_time=start_time, end_time=end_time)
            self.strategyArgs['rsi_indicator'] = RSI(ticker=self.ticker, start_time=start_time, end_time=end_time)

    def to_dict(self):
        return {
            'ticker': self.ticker,
            'strategy': self.strategyband.getName(),
            'strategy_type': self.strategy_type,
            'trade_time_in_days': self.trade_time_in_days
        }

    def potentialTrades(self):
        trades = []
        for signal in self.strategyband.getSignals(**self.strategyArgs):
            # print(signal)
            if signal['type'] == 'CROSS_UPPER_BAND':
                # sell as its getting hot
                signal_date = signal['history'][0]
                exit_date = signal_date + datetime.timedelta(days=self.trade_time_in_days)
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
                exit_date = signal_date + datetime.timedelta(days=self.trade_time_in_days)
                trade = Trade(ticker=self.ticker,
                              trade_type=TradeTypes.PUT,
                              entry_time=signal_date,
                              exit_time=exit_date,
                              target_execution_price=signal['middleBand'],
                              target_stop_loss=signal['lowerBand'] - ((signal['middleBand'] - signal['lowerBand']) / 2))
                trades.append(trade)
        return trades
