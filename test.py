import numpy as np
import pandas as pd
import backtrader as bt
from datetime import datetime
from src.modules.data.services import YahooDatasetService
from src.modules.backtrader.websim_operators import SettingOperators, CrossSectionalOperators
from src.modules.backtrader.cerebros import DemoBacktraderCerebro
from src.modules.backtrader.statistics import PortfolioStatistic

# Pull data from yahoo
YahooDatasetService.pull()

# Load data from csv files
symbols = YahooDatasetService.get_list_symbol()
data = YahooDatasetService.load_dataset(symbols)

# Run backtesting
test_demo = DemoBacktraderCerebro(data=data)
st = test_demo.run()

# extract output and statistics
position_history, fee_history = st.analyzers.portfolioanalyzer.get_analysis()
alpha_report = st.p.alpha_report
history, pnl = PortfolioStatistic.statistic(
    data=data, alpha_report=alpha_report, position_history=position_history, fee_history=fee_history
)
# 2.88 s ± 12.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)