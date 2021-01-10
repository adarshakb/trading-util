import datetime
from enum import Enum
import numpy
import pandas

from src.dataUtils.PriceDataUtil import PriceData


class TradeTypes(Enum):
    BUY = 1
    SELL = 2
    SHORT = 3
    PUT = 4
    CALL = 5


class Trade:
    def __init__(self, ticker, trade_type: TradeTypes, entry_time, exit_time, target_execution_price, target_stop_loss, actual_execution_price=None, actual_execution_ticker_data=None):
        self.ticker = ticker
        self.trade_type = trade_type
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.target_execution_price = target_execution_price
        self.stop_loss = target_stop_loss
        self.actual_execution_price = actual_execution_price
        self.actual_execution_ticker_data = actual_execution_ticker_data
        if self.actual_execution_ticker_data is not None:
            assert len(actual_execution_ticker_data.index) is 1

    def adjust_exit_time_based_on_market_holidays(self):
        df = PriceData.get_price_data(ticker=self.ticker)
        max_date = df['Date'].max()
        while df[numpy.equal(df['Date'], self.exit_time)].shape[0] is 0:
            self.exit_time = self.exit_time + datetime.timedelta(days=1)
            if self.exit_time > max_date:
                return False

        return True

    def to_dict(self):
        return {
            'ticker': self.ticker,
            'trade_type': self.trade_type,
            'entry_time': self.entry_time,
            'exit_time': self.exit_time,
            'target_execution_price': self.target_execution_price,
            'stop_loss': self.stop_loss,
            'actual_execution_price': self.actual_execution_price,
            'actual_execution_ticker_data': self.actual_execution_ticker_data.to_dict('records')
        }


class TradeUtil:
    def convert_trades(self, trades_list, column='Close'):
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
                ticker_data_for_actual_execution = ticker_data[numpy.equal(ticker_data['Date'], trade.entry_time)]
                finaltrades.append(Trade(ticker=trade.ticker,
                                         trade_type=TradeTypes.SELL,
                                         entry_time=trade.entry_time,
                                         exit_time=None,
                                         target_execution_price=None,
                                         target_stop_loss=None,
                                         actual_execution_price=ticker_data_for_actual_execution.iloc[0][column],
                                         actual_execution_ticker_data=ticker_data_for_actual_execution))
                possibleEarlyExit = ticker_data_filtered_date[numpy.logical_or(ticker_data_filtered_date['Low'] <= trade.target_execution_price, ticker_data_filtered_date['High'] >= trade.stop_loss)]
                if possibleEarlyExit.shape[0] > 0:
                    # either the short's target price hit or we hit stop loss
                    # print(possibleEarlyExit)
                    earlyExit = possibleEarlyExit.iloc[0]
                    ticker_data_for_actual_execution = ticker_data[numpy.equal(ticker_data['Date'], earlyExit['Date'])]
                    finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.BUY,
                                             entry_time=earlyExit['Date'],
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data_for_actual_execution.iloc[0][column],
                                             actual_execution_ticker_data=ticker_data_for_actual_execution))
                else:
                    #check if market was opn on our exit date
                    if not trade.adjust_exit_time_based_on_market_holidays():
                        #our trade is outside bounds of known market data. lets clean up and skip
                        # print("lets skip as its in future", trade.exit_time)
                        finaltrades.pop()
                    else:
                        ticker_data_for_actual_execution = ticker_data[numpy.equal(ticker_data['Date'], trade.exit_time)]
                        finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.BUY,
                                             entry_time=trade.exit_time,
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data_for_actual_execution.iloc[0][column],
                                             actual_execution_ticker_data=ticker_data_for_actual_execution))

            if trade.trade_type is TradeTypes.PUT:
                ticker_data_for_actual_execution = ticker_data[numpy.equal(ticker_data['Date'], trade.entry_time)]
                finaltrades.append(Trade(ticker=trade.ticker,
                                         trade_type=TradeTypes.BUY,
                                         entry_time=trade.entry_time,
                                         exit_time=None,
                                         target_execution_price=None,
                                         target_stop_loss=None,
                                         actual_execution_price=ticker_data_for_actual_execution.iloc[0][column],
                                         actual_execution_ticker_data=ticker_data_for_actual_execution))
                possibleEarlyExit = ticker_data_filtered_date[numpy.logical_or(ticker_data_filtered_date['Low'] <= trade.stop_loss, ticker_data_filtered_date['High'] >= trade.target_execution_price)]
                if possibleEarlyExit.shape[0] > 0:
                    # either the short's target price hit or we hit stop loss
                    # print(possibleEarlyExit)
                    earlyExit = possibleEarlyExit.iloc[0]
                    ticker_data_for_actual_execution = ticker_data[numpy.equal(ticker_data['Date'], earlyExit['Date'])]
                    finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.SELL,
                                             entry_time=earlyExit['Date'],
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data_for_actual_execution.iloc[0][column],
                                             actual_execution_ticker_data=ticker_data_for_actual_execution))
                else:
                    if not trade.adjust_exit_time_based_on_market_holidays():
                        #our trade is outside bounds of known market data. lets clean up and skip
                        # print("lets skip as its in future", trade.exit_time)
                        finaltrades.pop()
                    else:
                        ticker_data_for_actual_execution = ticker_data[numpy.equal(ticker_data['Date'], trade.exit_time)]
                        finaltrades.append(Trade(ticker=trade.ticker,
                                             trade_type=TradeTypes.SELL,
                                             entry_time=trade.exit_time,
                                             exit_time=None,
                                             target_execution_price=None,
                                             target_stop_loss=None,
                                             actual_execution_price=ticker_data_for_actual_execution.iloc[0][column],
                                             actual_execution_ticker_data=ticker_data_for_actual_execution))

        return TradeUtil.convert_trades_to_dataframe(finaltrades)

    @staticmethod
    def convert_trades_to_dataframe(trades_list):
        return pandas.DataFrame.from_records([t.to_dict() for t in trades_list])

    @staticmethod
    def get_analysis_from_trades(trades_list, start_date=None, end_date=None):
        money = 0
        prev_trade_type = None
        prev_trade_value = None
        prev_trade_date = None
        no_profitable_trade = 0
        start_date = None
        total_num_time_in_trade = datetime.timedelta(0)
        for index, row in trades_list.iterrows():
            if start_date is None:
                start_date = row['entry_time']
            if row['trade_type'] is TradeTypes.BUY:
                money -= row['actual_execution_price']
                if prev_trade_type is TradeTypes.SELL and row['actual_execution_price'] < prev_trade_value:
                    no_profitable_trade += 1
                    total_num_time_in_trade += row['entry_time'] - prev_trade_date
                    prev_trade_type = None
                    prev_trade_value = None
                    prev_trade_date = None
                else:
                    prev_trade_type = TradeTypes.BUY
                    prev_trade_value = row['actual_execution_price']
                    prev_trade_date = row['entry_time']
            if row['trade_type'] is TradeTypes.SELL:
                money += row['actual_execution_price']
                if prev_trade_type is TradeTypes.BUY and row['actual_execution_price'] > prev_trade_value:
                    no_profitable_trade += 1
                    total_num_time_in_trade += row['entry_time'] - prev_trade_date
                    prev_trade_type = None
                    prev_trade_value = None
                    prev_trade_date = None
                else:
                    prev_trade_type = TradeTypes.SELL
                    prev_trade_value = row['actual_execution_price']
                    prev_trade_date = row['entry_time']
        number_of_trades = len(trades_list.index)/2
        return pandas.DataFrame([{
            'start_date': start_date,
            'number_of_trades': number_of_trades,
            'no_profitable_trade': no_profitable_trade,
            'no_losing_trades': number_of_trades-no_profitable_trade,
            'avg_profit_or_loss': money/number_of_trades,
            'probablity_of_profit': no_profitable_trade/number_of_trades,
            'avg_number_of_days_in_trade': total_num_time_in_trade.days/number_of_trades,
            'profit_or_loss': money
        }])



