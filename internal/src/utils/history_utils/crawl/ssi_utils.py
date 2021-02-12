import requests
import json


class SSIUtils:
    base_url = 'https://iboard.ssi.com.vn/dchart/api/history?resolution={resolution}&symbol={symbol}&from={_from}&to={_to}'

    @staticmethod
    def get_history_resolution_1(symbol, _from, _to):
        response = requests.get(SSIUtils.base_url.format(symbol=symbol, resolution=1, _from=_from, _to=_to))
        results = json.loads(response.content)
        return results

    @staticmethod
    def convert_second_to_milisecond(data):
        for i in range(len(data['t'])):
            data['t'][i] = data['t'][i] * 1000
        return data
