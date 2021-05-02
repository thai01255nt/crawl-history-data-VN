from typing import List
from libs.utils.data_utils import DataUtils


class BaseResponse:
    class ErrorObject:
        def __init__(self, body_code: int, message: str, location_type: str = None, location = None):
            self.body_code = body_code
            self.message = message
            self.location_type = location_type
            self.location = location

        def to_dict(self):
            result = {}
            if DataUtils.is_has_value(self.body_code):
                result['bodyCode'] = self.body_code
            if DataUtils.is_has_value(self.message):
                result['message'] = self.message
            if DataUtils.is_has_value(self.location_type):
                result['locationType'] = self.location_type
            if DataUtils.is_has_value('location'):
                result['location'] = self.location
            return result

    def __init__(self,
                 http_code: int = None,
                 body_code: int = None,
                 message: str = None,
                 data: List = None,
                 errors: List[ErrorObject] = None):
        self.http_code = http_code
        self.body_code = body_code
        self.message = message
        self.data = data
        self.errors = errors

    def to_dict(self) -> dict:
        result = {}
        if DataUtils.is_has_value(self.body_code):
            result["bodyCode"] = self.body_code
        if DataUtils.is_has_value(self.message):
            result["message"] = self.message
        if self.data:
            result['data'] = self.data
        if self.errors:
            result["errors"] = []
            for error in self.errors:
                result["errors"].append(error.to_dict())
        return result
