import uuid
from sqlalchemy.dialects.postgresql import UUID

from internal.db.psql import db


class HistoryResolution1Model(db.Model):
    __tablename__ = 'historyResolution1'

    id = db.Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True)
    t = db.Column('t', db.Integer, nullable=False)
    c = db.Column('c', db.Float, nullable=False)
    o = db.Column('o', db.Float, nullable=False)
    h = db.Column('h', db.Float, nullable=False)
    l = db.Column('l', db.Float, nullable=False)
    v = db.Column('v', db.Integer, nullable=False)
    symbol = db.Column('symbol', db.String, db.ForeignKey('ticket.symbol'), nullable=False)

    __table_args__ = (
        db.Index(
            'uixTSymbol',
            't',
            'symbol',
            unique=True
        ),
    )

    def __init__(self, t, c, o, h, l, v, symbol, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.pop('id')
        if len(kwargs) > 0:
            raise TypeError("%r is an invalid keyword argument for %s" % (kwargs.keys(), self.__name__))
        self.t = t
        self.c = c
        self.o = o
        self.h = h
        self.l = l
        self.v = v
        self.symbol = symbol
