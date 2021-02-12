from internal.src.services.exception.response_exception import ResponseException
from internal.src.common.consts.response_consts import ResponseCode
from internal.src.utils.data_utils import DataUtils


class BaseService:
    def __init__(self, dao):
        self.dao = dao

    def add(self, add_data):
        record = self.dao.add(add_data)
        dict_data = DataUtils.record_to_dict(record)
        return dict_data

    def get(self, id):
        record = self.dao.get(id)
        if not record:
            raise ResponseException(ResponseCode.NOT_FOUND, None, "This record does not exists!")
        dict_data = DataUtils.record_to_dict(record)
        return dict_data

    def get_all(self):
        records = self.dao.get_all()
        dict_datas = DataUtils.records_to_dict(records)
        return dict_datas
