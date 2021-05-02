from flask_restx import Resource
from internal.src.services.history_vn.history_resolution_d import HistoryResolutionDService
from internal.src.http.response.success import SuccessResponse
from internal.src.common.consts.response_consts import ResponseCode


class HistoryResolutionDUpdateNewestController(Resource):
    def __init__(self, *kwargs):
        self.service = HistoryResolutionDService()

    def patch(self):
        data = self.service.update_newest_all_symbol()
        response_body = SuccessResponse(data=data)
        return response_body, ResponseCode.CREATED
