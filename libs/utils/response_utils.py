import traceback
from flask_api import status
from libs.response.base import BaseResponse
from libs.response.exception.base_exception import BaseExceptionResponse
from libs.response.exception.exception_consts import ExceptionMessage


class ResponseUtils:
    @staticmethod
    def parse_response_from_exception(exception, debug=False):
        if isinstance(exception, BaseResponse):
            response_body = exception.to_dict()
            return response_body, exception.http_code
        else:
            exception = traceback.TracebackException.from_exception(exception)

            if debug:
                error_object = BaseExceptionResponse.ErrorObject(body_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                 message=str(exception))
                exception_object = BaseExceptionResponse(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                         body_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                         message=ExceptionMessage.INTERNAL_SERVER_ERROR,
                                                         errors=[error_object])
            else:
                exception_object = BaseExceptionResponse(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                         body_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                         message=ExceptionMessage.INTERNAL_SERVER_ERROR)
            raise exception_object
