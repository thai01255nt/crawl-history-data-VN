from flask_api import status
from libs.response.exception.base_exception import BaseExceptionResponse

from internal.services.base import BaseService
from internal.repositories.ticket import TicketRepository
from internal.services.history_vn.history_vn_consts import TicketMessageConst
from internal.utils.database_utils import DatabaseUtils

from third_parties.ssi.crawling import SsiTicketService


class TicketService(BaseService):
    def __init__(self):
        super().__init__(TicketRepository())
        self.ticket_repo = TicketRepository()
        self.ssi_ticket_service = SsiTicketService()

    def get_by_symbol(self, symbol):
        ticket_records = self.ticket_repo.get_by_symbol(symbol)
        if len(ticket_records) > 1:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error = BaseExceptionResponse.ErrorObject(body_code=code,
                                                      message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED,
                                                      location_type=self.get_by_symbol.__qualname__,
                                                      location=symbol)
            raise BaseExceptionResponse(http_code=code,
                                        body_code=code,
                                        message=error.message,
                                        errors=[error])
        elif len(ticket_records) == 0:
            code = status.HTTP_404_NOT_FOUND
            error = BaseExceptionResponse.ErrorObject(body_code=code,
                                                      message=TicketMessageConst.TICKET_SYMBOL_NOT_EXISTS,
                                                      location_type=self.get_by_symbol.__qualname__,
                                                      location=symbol)

            raise BaseExceptionResponse(http_code=code,
                                        body_code=code,
                                        message=error.message,
                                        errors=[error])
        return ticket_records

    def update_newest(self):
        return_data = {
            'insertedRecords': [],
            'updatedRecords': []
        }
        raw_ticket_data = self.ssi_ticket_service.get_all()
        ticket_data = self.convert_raw_into_ticket_entity(raw_data=raw_ticket_data)
        current_ticket_dataframe = DatabaseUtils.records_to_dataframe(self.ticket_repo.get_all_records())

        if current_ticket_dataframe is None:
            # Insert all
            inserted_records = self.ticket_repo.insert_records(ticket_data)
            return_data['insertedRecords'] = DatabaseUtils.records_to_dict(inserted_records)
            return return_data

        insert_data = []
        update_data = []
        for ticket_data_item in ticket_data:
            current_ticket_rows = current_ticket_dataframe[
                current_ticket_dataframe['symbol'] == ticket_data_item['symbol']]
            # Insert if not exists
            if len(current_ticket_rows) == 0:
                insert_data.append(ticket_data_item)
            else:
                # Compare 2 dict
                ticket_data_item['id'] = current_ticket_rows.iloc[0]['id']
                if dict(current_ticket_rows.iloc[0]) != ticket_data_item:
                    update_data.append(ticket_data_item)
        inserted_records = self.ticket_repo.insert_records(insert_data)
        update_records = self.ticket_repo.update_records_by_id(update_data)
        return_data['insertedRecords'] = DatabaseUtils.records_to_dict(inserted_records)
        return_data['updatedRecords'] = DatabaseUtils.records_to_dict(update_records)
        return return_data

    def convert_raw_into_ticket_entity(self, raw_data):
        raw_data = raw_data['data']
        # Mapping raw_data into TicketSchema
        ticket_data = []
        for raw_data_item in raw_data:
            try:
                ticket_data_item = {
                    'full_name': raw_data_item['full_name'],
                    'description': raw_data_item['description'],
                    'stock_operator': raw_data_item['exchange'],
                    'type': raw_data_item['type'],
                    'symbol': raw_data_item['code'],
                    'security_name': raw_data_item['securityName']
                }
                ticket_data.append(ticket_data_item)
            except Exception as exception:
                code = status.HTTP_500_INTERNAL_SERVER_ERROR
                message = TicketMessageConst.CONVERT_FAIL
                error \
                    = BaseExceptionResponse.ErrorObject(body_code=code,
                                                        message=message,
                                                        location_type=self.convert_raw_into_ticket_entity.__qualname__,
                                                        location=str(exception))
                raise BaseExceptionResponse(http_code=code, body_code=code, message=message, errors=[error])
        return ticket_data
