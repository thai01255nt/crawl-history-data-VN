import backtrader as bt
import numpy as np

from src.modules.backtrader.consts import DemoStrategyConsts
from src.modules.backtrader.websim_operators import SettingOperators, CrossSectionalOperators


class DemoStrategy(bt.Strategy):
    params = (
        ("universe", DemoStrategyConsts.UNIVERSE),
        ("alpha_report", {}),
    )

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime[0]
        dt = bt.num2date(dt)
        # print("%s, %s" % (dt.isoformat(), txt))

    def prenext(self):
        self.next()

    def next(self):
        # symbols = []
        open = []
        close = []
        high = []
        low = []
        volume = []
        for data in self.datas:
            # symbols.append(data._name)
            open.append(data.open[0])
            close.append(data.close[0])
            high.append(data.high[0])
            low.append(data.low[0])
            volume.append(data.volume[0])
        # symbols = np.array(symbols)
        open = np.array(open)
        close = np.array(close)
        high = np.array(high)
        low = np.array(low)
        volume = np.array(volume)

        universe = SettingOperators.universe(volumes=np.array([volume]), universes=np.array([[self.p.universe]]))
        universe = universe[0]

        alpha = (close - open) / ((high - low) + 0.001)
        alpha = CrossSectionalOperators.rank(np.array([alpha]))[0]
        universe_alpha = alpha
        universe_alpha[~universe] = np.nan
        neutralized_alpha = SettingOperators.neutralize(alpha=alpha)
        allocated_target = self.execute_alpha(alpha=neutralized_alpha)
        # results = np.stack((symbols, allocated_target), axis=1)
        # self.log(np.stack((symbols, open), axis=1))
        # self.log(results[~np.isnan(allocated_target)])
        # self.log(("totalwealth", self.broker.getvalue()))
        # self.log(("cash", self.broker.getcash()))

    def execute_alpha(self, alpha):
        book = DemoStrategyConsts.BOOK
        current_allocated_target = alpha * book
        current_allocated_target = np.nan_to_num(current_allocated_target, nan=0.0)

        # Make order
        for i in range(len(current_allocated_target)):
            target_value = current_allocated_target[i]
            data = self.datas[i]
            if np.isnan(target_value):
                self.order_target_value(data=data, target=0.0)
            else:
                self.order_target_value(data=data, target=target_value)
        alpha_report = np.array([alpha, current_allocated_target]).T
        alpha_report = [["alpha", "allocated_target"]] + alpha_report.tolist()
        self.p.alpha_report[self.datetime.date()] = alpha_report
        return current_allocated_target
