import traceback
from flask_api import status
from internal.libs.http_handlers.response.error import ErrorResponse
from internal.libs.http_handlers.exception.response_exception import ResponseException
from internal.libs.http_handlers.exception.exception_consts import ExceptionMessage


class ResponseUtils:
    @staticmethod
    def parse_response_from_exception(exception, debug=False):
        if isinstance(exception, ResponseException):
            http_code = exception.http_code
            body_code = exception.body_code
            message = exception.message
            errors = exception.errors
            response_body = ErrorResponse(code=body_code, message=message, errors=errors).to_dict()
            return response_body, http_code
        else:
            exception = traceback.TracebackException.from_exception(exception)
            if debug:
                exception = ResponseException(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(exception))
            else:
                exception = ResponseException(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                              message=ExceptionMessage.INTERNAL_SERVER_ERROR)
            raise exception
