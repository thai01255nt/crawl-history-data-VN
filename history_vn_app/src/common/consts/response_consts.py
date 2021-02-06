class ErrorMessage:
    VALIDATION_FAILED = "Validation failed"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    NOT_FOUND = "Not found"
    CONFLICT = "Conflict"
    INVALID_OBJECT_ID = "Invalid object id"


class LocationType:
    BODY = "body"
    QUERY = "query"


class ResponseCode:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    VALIDATION_FAILED = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class ResponseBodyCode:
    COMMON = {
        "OK": "ok"
    }
    INTERNAL_SERVER_ERROR = {
        "UNKNOWN": "unknown error"
    }
