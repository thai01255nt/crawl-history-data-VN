from validator import validate
from internal.src.http.request.custom_validator import CustomValidator


class AddDestinationValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            'metaId': ['required', CustomValidator.ObjectId()],
            'fieldName': 'required|string',
            'dataType': 'required|string',
            'opt': 'string'
        }
        return rules

    @staticmethod
    def validate(payload: dict):
        rules = AddDestinationValidator.__get_rules()
        return validate(payload, rules, return_info=True)
