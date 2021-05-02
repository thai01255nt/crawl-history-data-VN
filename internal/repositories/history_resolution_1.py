from internal.src.repositories.base import BaseRepository
from internal.src.entities.history_resolution_1 import HistoryResolution1


class HistoryResolution1Repository(BaseRepository):
    def __init__(self):
        super().__init__(HistoryResolution1)
        self.history_resolution_1_entity = HistoryResolution1

    def get_last_timestamp_record_by_symbol(self, symbol):
        record = self.history_resolution_1_entity.objects(symbol=symbol).order_by('t').limit(-1).first()
        return record

    def get_by_symbol(self, symbol):
        records = self.history_resolution_1_entity.objects(symbol=symbol)
        return records
