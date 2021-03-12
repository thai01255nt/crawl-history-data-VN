from .base_exception import BaseException


class ResponseException(BaseException):
    def __init__(self, http_code, body_code=None, message=None, errors=None):
        super().__init__(http_code=http_code, body_code=body_code, message=message, errors=errors)
