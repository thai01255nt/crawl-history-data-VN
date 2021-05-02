from typing import List
from libs.response.base import BaseResponse


class BaseExceptionResponse(BaseResponse, Exception):
    def __init__(self,
                 http_code: int = None,
                 body_code: int = None,
                 message: str = None,
                 errors: List[BaseResponse.ErrorObject] = None):
        self.http_code = http_code
        self.body_code = body_code
        self.message = message
        self.errors = errors
        super().__init__(http_code=http_code, body_code=body_code, message=message, errors=errors)
