from internal.src.entities.ticket import Tick
from internal.src.repositories.base import BaseRepository


class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__(Tick)
        self.tick_entity = Tick

    def get_by_symbol(self, symbol):
        records = self.tick_entity.objects(symbol=symbol)
        return records
