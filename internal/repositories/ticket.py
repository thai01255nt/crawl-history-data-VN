from internal.entities.ticket import Ticket
from internal.repositories.base import BaseRepository


class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__(Ticket)
        self.tick_entity = Ticket

    def get_by_symbol(self, symbol):
        records = self.tick_entity.objects(symbol=symbol)
        return records
