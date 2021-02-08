from .base import BaseDAO
from ..schema.ticket import TickModel
from ...db.psql import db


class TicketDAO(BaseDAO):
    def __init__(self):
        super().__init__(TickModel)

    def get_by_symbol(self, symbol):
        results = db.session.query(self.model).filter(
            db.and_(self.model.symbol == symbol)
        ).all()
        return results
