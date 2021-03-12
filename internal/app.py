from flask import (
    Flask,
    make_response
)
from flask_cors import CORS
from flask_restx import Api
from internal.libs.utils.config_utils import get_system_config
from internal.libs.http_handlers.response.base import BaseResponse
from internal.libs.http_handlers.response.response_utils import ResponseUtils
from internal.libs.http_handlers.exception.response_exception import ResponseException

PREFIX = "/crawls/v1"

app = Flask(__name__)
CORS(app)

config = {
    # App config
    'FLASK_PORT': 'FLASK_PORT',
    'FLASK_ENV': 'FLASK_ENV',
    'FLASK_DEBUG': 'FLASK_DEBUG',

    # Database config
    'MONGODB_URI': 'MONGODB_URI'
}

app.config["SYS"] = get_system_config(config)
app.config["SYS"]['FLASK_DEBUG'] = int(app.config["SYS"]['FLASK_DEBUG'])
api = Api(app, prefix=PREFIX)


@api.representation('application/json')
def represent(data, code, headers=None):
    response_body = data
    if issubclass(data.__class__, BaseResponse):
        response_body = data.to_dict()
    resp = make_response(response_body, code)
    resp.headers.extend(headers or {})
    return resp


@api.errorhandler(ResponseException)
def handle_responese_exception(exception):
    return ResponseUtils.parse_response_from_exception(exception, debug=app.config["SYS"]['FLASK_DEBUG'])


@api.errorhandler(Exception)
def handle_system_exception(exception):
    return ResponseUtils.parse_response_from_exception(exception, debug=app.config["SYS"]['FLASK_DEBUG'])
