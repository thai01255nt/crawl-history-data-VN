from internal.src.entities.history_resolution_d import HistoryResolutionD
from internal.src.repositories.base import BaseRepository


class HistoryResolutionDRepository(BaseRepository):
    def __init__(self):
        super().__init__(HistoryResolutionD)
        self.history_resolution_d_entity = HistoryResolutionD

    def get_last_datetime_record_by_symbol(self, symbol):
        record = self.history_resolution_d_entity.objects(symbol=symbol).order_by('date').limit(-1).first()
        return record

    def get_by_symbol(self, symbol):
        records = self.history_resolution_d_entity.objects(symbol=symbol)
        return records
