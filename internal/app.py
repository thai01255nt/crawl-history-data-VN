import os
from flask import (
    Flask,
    make_response
)
from flask_cors import CORS
from flask_restx import Api
from internal.src.utils.config_utils import get_system_config
from internal.src.http.response.base import BaseResponse
from internal.src.utils.response_utils import ResponseUtils
from internal.src.services.exception.response_exception import ResponseException
from internal.src.services.exception.system_exception import SystemException

app = Flask(__name__)
CORS(app)
env = os.getenv("FLASK_ENV")
config_data = get_system_config(env)
app.config["SYS"] = config_data

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
