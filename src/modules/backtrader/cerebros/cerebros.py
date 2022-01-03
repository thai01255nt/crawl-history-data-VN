from typing import Dict
import pandas as pd
import backtrader as bt

from src.modules.backtrader.analyzers import PortfolioAnalyzer
from src.modules.backtrader.consts import DemoStrategyConsts
from src.modules.backtrader.data_feeds import HistoricalDataFeeds
from src.modules.backtrader.strategies import DemoStrategy


class DemoBacktraderCerebro:
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.cerebro = bt.Cerebro(maxcpus=None)
        self.data = data
        self.symbols = list(self.data.keys())
        print(self.symbols)

    def add_data_feeds(self, data: Dict[str, pd.DataFrame]):
        for symbol in data:
            data_feed = HistoricalDataFeeds(dataname=data[symbol])
            self.cerebro.adddata(data_feed, name=symbol)
        return

    def run(self):
        self.add_data_feeds(data=self.data)
        self.cerebro.broker.setcash(DemoStrategyConsts.INIT_CASH)
        self.cerebro.addstrategy(DemoStrategy)
        self.cerebro.addanalyzer(PortfolioAnalyzer)
        self.cerebro.broker.setcommission(commission=0.0015)
        print("start back test")
        return self.cerebro.run()[0]

        # Plot the result
        # self.cerebro.plot(style='bar')
