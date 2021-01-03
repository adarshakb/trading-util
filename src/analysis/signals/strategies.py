from src.analysis.ta.bollingerBand import BolingerBand
from src.analysis.trade.trade import Trade, TradeTypes, TradeUtil
import datetime

from src.dataUtils.PriceDataUtil import PriceColumnFormats, PriceData


class bolingerBandStrategy():
    # When stock prices continually touch the upper Bollinger Band®, the prices are thought to be overbought; conversely, when they continually touch the lower band, prices are thought to be oversold, triggering a buy signal.
    def __init__(self, ticker='aapl'):
        self.ticker = ticker
        self.bolingerband = BolingerBand(ticker=self.ticker)

    def potentialTrades(self, trade_time_in_days=45):
        trades = []
        for signal in self.bolingerband.getSignals():
            # print(signal)
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



# TradeUtil.convert_trades(trades_list=bolingerBandStrategy(ticker='alxn').potentialTrades(45))

tickers = PriceData.get_all_tickers()
for ticker, name in tickers.itertuples(index=False):
    print(ticker, name)
    TradeUtil.convert_trades(trades_list=bolingerBandStrategy(ticker=ticker).potentialTrades(45))
    TradeUtil.convert_trades(trades_list=bolingerBandStrategy(ticker=ticker).potentialTrades(60))
