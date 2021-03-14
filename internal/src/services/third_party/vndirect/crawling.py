import os
import json
import datetime
import requests


class VndirectHistoryResolutionDService:
    BASE_URL = 'https://finfo-api.vndirect.com.vn/v4'
    TIME_FORMAT = '%Y-%m-%d'

    def get_history_resolution_D(self, symbol: str, gte: datetime.datetime, lte: datetime.datetime):
        def generate_url(symbol, gte, lte, page):
            url = os.path.join(
                self.BASE_URL,
                'stock_prices',
                f'?sort=date'
                f'&q=code:{symbol}'
                f'~date:gte:{self.datetime_to_string(gte)}'
                f'~date:lte:{self.datetime_to_string(lte)}'
                f'&size=15'
                f'&page={page}'
            )
            return url

        # Get number pages first
        response = requests.get(generate_url(symbol=symbol, gte=gte, lte=lte, page=1))
        response_dict = json.loads(response.content)
        total_pages = response_dict['totalPages']

        # Get all data
        results = []
        for page in range(total_pages):
            response = requests.get(generate_url(symbol=symbol, gte=gte, lte=lte, page=page + 1))
            response_dict = json.loads(response.content)
            data = response_dict['data']
            results += self.convert_raw_raw_history_resolution_d_into_schema(data)
        return results

    def convert_raw_raw_history_resolution_d_into_schema(self, raw_datas):
        # Mapping raw_data into TicketSchema
        history_resolution_d_datas = []
        for raw_data in raw_datas:
            history_resolution_d_data = {
                'symbol': raw_data['code'],
                'date': raw_data['date'],
                'time': raw_data['time'],
                'stockOperator': raw_data['floor'],
                'type': raw_data['type'],
                'basicPrice': raw_data['basicPrice'],
                'ceilingPrice': raw_data['ceilingPrice'],
                'floorPrice': raw_data['floorPrice'],
                'open': raw_data['open'],
                'high': raw_data['high'],
                'low': raw_data['low'],
                'close': raw_data['close'],
                'average': raw_data['average'],
                'adjustOpen': raw_data['adOpen'],
                'adjustHigh': raw_data['adHigh'],
                'adjustLow': raw_data['adLow'],
                'adjustClose': raw_data['adClose'],
                'adjustAverage': raw_data['adAverage'],
                'normalVolume': raw_data['nmVolume'],
                'normalValue': raw_data['nmValue'],
                'putThroughVolume': raw_data['ptVolume'],
                'putThroughValue': raw_data['ptValue'],
                'change': raw_data['change'],
                'adjustChange': raw_data['adChange'],
                'percentageChange': raw_data['pctChange']
            }
            history_resolution_d_datas.append(history_resolution_d_data)
        return history_resolution_d_datas

    def datetime_to_string(self, _datetime: datetime.datetime):
        return _datetime.strftime(self.TIME_FORMAT)

    def string_to_datetime(self, string: str):
        return datetime.datetime.strptime(string, self.TIME_FORMAT)

    def convert_second_to_milisecond(self, data):
        for i in range(len(data['t'])):
            data['t'][i] = data['t'][i] * 1000
        return data
