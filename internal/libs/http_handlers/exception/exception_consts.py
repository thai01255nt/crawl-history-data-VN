class ExceptionMessage:
    VALIDATION_FAILED = "Validation failed"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    NOT_FOUND = "Not found"
    CONFLICT = "Conflict"
    INVALID_OBJECT_ID = "Invalid object id"
    INTERNAL_SERVER_ERROR = "Unknown internal server error"


class ExceptionLocationType:
    BODY = "body"
    QUERY = "query"
