from .base import BaseService
from ...dao.history_realtime import HistoryRealtimeDAO
from ...dao.ticket import TicketDAO
from ...utils.vndirect_utils.ticket_utils import TicketUtils
from ...utils.data_utils import DataUtils
from ..exception.response_exception import ResponseException
from ...common.consts.response_consts import ResponseCode
from ...common.consts.message_consts import TicketMessageConst


class TicketService(BaseService):
    def __init__(self):
        super().__init__(HistoryRealtimeDAO())
        self.ticket_dao = TicketDAO()

    def update_newest_by_symbol(self, symbol):
        ticket_records = self.ticket_dao.get_by_symbol(symbol)
        if len(ticket_records) > 1:
            raise ResponseException(http_code=ResponseCode.INTERNAL_SERVER_ERROR,
                                    message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED.format(symbol=symbol))
        elif len(ticket_records) == 0:
            raise ResponseException(http_code=ResponseCode.INTERNAL_SERVER_ERROR,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol=symbol))
        ticket_id = ticket_records[0].id
        history_realtime_record = self.dao.get_by_ticket_id(ticket_id)
        return history_realtime_record
