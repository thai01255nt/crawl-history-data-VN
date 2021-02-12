import json
import requests


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
