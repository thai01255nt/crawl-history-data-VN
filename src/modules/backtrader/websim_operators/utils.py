import numpy as np


class WebsimOperatorUtils:
    @staticmethod
    def validate_dimension(data: np.ndarray, ndim: int):
        if len(data.shape) != ndim:
            raise Exception(f"Required dimension number is {ndim}")
