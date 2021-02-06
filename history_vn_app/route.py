from flask import make_response
from flask_restx import Api

from history_vn_app.db.psql import db
from history_vn_app.app import app
from history_vn_app.src.utils.response_utils import ResponseUtils
from history_vn_app.src.provider.exception.response_exception import ResponseException
from history_vn_app.src.provider.exception.system_exception import SystemException
from history_vn_app.src.http.response.base import BaseResponse

from history_vn_app.src.http.controller.ticket import TicketUpdateNewestController

api = Api(app, prefix="/api.dev.vn/crawls/v1")


@api.representation('application/json')
def represent(data, code, headers=None):
    response_body = data
    if issubclass(data.__class__, BaseResponse):
        response_body = data.to_dict()
    resp = make_response(response_body, code)
    resp.headers.extend(headers or {})
    return resp


@api.errorhandler(ResponseException)
def handle_custom_exception(exception):
    return ResponseUtils.parse_response_from_exception(exception)


@api.errorhandler(SystemException)
def handle_custom_exception(exception):
    return ResponseUtils.parse_response_from_exception(exception)


@api.errorhandler(Exception)
def handle_custom_exception(exception):
    return ResponseUtils.parse_response_from_exception(exception)


api.add_resource(TicketUpdateNewestController, '/tickets/update-newest')

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run('0.0.0.0', app.config["SYS"]["port"]["port"])
