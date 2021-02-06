from ...utils.data_utils import DataUtils


class BaseResponse:
    def __init__(self, code=None, message=None, data=None, errors=None):
        self.code = code
        self.message = message
        self.data = data
        self.errors = errors

    def to_dict(self):
        result = {}
        if DataUtils.is_has_value(self.code):
            result["code"] = self.code
        if DataUtils.is_has_value(self.message):
            result["message"] = self.message
        if DataUtils.is_has_value(self.data):
            data = self.data
            result["data"] = data
        if self.errors:
            result["errors"] = [error.__dict__ for error in self.errors]
        return result
