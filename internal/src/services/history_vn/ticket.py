from .base import BaseService
from internal.src.dao.ticket import TicketDAO
from internal.src.utils.history_utils.ticket_utils import TicketUtils
from internal.src.utils.data_utils import DataUtils
from internal.src.services.exception.response_exception import ResponseException
from internal.src.common.consts.response_consts import ResponseCode
from internal.src.common.consts.message_consts import TicketMessageConst


class TicketService(BaseService):
    def __init__(self):
        super().__init__(TicketDAO())

    def update_newest(self):
        return_data = {
            'insertedRecords': [],
            'updatedRecords': []
        }
        ssi_ticket_datas = TicketUtils.get_all_ssi_datas()
        history_vn_ticket_dataframe = DataUtils.records_to_dataframe(self.dao.get_all())

        if history_vn_ticket_dataframe is None:
            # Insert all
            inserted_records = self.dao.add_all(ssi_ticket_datas)
            return_data['insertedRecords'] = DataUtils.records_to_dict(inserted_records)
            return return_data

        insert_datas = []
        update_datas = []
        for ssi_ticket_data in ssi_ticket_datas:
            history_vn_ticket_rows = history_vn_ticket_dataframe[
                history_vn_ticket_dataframe['symbol'] == ssi_ticket_data['symbol']]
            # Insert if not exists
            if len(history_vn_ticket_rows) == 0:
                insert_datas.append(ssi_ticket_data)
            elif len(history_vn_ticket_rows) > 1:
                raise ResponseException(http_code=ResponseCode.INTERNAL_SERVER_ERROR,
                                        message=TicketMessageConst.TICKET_SYMBOL_DUPLICATED.format(
                                            symbol=ssi_ticket_data['symbol']))
            else:
                # Compare 2 dict
                ssi_ticket_data['id'] = history_vn_ticket_rows.iloc[0]['id']
                if dict(history_vn_ticket_rows.iloc[0]) != ssi_ticket_data:
                    update_datas.append(ssi_ticket_data)
        inserted_records = self.dao.add_all(insert_datas)
        update_records = self.dao.update_all(update_datas)
        return_data['insertedRecords'] = DataUtils.records_to_dict(inserted_records)
        return_data['updatedRecords'] = DataUtils.records_to_dict(update_records)
        return return_data
