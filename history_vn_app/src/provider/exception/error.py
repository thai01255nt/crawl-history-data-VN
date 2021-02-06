class ApiError:
    def __init__(self, code, message, location_type, location):
        self.code = code
        self.message = message
        self.location_type = location_type
        self.location = location
