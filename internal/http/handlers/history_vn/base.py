from flask import request
from flask_restx import Resource

from internal.src.http.response.success import SuccessResponse
from internal.src.http.response.error import ErrorResponse
from internal.src.common.consts.response_consts import (
    ResponseCode,
    ErrorMessage
)
from internal.src.http.request.request import (
    get_json_body,
    get_param
)
from internal.src.middleware.common import valid_object_id_required


class BasePostController(Resource):
    def __init__(self, service, validator):
        self.service = service
        self.validator = validator

    def post(self):
        _, request_body = get_json_body(request)
        is_valid, _, errors = self.validator.validate(request_body)
        if not is_valid:
            request_body = ErrorResponse(code=ResponseCode.VALIDATION_FAILED, message=ErrorMessage.VALIDATION_FAILED,
                                         errors=[errors])
            return request_body, ResponseCode.VALIDATION_FAILED
        data = self.service.add(request_body)
        response_body = SuccessResponse(data=data)
        return response_body, ResponseCode.CREATED


class BaseGetController(Resource):
    def __init__(self, service):
        self.service = service

    @valid_object_id_required
    def get(self, record_id):
        data = self.service.get(record_id)
        response_body = SuccessResponse(data=data)
        return response_body, ResponseCode.OK


class BaseGetAllController(Resource):
    def __init__(self, service):
        self.service = service

    def get(self):
        datas = self.service.get_all()
        response_body = SuccessResponse(data=datas)
        return response_body, ResponseCode.OK
