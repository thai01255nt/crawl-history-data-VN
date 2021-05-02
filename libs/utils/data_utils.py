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
        except Exception:
            return False

    # @staticmethod
    # def dict_to_dict(dictionary, ignore_fields=()):
    #     result = {}
    #     for field_name, field_value in dictionary.items():
    #         if field_name in ignore_fields:
    #             continue
    #         elif isinstance(field_value, uuid.UUID):
    #             result[field_name] = str(field_value)
    #         elif isinstance(field_value, dict):
    #             result[field_name] = DataUtils.dict_to_dict(field_value)
    #         elif isinstance(field_value, list):
    #             result[field_name] = list(map(lambda x: DataUtils.dict_to_dict(x), field_value))
    #         else:
    #             result[field_name] = field_value
    #     return result
    #
