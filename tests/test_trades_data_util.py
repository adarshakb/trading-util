import unittest
from datetime import datetime
from types import SimpleNamespace

from src.dataUtils.TradesDataUtil import TradesDataUtil


class _StrategyType:
    value = "BOLINGER"


class _DummyStrategy:
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "ticker": "AAPL",
            "strategy_type": _StrategyType(),
            "trade_time_in_days": 45,
        }


class TradesDataUtilPathTests(unittest.TestCase):
    def test_all_path_when_no_time_bounds(self):
        strategy = _DummyStrategy()
        path = TradesDataUtil.get_trades_resource_path(strategy)
        self.assertTrue(str(path).endswith("resources/trades/ticker/AAPL/BOLINGER/45/ALL"))

    def test_bounded_time_path(self):
        strategy = _DummyStrategy(start_time=datetime(2020, 1, 2), end_time=datetime(2020, 2, 3))
        path = TradesDataUtil.get_trades_resource_path(strategy)
        self.assertTrue(str(path).endswith("resources/trades/ticker/AAPL/BOLINGER/45/2020-01-02_to_2020-02-03"))


if __name__ == "__main__":
    unittest.main()
