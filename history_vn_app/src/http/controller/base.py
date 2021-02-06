from flask import request
from flask_restx import Resource

from ..response.success import SuccessResponse
from ...common.consts.response_consts import ResponseCode
from ...utils.request_model_utils import RequestModelUtils


class BasePostController(Resource):
    def __init__(self, service, request_model):
        self.service = service
        self.request_model = request_model

    def post(self):
        request_body = request.get_json()
        insert_data = self._parse_data_for_post(request_body)
        data = self.service.add(insert_data)
        response_body = SuccessResponse(data=data)
        return response_body, ResponseCode.CREATED

    def _parse_data_for_post(self, data):
        return RequestModelUtils.parse_data_for_insert(request_model=self.request_model, data=data)


class BaseGetController(Resource):
    def __init__(self, service):
        self.service = service

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
