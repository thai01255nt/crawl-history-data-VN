import bs4 as bs
import requests
import yfinance as yf
import os
import pandas as pd
import glob

from typing import List, Dict

from src.modules.data.consts import YahooConsts


class YahooDatasetService:
    LIST_SYMBOL = None
    DATA_SET = None

    @staticmethod
    def pull():
        if os.path.exists(YahooConsts.DATASET_FOLDER):
            print(f"Data is already pulled in {YahooConsts.DATASET_FOLDER} folder, this function will be ignored.")
            return
        os.mkdir(YahooConsts.DATASET_FOLDER)
        resp = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        soup = bs.BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", {"class": "wikitable sortable"})
        tickers = []
        for row in table.findAll("tr")[1:]:
            ticker = row.findAll("td")[0].text
            tickers.append(ticker)

        tickers = [s.replace("\n", "") for s in tickers]
        tickers = tickers[: YahooConsts.PULLED_DATA_NUM]
        start_time = YahooConsts.START_TIME
        end_time = YahooConsts.END_TIME
        data = yf.download(tickers, start=start_time, end=end_time)
        symbols = list(data.columns.get_level_values(1))
        print(f"Saving data: {len(symbols)} symbols")
        for i in range(len(symbols)):
            symbol = symbols[i]
            print(f"- Saving {symbol}, {i}")
            data_item = data.iloc[:, data.columns.get_level_values(1) == symbol]
            data_item.columns = data_item.columns.droplevel(1)
            data_item.to_csv(f"{YahooConsts.DATASET_FOLDER}/{symbol}.csv")

    @staticmethod
    def get_list_symbol():
        if YahooDatasetService.LIST_SYMBOL is None:
            files = glob.glob(os.path.join(YahooConsts.DATASET_FOLDER, "*"))
            results = [os.path.basename(file)[:-4] for file in files]
            YahooDatasetService.LIST_SYMBOL = results
        return YahooDatasetService.LIST_SYMBOL

    @staticmethod
    def load_dataset(symbols: List[str]) -> Dict[str, pd.DataFrame]:
        if YahooDatasetService.DATA_SET is None:
            YahooDatasetService.DATA_SET = {}
            for symbol in symbols:
                stock_csv_path = os.path.join(YahooConsts.DATASET_FOLDER, f"{symbol}.csv")
                if not os.path.exists(stock_csv_path):
                    raise Exception(f"File not exists: {stock_csv_path}")
                data = pd.read_csv(stock_csv_path, index_col="Date")
                data.index = pd.to_datetime(data.index)
                YahooDatasetService.DATA_SET[symbol] = data
        return YahooDatasetService.DATA_SET

    @staticmethod
    def get_all_data():
        return YahooDatasetService.load_dataset(symbols=YahooDatasetService.get_list_symbol())
