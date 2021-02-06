from .data_utils import DataUtils
from ..common.consts.response_consts import ResponseCode, LocationType
from ..provider.exception.error import ApiError
from ..provider.exception.response_exception import ResponseException


class RequestModelUtils:
    @staticmethod
    def get_all_field_of_schema(request_model):
        list_key = list(request_model.keys())
        return list(list_key)

    @staticmethod
    def parse_data_for_insert(request_model, data):
        RequestModelUtils.validate_data_for_insert(request_model, data)
        result = RequestModelUtils.parse_data_for_insert_without_validate(request_model=request_model, data=data)
        return result

    @staticmethod
    def validate_data_for_insert(request_model, data):
        errors = []
        if not data:
            for field_name, field_configs in request_model.items():
                if field_configs.required:
                    errors.append(ApiError(ResponseCode.VALIDATION_FAILED, f"Invalid {field_name}", LocationType.BODY,
                                           f"/{field_name}"))
        else:
            for field_name, field_configs in request_model.items():
                value = DataUtils.get_value_from_dict_by_key(data, field_name)
                is_valid_value = field_configs.is_valid_value(value)
                if not is_valid_value:
                    errors.append(ApiError(ResponseCode.VALIDATION_FAILED, f"Invalid {field_name}", LocationType.BODY,
                                           f"/{field_name}"))
        if len(errors):
            raise ResponseException(http_code=ResponseCode.VALIDATION_FAILED, errors=errors)

    @staticmethod
    def parse_data_for_insert_without_validate(request_model, data):
        result = {}
        if not data:
            return result
        for field_name, field_configs in request_model.items():
            value = DataUtils.get_value_from_dict_by_key(data, field_name)
            default = field_configs.default
            if DataUtils.is_has_value(value):
                result[field_name] = value
            elif DataUtils.is_has_value(default):
                result[field_name] = default
        return result

    @staticmethod
    def parse_data_for_update(request_model, data):
        RequestModelUtils.validate_data_for_update(request_model, data)
        result = RequestModelUtils.parse_data_for_update_without_validate(request_model=request_model, data=data)
        return result

    @staticmethod
    def validate_data_for_update(request_model, data):
        errors = []
        if not data:
            return
        for field_name, field_configs in request_model.items():
            value = DataUtils.get_value_from_dict_by_key(data, field_name)
            is_valid_value = field_configs.is_valid_value(value)
            if DataUtils.is_has_value(value) and not is_valid_value:
                errors.append(ApiError(ResponseCode.VALIDATION_FAILED, f"Invalid {field_name}", LocationType.BODY,
                                       f"/{field_name}"))
        if len(errors):
            raise ResponseException(http_code=ResponseCode.VALIDATION_FAILED, errors=errors)

    @staticmethod
    def parse_data_for_update_without_validate(request_model, data):
        result = {}
        if not data:
            return result
        for field_name, field_configs in request_model.items():
            value = DataUtils.get_value_from_dict_by_key(data, field_name)
            if field_name == "phone" and value == '' or field_name == "dob" and value == '':
                result[field_name] = value
            if DataUtils.is_has_value(value) and field_configs.editable:
                result[field_name] = value
        return result
