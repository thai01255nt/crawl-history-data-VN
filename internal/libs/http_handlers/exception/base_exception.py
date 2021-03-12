class BaseException(Exception):
    def __init__(self, http_code=None, body_code=None, message=None, errors=None):
        self.http_code = http_code
        self.body_code = body_code
        self.message = message
        self.errors = errors  # list of ErrorObject or Dict

    class ErrorObject:
        def __init__(self, code, message, location_type, location):
            self.code = code
            self.message = message
            self.location_type = location_type
            self.location = location
