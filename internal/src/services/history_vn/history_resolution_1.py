from flask_api import status

from internal.libs.http_handlers.exception.response_exception import ResponseException
from internal.libs.utils.timestamp_utils import TimestampUtils

from internal.src.services.base import BaseService
from internal.src.services.history_vn.ticket import TicketService
from internal.src.services.history_vn.history_vn_consts import TicketMessageConst
from internal.src.repositories.history_resolution_1 import HistoryResolution1Repository


class HistoryResolution1Service(BaseService):
    def __init__(self):
        super().__init__(HistoryResolution1Repository())
        self.history_resolution_1_repo = HistoryResolution1Repository()
        self.ticket_service = TicketService()

    def update_newest_by_symbol(self, symbol):
        ticket_records = self.ticket_service.get_by_symbol(symbol=symbol)
        last_timestamp_record = self.history_resolution_1_repo.get_last_timestamp_record_by_symbol(symbol)
        if last_timestamp_record is None:
            last_timestamp = TimestampUtils.minimum_timestamp - 1
        else:
            last_timestamp = last_timestamp_record.t
        current_timestamp = int(TimestampUtils.timestamp_now())

        # Get data from last_timestamp+1 to current_time
        data = SSIUtils.get_history_resolution_1(symbol=symbol, _from=last_timestamp + 1, _to=current_timestamp)
        converted_data = []
        if data['s'] == 'no_data':
            return []
        elif 't' not in data:
            return []
        for i in range(len(data['t'])):
            converted_data.append(
                {
                    't': data['t'][i],
                    'c': data['c'][i],
                    'o': data['o'][i],
                    'h': data['h'][i],
                    'l': data['l'][i],
                    'v': data['v'][i],
                    'symbol': symbol
                }
            )
        inserted_records = self.history_resolution_1_repo.insert_records(converted_data)
        return inserted_records

    def update_newest_all_symbol(self):
        ticket_records = self.ticket_repo.get_all()
        if len(ticket_records) == 0:
            raise ResponseException(http_code=status.HTTP_404_NOT_FOUND,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol='all'))
        results = []
        for ticket_record in ticket_records:
            try:
                result = self.update_newest_by_symbol(ticket_record.symbol)
                if len(result) > 0:
                    results.append(
                        {
                            'symbol': ticket_record.symbol,
                            'num_history_resolution_1_data': len(result)
                        }
                    )
            except Exception as error:
                results.append(
                    {
                        'symbol': ticket_record.symbol,
                        'error': str(error)
                    }
                )
                return results
        return results
