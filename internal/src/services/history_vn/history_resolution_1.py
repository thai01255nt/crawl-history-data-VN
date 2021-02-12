from .base import BaseService
from internal.src.dao.history_resolution_1 import HistoryResolution1DAO
from internal.src.dao.ticket import TicketDAO
from internal.src.services.exception.response_exception import ResponseException
from internal.src.common.consts.response_consts import ResponseCode
from internal.src.common.consts.message_consts import TicketMessageConst
from internal.src.utils.history_utils.timestamp_utils import TimestampUtils
from internal.src.utils.history_utils.crawl.ssi_utils import SSIUtils
from internal.src.utils.data_utils import DataUtils


class HistoryResolution1Service(BaseService):
    def __init__(self):
        super().__init__(HistoryResolution1DAO())
        self.ticket_dao = TicketDAO()

    def update_newest_by_symbol(self, symbol):
        ticket_records = self.ticket_dao.get_by_symbol(symbol)
        if len(ticket_records) > 1:
            raise ResponseException(http_code=ResponseCode.INTERNAL_SERVER_ERROR,
                                    message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED.format(symbol=symbol))
        elif len(ticket_records) == 0:
            raise ResponseException(http_code=ResponseCode.NOT_FOUND,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol=symbol))
        last_timestamp = self.dao.get_last_timestamp_by_symbol(symbol)
        current_timestamp = int(TimestampUtils.timestamp_now())

        if last_timestamp is None:
            last_timestamp = TimestampUtils.minimum_timestamp - 1

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
        inserted_records = self.dao.add_all(converted_data)
        return DataUtils.records_to_dict(inserted_records)

    def update_newest_all_symbol(self):
        ticket_records = self.ticket_dao.get_all()
        if len(ticket_records) == 0:
            raise ResponseException(http_code=ResponseCode.NOT_FOUND,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol='all'))
        results = []
        try:
            for ticket_record in ticket_records:
                result = self.update_newest_by_symbol(ticket_record.symbol)
                results.append(
                    {
                        'symbol': ticket_record.symbol,
                        'num_history_resolution_1_data': len(result)
                    }
                )
        except:
            return results
        return results
