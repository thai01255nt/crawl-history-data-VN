from datetime import (
    datetime,
    timedelta
)
from third_parties.utils.third_party_requests import ThirdPartyRequest


class SsiHistoryResolution1Service:
    base_url = 'https://iboard.ssi.com.vn/dchart/api/history'

    def get(self, symbol: str, start: datetime, end: datetime):
        params = (
            ('resolution', 1),
            ('symbol', symbol),
            ('from', int(start.timestamp())),
            ('to', int(end.timestamp())),
        )
        data = ThirdPartyRequest.get(url=self.base_url, params=params)
        return data

    def get_example(self):
        symbol = 'MSN'
        end = datetime.now()
        start = end + timedelta(days=-3)
        params = (
            ('resolution', 1),
            ('symbol', symbol),
            ('from', int(start.timestamp())),
            ('to', int(end.timestamp())),
        )
        data = ThirdPartyRequest.get(url=self.base_url, params=params)
        return data


class SsiTicketService:

    def get_all(self):
        url = 'https://iboard.ssi.com.vn/dchart/api/1.1/defaultAllStocks'
        data = ThirdPartyRequest.get(url=url)
        return data
