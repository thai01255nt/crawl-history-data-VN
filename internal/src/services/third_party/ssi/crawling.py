import json
import requests


class SsiHistoryResolution1Service:
    base_url = 'https://iboard.ssi.com.vn/dchart/api/history?resolution={resolution}&symbol={symbol}&from={_from}&to={_to}'

    def get_history_resolution_1(self, symbol, _from, _to):
        response = requests.get(self.base_url.format(symbol=symbol, resolution=1, _from=_from, _to=_to))
        results = json.loads(response.content)
        return results

    def convert_second_to_milisecond(self, data):
        for i in range(len(data['t'])):
            data['t'][i] = data['t'][i] * 1000
        return data


class SsiTicketService:

    def get_all_ticket(self):
        response_dict = json.loads(requests.get('https://iboard.ssi.com.vn/dchart/api/1.1/defaultAllStocks').content)
        raw_datas = response_dict['data']
        return self.convert_raw_into_ticket_entity(raw_datas=raw_datas)

    def convert_raw_into_ticket_entity(self,raw_datas):
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
