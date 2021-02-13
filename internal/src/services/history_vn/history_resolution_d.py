import datetime

from .base import BaseService
from internal.src.dao.history_resolution_d import HistoryResolutionDDAO
from internal.src.dao.ticket import TicketDAO
from internal.src.services.exception.response_exception import ResponseException
from internal.src.common.consts.response_consts import ResponseCode
from internal.src.common.consts.message_consts import TicketMessageConst
from internal.src.utils.history_utils.timestamp_utils import TimestampUtils
from internal.src.utils.history_utils.crawl.vndirect_utils import VndirectUtils
from internal.src.utils.data_utils import DataUtils


class HistoryResolutionDService(BaseService):
    def __init__(self):
        super().__init__(HistoryResolutionDDAO())
        self.ticket_dao = TicketDAO()

    def update_newest_by_symbol(self, symbol):
        ticket_records = self.ticket_dao.get_by_symbol(symbol)
        if len(ticket_records) > 1:
            raise ResponseException(http_code=ResponseCode.INTERNAL_SERVER_ERROR,
                                    message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED.format(symbol=symbol))
        elif len(ticket_records) == 0:
            raise ResponseException(http_code=ResponseCode.NOT_FOUND,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol=symbol))
        last_datetime = self.dao.get_last_datetime_by_symbol(symbol)
        current_datetime = TimestampUtils.gmt7_now()

        if last_datetime is None:
            last_datetime = \
                datetime.datetime.fromtimestamp(TimestampUtils.minimum_timestamp) - datetime.timedelta(days=1)

        # Get data from last_datetime + 1 day to current_time
        data = VndirectUtils.get_history_resolution_D(symbol=symbol,
                                                      gte=last_datetime + datetime.timedelta(days=1),
                                                      lte=current_datetime)
        inserted_records = self.dao.add_all(data)
        return DataUtils.records_to_dict(inserted_records)

    def update_newest_all_symbol(self):
        ticket_records = self.ticket_dao.get_all()
        if len(ticket_records) == 0:
            raise ResponseException(http_code=ResponseCode.NOT_FOUND,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol='all'))
        results = []
        for ticket_record in ticket_records:
            try:
                result = self.update_newest_by_symbol(ticket_record.symbol)
                if len(results) > 0:
                    results.append(
                        {
                            'symbol': ticket_record.symbol,
                            'num_history_resolution_d_data': len(result)
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
