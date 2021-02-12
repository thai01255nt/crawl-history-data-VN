import uuid
import enum
import pandas as pd

TEXT_MAX_BYTE = 1024


class DataUtils:
    @staticmethod
    def is_has_value(value):
        return value is not None

    @staticmethod
    def is_dict_type(value):
        return type(value) is dict

    @staticmethod
    def is_valid_common_string(value):
        value_length = len(value.encode('utf-8'))
        return value_length <= TEXT_MAX_BYTE

    @staticmethod
    def is_valid_common_number(value):
        try:
            return pow(-2, 31) < int(value) < pow(2, 31) - 1
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def record_to_dict(record, ignore_fields=()):
        result = {}
        attributes = record.__mapper__.attrs.keys()
        for attr in attributes:
            field_name = record.__mapper__.attrs[attr].columns[0].key
            if field_name in ignore_fields:
                continue
            elif isinstance(getattr(record, attr), uuid.UUID):
                result[field_name] = getattr(record, attr).__str__()
            elif getattr(record, attr).__class__.__class__ is enum.EnumMeta:
                result[field_name] = getattr(record, attr).value
            else:
                result[field_name] = getattr(record, attr)
        return result

    @staticmethod
    def records_to_dict(records, ignore_fields=()):
        result = []
        for record in records:
            element = DataUtils.record_to_dict(record, ignore_fields=ignore_fields)
            result.append(element)
        return result

    @staticmethod
    def records_to_dataframe(records, ignore_fields=()):
        if len(records) == 0:
            return None
        result = []
        # Init field
        for record in records:
            element = DataUtils.record_to_dict(record, ignore_fields=ignore_fields)
            # fetch dict to list
            result.append(list(element.values()))
        # first record for the columns
        result = pd.DataFrame(result, columns=DataUtils.record_to_dict(records[0], ignore_fields=ignore_fields).keys())
        return result

    @staticmethod
    def dict_to_dict(dictionary, ignore_fields=()):
        result = {}
        for field_name, field_value in dictionary.items():
            if field_name in ignore_fields:
                continue
            elif isinstance(field_value, uuid.UUID):
                result[field_name] = str(field_value)
            elif isinstance(field_value, dict):
                result[field_name] = DataUtils.dict_to_dict(field_value)
            elif isinstance(field_value, list):
                result[field_name] = list(map(lambda x: DataUtils.dict_to_dict(x), field_value))
            else:
                result[field_name] = field_value
        return result

    @staticmethod
    def get_value_from_dict_by_key(object_data, key):
        result = object_data[key] if key in object_data else None
        return result

    @staticmethod
    def get_value_from_request_args_by_key(request_args, key):
        result = request_args.get(key) if key in request_args else None
        return result
