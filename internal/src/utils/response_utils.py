import os
import traceback
from internal.src.http.response.error import ErrorResponse
from internal.src.services.exception.system_exception import SystemException
from internal.src.services.exception.response_exception import ResponseException

DEBUG = os.environ.get('FLASK_DEBUG', False)


class ResponseUtils:
    @staticmethod
    def parse_response_from_exception(exception):
        if isinstance(exception, ResponseException) or isinstance(exception, SystemException):
            http_code = exception.http_code
            body_code = exception.body_code
            message = exception.message
            errors = exception.errors
            response_body = ErrorResponse(code=body_code, message=message, errors=errors).to_dict()
        else:
            exception = traceback.TracebackException.from_exception(exception)
            if DEBUG:
                exception = SystemException(message=str(exception))
            else:
                exception = SystemException()
            http_code = exception.http_code
            body_code = exception.body_code
            message = exception.message
            errors = exception.errors
            response_body = ErrorResponse(code=body_code, message=message, errors=errors).to_dict()
        return response_body, http_code
