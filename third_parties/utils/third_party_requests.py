import requests
import json
from flask_api import status

from third_parties.consts import (
    ThirdPartyMessageConsts,
    ThirdPartyConsts
)
from libs.response.exception.base_exception import BaseExceptionResponse


class ThirdPartyRequest:
    @staticmethod
    def get(url, params=()):
        try:
            response = requests.get(url, params=params)
            results = json.loads(response.content)
        except Exception as exception:
            http_code = status.HTTP_503_SERVICE_UNAVAILABLE
            body_code = status.HTTP_503_SERVICE_UNAVAILABLE
            message = ThirdPartyMessageConsts.SERVICE_UNAVAILABLE
            location_type = ThirdPartyConsts.LOCATION_TYPE + ThirdPartyRequest.get.__qualname__ + url
            location = params
            error_object = BaseExceptionResponse.ErrorObject(body_code=body_code,
                                                             message=str(exception),
                                                             location_type=location_type,
                                                             location=location)
            raise BaseExceptionResponse(http_code=http_code,
                                        body_code=body_code,
                                        message=message,
                                        errors=[error_object])
        return results
