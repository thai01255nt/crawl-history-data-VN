from flask_api import status
from internal.libs.http_handlers.exception.response_exception import ResponseException
from internal.libs.http_handlers.exception.exception_consts import ExceptionMessage
from internal.libs.utils.postgres_utils import PostgresUtils

from internal.src.utils.postgres_utils import CustomPostgresUtils
from internal.src.services.history_vn.history_vn_consts import TicketMessageConst
from internal.src.services.base import BaseService
from internal.src.services.third_party.ssi.crawling import SsiTicketService
from internal.src.repositories.ticket import TicketRepository


class TicketService(BaseService):
    def __init__(self):
        super().__init__(TicketRepository())
        self.ticket_repo = TicketRepository()
        self.ssi_ticket_service = SsiTicketService()

    def get_by_symbol(self, symbol):
        ticket_records = self.ticket_repo.get_by_symbol(symbol)
        if len(ticket_records) > 1:
            raise ResponseException(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED.format(symbol=symbol))
        elif len(ticket_records) == 0:
            raise ResponseException(http_code=status.HTTP_404_NOT_FOUND,
                                    message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS.format(symbol=symbol))
        return ticket_records

    def update_newest(self):
        return_data = {
            'insertedRecords': [],
            'updatedRecords': []
        }
        ssi_ticket_data = self.ssi_ticket_service.get_all_ticket()
        history_vn_ticket_dataframe = CustomPostgresUtils.records_to_dataframe(self.ticket_repo.get_all_records())

        if history_vn_ticket_dataframe is None:
            # Insert all
            inserted_records = self.ticket_repo.insert_records(ssi_ticket_data)
            return_data['insertedRecords'] = PostgresUtils.records_to_dict(inserted_records)
            return return_data

        insert_datas = []
        update_datas = []
        for ssi_ticket_data in ssi_ticket_data:
            history_vn_ticket_rows = history_vn_ticket_dataframe[
                history_vn_ticket_dataframe['symbol'] == ssi_ticket_data['symbol']]
            # Insert if not exists
            if len(history_vn_ticket_rows) == 0:
                insert_datas.append(ssi_ticket_data)
            elif len(history_vn_ticket_rows) > 1:
                raise ResponseException(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED.format(
                                            symbol=ssi_ticket_data['symbol']))
            else:
                # Compare 2 dict
                ssi_ticket_data['id'] = history_vn_ticket_rows.iloc[0]['id']
                if dict(history_vn_ticket_rows.iloc[0]) != ssi_ticket_data:
                    update_datas.append(ssi_ticket_data)
        inserted_records = self.ticket_repo.insert_records(insert_datas)
        update_records = self.ticket_repo.up(update_datas)
        return_data['insertedRecords'] = DataUtils.records_to_dict(inserted_records)
        return_data['updatedRecords'] = DataUtils.records_to_dict(update_records)
        return return_data
