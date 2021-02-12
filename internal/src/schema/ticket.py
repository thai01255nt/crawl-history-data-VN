import uuid
from sqlalchemy.dialects.postgresql import UUID

from internal.db.psql import db
import enum


class StockOperatorTypeEnum(enum.Enum):
    HOSE = 'HOSE'
    HNX = 'HNX'
    UPCOM = 'UPCOM'
    FU = 'FU'


class TickModel(db.Model):
    __tablename__ = 'ticket'

    id = db.Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True)
    symbol = db.Column('symbol', db.String, nullable=False, unique=True)
    full_name = db.Column('fullName', db.String, nullable=False)
    description = db.Column('description', db.String, nullable=False)
    stock_operator = db.Column('stockOperator', db.Enum(StockOperatorTypeEnum), nullable=False)
    type = db.Column('type', db.String, nullable=False)
    security_name = db.Column('securityName', db.String, nullable=False)

    def __init__(self, symbol, fullName, description, stockOperator, type, securityName, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.pop('id')
        if len(kwargs) > 0:
            raise TypeError("%r is an invalid keyword argument for %s" % (kwargs.keys(), self.__class__))
        self.symbol = symbol
        self.full_name = fullName
        self.description = description
        self.stock_operator = stockOperator
        self.type = type
        self.security_name = securityName
