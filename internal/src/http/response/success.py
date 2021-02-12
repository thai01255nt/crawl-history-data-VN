from .base import BaseResponse


class SuccessResponse(BaseResponse):
    def __init__(self, code=None, message=None, data=None):
        super().__init__(code=code, message=message, data=data)
