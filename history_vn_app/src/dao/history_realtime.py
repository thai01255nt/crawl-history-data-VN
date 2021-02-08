from sqlalchemy.sql import func

from .base import BaseDAO
from ..schema.history_realtime import HistoryRealtimeModel
from ...db.psql import db


class HistoryRealtimeDAO(BaseDAO):
    def __init__(self):
        super().__init__(HistoryRealtimeModel)

    def get_last_timestamp_by_ticket_id(self, ticket_id):
        result = db.session.query(self.model).filter(self.model.ticket_id == ticket_id).order_by('t').first()
        return result

    def get_by_ticket_id(self, ticket_id):
        results = db.session.query(self.model).filter(
            db.and_(self.model.ticket_id == ticket_id)
        ).all()
        return results
