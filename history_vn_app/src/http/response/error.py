from .base import BaseResponse


class ErrorResponse(BaseResponse):
    def __init__(self, code, message, errors):
        super().__init__(code=code, message=message, data=None, errors=errors)
