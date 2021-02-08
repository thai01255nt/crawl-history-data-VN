import uuid
from sqlalchemy.dialects.postgresql import UUID

from ...db.psql import db


class HistoryRealtimeModel(db.Model):
    __tablename__ = 'historyRealtime'

    id = db.Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True)
    t = db.Column('t', db.Integer, nullable=False, unique=True)
    c = db.Column('c', db.Float, nullable=False)
    o = db.Column('o', db.Float, nullable=False)
    h = db.Column('h', db.Float, nullable=False)
    l = db.Column('l', db.Float, nullable=False)
    v = db.Column('v', db.Integer, nullable=False)
    ticket_id = db.Column('ticketId', UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)

    def __init__(self, t, c, o, h, l, v, ticketId):
        self.t = t
        self.c = c
        self.o = o
        self.h = h
        self.l = l
        self.v = v
        self.ticket_id = ticketId
