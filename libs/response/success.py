from libs.response.base import BaseResponse


class SuccessResponse(BaseResponse):
    def __init__(self, http_code: int = None, body_code: int = None, message=None, data=None):
        super().__init__(http_code=http_code, body_code=body_code, message=message, data=data)
