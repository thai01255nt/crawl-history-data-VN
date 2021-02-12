from flask_restx import Resource
from internal.src.services.history_vn.ticket import TicketService
from internal.src.http.response.success import SuccessResponse
from internal.src.common.consts.response_consts import ResponseCode


class TicketUpdateNewestController(Resource):
    def __init__(self, *kwargs):
        self.service = TicketService()

    def patch(self):
        data = self.service.update_newest()
        response_body = SuccessResponse(data=data)
        return response_body, ResponseCode.CREATED
