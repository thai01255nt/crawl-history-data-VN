from functools import wraps
from ..utils.postgres_utils import PostgresUtils
from ..provider.exception.response_exception import ResponseException
from ..common.consts.response_consts import (
    ResponseCode,
    ErrorMessage
)


def valid_object_id_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        for key in kwargs.keys():
            record_id = kwargs[key]
            is_valid_object_id = PostgresUtils.is_valid_object_id(record_id)
            if not is_valid_object_id:
                raise ResponseException(http_code=ResponseCode.VALIDATION_FAILED,
                                        message=ErrorMessage.INVALID_OBJECT_ID)
            kwargs[key] = PostgresUtils.string_to_object_id(record_id)
        return f(*args, **kwargs)

    return wrap
