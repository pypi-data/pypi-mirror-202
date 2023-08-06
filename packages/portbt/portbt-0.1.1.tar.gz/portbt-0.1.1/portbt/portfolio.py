from dataclasses import dataclass

from pandas import DataFrame, Series

from .backtest_functions import backtest_with_rebalance, backtest_without_rebalance


@dataclass
class Backtest:
    values: DataFrame | Series
    exposure: DataFrame | Series
    result: DataFrame | Series
    all_dates: list
    rebal_dates: list

    def set_parameters(self, backtest):
        self.values = backtest["values"].copy()
        self.exposure = backtest["exposure"].copy()
        self.result = backtest["result"].copy()
        self.all_dates = backtest["all_dates"].copy()
        self.rebal_dates = backtest["rebal_dates"].copy()

    @staticmethod
    def run_backtest_with_rebalance(prices, rebal_weights="ew", rebal_freq="1M"):
        _backtest = backtest_with_rebalance(prices=prices, rebal_weights=rebal_weights, rebal_freq=rebal_freq)
        Backtest.set_parameters(Backtest, _backtest)

    @staticmethod
    def run_backtest_without_rebalance(prices, start_weights="ew"):
        _backtest = backtest_without_rebalance(prices, start_weights=start_weights)
        Backtest.set_parameters(Backtest, _backtest)


@dataclass
class Portfolio:
    prices: DataFrame

    @property
    def backtest(self):
        return Backtest

    @property
    def tickers(self):
        return self.prices.columns.to_list()
