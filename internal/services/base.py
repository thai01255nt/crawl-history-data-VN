from flask_api import status

from libs.response.exception.base_exception import BaseExceptionResponse
from libs.response.exception.exception_consts import ExceptionMessage

from internal.repositories.base import BaseRepository


class BaseService:
    def __init__(self, repo):
        self.repo: BaseRepository = repo

    def insert_record(self, record_data):
        record = self.repo.insert_record(record_data)
        return record

    def insert_records(self, records_data):
        record = self.repo.insert_records(records_data)
        return record

    def get_record_by_id(self, record_id):
        record = self.repo.get_record_by_id(record_id)
        if record is None:
            code = status.HTTP_404_NOT_FOUND
            error = BaseExceptionResponse.ErrorObject(body_code=code,
                                                      message=ExceptionMessage.NOT_FOUND,
                                                      location_type=self.get_record_by_id.__qualname__,
                                                      location=record_id)
            raise BaseExceptionResponse(http_code=code,
                                        body_code=code,
                                        message=error.message,
                                        errors=[error])
        return record

    def delete_record_by_id(self, record_id):
        record = self.get_record_by_id(record_id=record_id)
        record = self.repo.delete_record(record)
        return record

    def update_record_by_id(self, record_id, update_data):
        record = self.repo.get_record_by_id(record_id=record_id)
        record = self.repo.update_record(record=record, update_data=update_data)
        return record

    def update_records_by_id(self, update_data):
        record = self.repo.update_records_by_id(update_data=update_data)
        return record

    def get_all_records(self):
        records = self.repo.get_all_records()
        return records
