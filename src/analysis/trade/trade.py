import datetime
from enum import Enum
import numpy

from src.dataUtils.PriceDataUtil import PriceData


class TradeTypes(Enum):
    BUY = 1
    SELL = 2
    SHORT = 3
    PUT = 4
    CALL = 5


class Trade:
    def __init__(self, ticker, trade_type: TradeTypes, entry_time, exit_time, target_execution_price, target_stop_loss, actual_execution_price=None):
        self.ticker = ticker
        self.trade_type = trade_type
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.target_execution_price = target_execution_price
        self.stop_loss = target_stop_loss
        self.actual_execution_price = actual_execution_price

    def adjust_exit_time_based_on_market_holidays(self):
        df = PriceData.get_price_data(ticker=self.ticker)
        max_date = df['Date'].max()
        while df[numpy.equal(df['Date'], self.exit_time)].shape[0] is 0:
            self.exit_time = self.exit_time + datetime.timedelta(days=1)
            if self.exit_time > max_date:
                return False

        return True


class TradeUtil:

    @staticmethod
    def convert_trades(trades_list, column='Close'):
        """
        Convert the PUTs and CALLs to BUYs and SELLs
        :param trades_list:
        :return:
        """
        df = {}
        finaltrades = []
        trades_list.sort(key=lambda t: t.entry_time) #sort based on trade's start time
        for i in range(0, len(trades_list)):
            trade = trades_list[i]

            if len(finaltrades) > 0 and trade.entry_time < finaltrades[len(finaltrades)-1].entry_time:
                #if there are some trades scheduled, make sure we are only processing trade signals after the last one so we dont "overlap" trades
                continue

            if trade.ticker not in df:
                df[trade.ticker] = PriceData.get_price_data(ticker=trade.ticker)
            ticker_data = df[trade.ticker]
            # print(trade.ticker, trade.trade_type, trade.entry_time, trade.exit_time, trade.target_execution_price, trade.stop_loss)
            ticker_data_filtered_date = ticker_data[numpy.logical_and(ticker_data['Date'] >= trade.entry_time, ticker_data['Date'] <= trade.exit_time)]
            if trade.trade_type is TradeTypes.SHORT:
                finaltrades.append(Trade(ticker=trade.ticker,
                                         trade_type=TradeTypes.SELL,
                                         entry_time=trade.entry_time,
                                         exit_time=None,
                                         target_execution_price=None,
                                         target_stop_loss=None,
                                         actual_execution_price=ticker_data[numpy.equal(ticker_data['Date'], trade.entry_time)].iloc[0][column]))
                possibleEarlyExit = ticker_data_filtered_date[numpy.logical_or(ticker_data_filtered_date['Low'] <= trade.target_execution_price, ticker_data_filtered_date['High'] >= trade.stop_loss)]
                if possibleEarlyExit.shape[0] > 0:
                    # either the short's target price hit or we hit stop loss
                    # print(possibleEarlyExit)
                    earlyExit = possibleEarlyExit.iloc[0]
                    finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.BUY,
                                             entry_time=earlyExit['Date'],
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data[numpy.equal(ticker_data['Date'], earlyExit['Date'])].iloc[0][column]))
                else:
                    #check if market was opn on our exit date
                    if not trade.adjust_exit_time_based_on_market_holidays():
                        #our trade is outside bounds of known market data. lets clean up and skip
                        # print("lets skip as its in future", trade.exit_time)
                        finaltrades.pop()
                    else :
                        finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.BUY,
                                             entry_time=trade.exit_time,
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data[numpy.equal(ticker_data['Date'], trade.exit_time)].iloc[0][column]))

            if trade.trade_type is TradeTypes.PUT:
                finaltrades.append(Trade(ticker=trade.ticker,
                                         trade_type=TradeTypes.BUY,
                                         entry_time=trade.entry_time,
                                         exit_time=None,
                                         target_execution_price=None,
                                         target_stop_loss=None,
                                         actual_execution_price=ticker_data[numpy.equal(ticker_data['Date'], trade.entry_time)].iloc[0][column]))
                possibleEarlyExit = ticker_data_filtered_date[numpy.logical_or(ticker_data_filtered_date['Low'] <= trade.stop_loss, ticker_data_filtered_date['High'] >= trade.target_execution_price)]
                if possibleEarlyExit.shape[0] > 0:
                    # either the short's target price hit or we hit stop loss
                    # print(possibleEarlyExit)
                    earlyExit = possibleEarlyExit.iloc[0]
                    finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.SELL,
                                             entry_time=earlyExit['Date'],
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data[numpy.equal(ticker_data['Date'], earlyExit['Date'])].iloc[0][column]))
                else:
                    if not trade.adjust_exit_time_based_on_market_holidays():
                        #our trade is outside bounds of known market data. lets clean up and skip
                        # print("lets skip as its in future", trade.exit_time)
                        finaltrades.pop()
                    else:
                        finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.SELL,
                                             entry_time=trade.exit_time,
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data[numpy.equal(ticker_data['Date'], trade.exit_time)].iloc[0][column]))

        money = 0
        for t in finaltrades:
            # print(t.ticker, t.trade_type, t.entry_time, t.exit_time, t.target_execution_price, t.stop_loss, t.actual_execution_price)
            if t.trade_type is TradeTypes.BUY:
                money -= t.actual_execution_price
            if t.trade_type is TradeTypes.SELL:
                money += t.actual_execution_price
        print("money after all trades", money)

        return finaltrades



