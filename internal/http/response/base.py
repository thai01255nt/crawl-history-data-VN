from internal.src.utils.data_utils import DataUtils


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
            result["errors"] = []
            for error in self.errors:
                if hasattr(self.errors[0], '__dict__'):
                    result["errors"].append(error.__dict__)
                else:
                    result["errors"].append(error)
        return result
