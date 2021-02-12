import os
import requests
import json

from ..common.utils.index_utils import IndexUtils


class VndirectUtils:
    base_url = 'https://finfo-api.vndirect.com.vn/v4'

    def get_history_all_stocks(self, sort, gte, lte):
        # Get number pages first
        response = requests.get(
            os.path.join(finfoUtils.base_url, f'?sort=date&date:gte:2020-01-25~date:lte:2021-01-31'))
        result = json.loads(response.content)
        total_pages = result['totalPages']

        # Loop page to get all
        # for page in total_pages:
    @staticmethod
    def convert_second_to_milisecond(data):
        for i in range(len(data['t'])):
            data['t'][i] = data['t'][i] * 1000
        return data
