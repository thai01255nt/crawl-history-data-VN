from .base_exception import BaseException
from ...common.consts.response_consts import ResponseCode, ResponseBodyCode


class SystemException(BaseException):
    def __init__(self,
                 http_code=ResponseCode.INTERNAL_SERVER_ERROR,
                 body_code=ResponseBodyCode.INTERNAL_SERVER_ERROR['UNKNOWN'],
                 message=ResponseBodyCode.INTERNAL_SERVER_ERROR['UNKNOWN'],
                 errors=None):
        super().__init__(http_code=http_code, body_code=body_code, message=message, errors=errors)
