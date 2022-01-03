import os
from datetime import datetime

from src.common.consts import CommonConsts


class YahooConsts:
    PULLED_DATA_NUM = 10
    DATASET_FOLDER = os.path.join(CommonConsts.BASE_FOLDER, "dataset")
    START_TIME = datetime(2018, 1, 1)
    END_TIME = datetime(2021, 11, 30)
