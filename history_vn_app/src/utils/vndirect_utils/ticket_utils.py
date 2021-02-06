import requests
import json
import datetime


class HOSEUtils:
    list_symbol = []


class HNXUtils:
    list_symbol = []


class UPCOMUtils:
    list_symbol = []


class LIST_STOCK_OPERATOR:
    HOSE = HOSEUtils
    HNX = HNXUtils
    UPCOM = UPCOMUtils

    @staticmethod
    def __all_values__():
        return [getattr(LIST_STOCK_OPERATOR, attr) for attr in dir(LIST_STOCK_OPERATOR) if not attr.startswith('__')]

    @staticmethod
    def __all_keys__():
        return [attr for attr in dir(LIST_STOCK_OPERATOR) if not attr.startswith('__')]


def update_list_symbols():
    # Get stock operator Utils from LIST_STOCK_OPERATOR and reset list_symbol
    print('[INFO] [RESET] Reset list_symbol.')
    for stock_operator_utils in LIST_STOCK_OPERATOR.__all_values__():
        stock_operator_utils.list_symbol = []

    # Request from SSI and update list symbol
    print('[INFO] [INIT] Update list symbol from SSI.')
    response_dict = json.loads(requests.get('https://iboard.ssi.com.vn/dchart/api/1.1/defaultAllStocks').content)
    datas = response_dict['data']
    for data in datas:
        stock_operator = data['exchange']
        if stock_operator in LIST_STOCK_OPERATOR.__all_keys__():
            getattr(LIST_STOCK_OPERATOR, stock_operator).list_symbol.append(data['code'])
    return


# --------------------------
class TicketUtils:
    @staticmethod
    def get_all_ssi_datas():
        response_dict = json.loads(requests.get('https://iboard.ssi.com.vn/dchart/api/1.1/defaultAllStocks').content)
        raw_datas = response_dict['data']
        return TicketUtils.convert_raw_into_schema(raw_datas=raw_datas)

    @staticmethod
    def convert_raw_into_schema(raw_datas):
        # Mapping raw_data into TicketSchema
        ticket_datas = []
        for raw_data in raw_datas:
            ticket_data = {
                'fullName': raw_data['full_name'],
                'description': raw_data['description'],
                'stockOperator': raw_data['exchange'],
                'type': raw_data['type'],
                'symbol': raw_data['code'],
                'securityName': raw_data['securityName']
            }
            ticket_datas.append(ticket_data)
        return ticket_datas
