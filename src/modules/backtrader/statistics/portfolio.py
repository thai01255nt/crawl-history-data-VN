from typing import Dict

import pandas as pd


class PortfolioStatistic:
    @staticmethod
    def merge_positions(symbols, position_history: Dict) -> pd.DataFrame:
        positions_df = []
        for date in position_history:
            position = pd.DataFrame(position_history[date])
            position.columns = position.iloc[0]
            position = position[1:]
            position["symbol"] = symbols
            position["date"] = date
            positions_df.append(position)
        positions_df = pd.concat(positions_df, ignore_index=True)
        positions_df = positions_df[["date", "symbol", "size", "price", "datetime"]]
        return positions_df

    @staticmethod
    def merge_alpha_report(symbols, alpha_report: Dict) -> pd.DataFrame:
        alpha_report_df = []
        for date in alpha_report:
            alpha = pd.DataFrame(alpha_report[date])
            alpha.columns = alpha.iloc[0]
            alpha = alpha[1:]
            alpha["symbol"] = symbols
            alpha["date"] = date
            alpha_report_df.append(alpha)
        alpha_report_df = pd.concat(alpha_report_df, ignore_index=True)
        alpha_report_df = alpha_report_df[["date", "symbol", "alpha", "allocated_target"]]
        return alpha_report_df

    @staticmethod
    def merge_fees(fee_history: Dict) -> pd.DataFrame:
        date = list(fee_history.keys())
        fee_history = list(fee_history.values())
        fee_df = pd.DataFrame([date, fee_history]).T
        fee_df = fee_df.rename(columns={0: "date", 1: "fee"})
        return fee_df

    @staticmethod
    def merge_data_feeds(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        data_df = []
        for symbol in data:
            data_item = data[symbol].reset_index()
            data_item = data_item.rename(columns={"Date": "date"})
            data_item["symbol"] = symbol
            data_df.append(data_item)
        data_df = pd.concat(data_df, ignore_index=True)
        data_df = data_df[["date", "symbol", "Open", "Close"]].rename(columns={"Open": "open", "Close": "close"})
        return data_df

    @classmethod
    def merge(cls, data: Dict[str, pd.DataFrame], alpha_report: Dict, position_history: Dict) -> pd.DataFrame:
        symbols = list(data.keys())
        data_df = cls.merge_data_feeds(data=data)
        alpha_report_df = cls.merge_alpha_report(symbols=symbols, alpha_report=alpha_report)
        positions_df = cls.merge_positions(symbols=symbols, position_history=position_history)

        data_df = data_df.set_index(["date", "symbol"])
        alpha_report_df = alpha_report_df.set_index(["date", "symbol"])
        positions_df = positions_df.set_index(["date", "symbol"])
        results = positions_df.merge(alpha_report_df, left_index=True, right_index=True, how="left")
        results = results.merge(data_df, left_index=True, right_index=True, how="left")
        return results

    @classmethod
    def statistic(cls, data: Dict[str, pd.DataFrame], alpha_report: Dict, position_history: Dict, fee_history: Dict):
        history = cls.merge(data=data, alpha_report=alpha_report, position_history=position_history)
        history["cost"] = history["size"].abs() * history["price"]
        history["market_value"] = history["size"].abs() * history["close"]
        fees = cls.merge_fees(fee_history=fee_history)
        fees = fees.set_index("date")
        pnl = history[["cost", "market_value"]].groupby(level=["date"]).sum()
        pnl = pnl.merge(fees, left_index=True, right_index=True, how="left")
        pnl["pnl"] = pnl["market_value"] - pnl["cost"]
        pnl["return"] = (pnl["market_value"] - pnl["cost"]) / pnl["cost"]
        return history, pnl
