import pandas as pd
import backtrader as bt


class PortfolioAnalyzer(bt.analyzers.Analyzer):
    def log(self, txt, dt=None):
        dt = dt or self.data.datetime[0]
        dt = bt.num2date(dt)
        # print("%s, %s" % (dt.isoformat(), txt))

    def create_analysis(self):
        self.position_history = {}
        self.fee_history = {}

    def notify_order(self, order):
        if order.status == order.Completed:
            dt = self.strategy.datetime.date()
            fee = self.fee_history.get(dt, 0)
            fee += order.executed.comm
            self.fee_history[dt] = fee
            if order.isbuy():
                buy_txt = "BUY COMPLETE {}, size = {:.2f}, price = {:.2f}, value = {:.2f}, Comm %.2f".format(
                    order.data._name,
                    order.executed.size,
                    order.executed.price,
                    order.executed.size * order.executed.price,
                    order.executed.comm,
                )
                self.log(buy_txt, order.executed.dt)
            else:
                sell_txt = "SELL COMPLETE {}, size = {:.2f}, price = {:.2f}, value = {:.2f}, Comm {:.2f}".format(
                    order.data._name,
                    order.executed.size,
                    order.executed.price,
                    order.executed.size * order.executed.price,
                    order.executed.comm,
                )
                self.log(sell_txt, order.executed.dt)
            self.log(self.strategy.broker.positions[order.data])
        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log("%s ," % order.Status[order.status])
            raise Exception("Some order failed or margin")
            pass

    def next(self):
        dt = self.strategy.datetime.date()
        positions = self.strategy.broker.positions
        # columns = ["size", "price", "adjbase", "upopened", "upclosed", "price_orig", "updt"]
        # if not self.position_history:
        #     for key in positions:
        #         self.position_history[key] = pd.DataFrame(columns=columns)
        # for key in positions:
        #     position = positions[key]
        #     data = [position.__dict__[column] for column in columns]
        #     self.position_history[key].loc[dt] = data
        # print(positions[0].__dict__)
        key = list(positions[next(iter(positions))].__dict__.keys())
        data = [key]
        data += [list(positions[key].__dict__.values()) for key in positions]
        self.position_history[dt] = data

    def get_analysis(self):
        return self.position_history, self.fee_history
