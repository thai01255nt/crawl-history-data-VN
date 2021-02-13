import uuid
from sqlalchemy.dialects.postgresql import UUID

from internal.db.psql import db


class HistoryResolutionDModel(db.Model):
    __tablename__ = 'historyResolutionD'

    id = db.Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True)
    symbol = db.Column('symbol', db.String, db.ForeignKey('ticket.symbol'), nullable=False)
    date = db.Column('date', db.String, nullable=False)
    time = db.Column('time', db.String, nullable=False)
    stock_operator = db.Column('stockOperator', db.String, nullable=False)
    type = db.Column('type', db.String, nullable=False)
    basic_price = db.Column('basicPrice', db.Float, nullable=False)
    ceiling_price = db.Column('ceilingPrice', db.Float, nullable=False)
    floor_price = db.Column('floorPrice', db.Float, nullable=False)
    open = db.Column('open', db.Float, nullable=False)
    high = db.Column('high', db.Float, nullable=False)
    low = db.Column('low', db.Float, nullable=False)
    close = db.Column('close', db.Float, nullable=False)
    average = db.Column('average', db.Float, nullable=False)
    adjust_open = db.Column('adjustOpen', db.Float, nullable=False)
    adjust_High = db.Column('adjustHigh', db.Float, nullable=False)
    adjust_low = db.Column('adjustLow', db.Float, nullable=False)
    adjust_close = db.Column('adjustClose', db.Float, nullable=False)
    adjust_average = db.Column('adjustAverage', db.Float, nullable=False)
    normal_volume = db.Column('normalVolume', db.Float, nullable=False)
    normal_value = db.Column('normalValue', db.Float, nullable=False)
    put_through_volume = db.Column('putThroughVolume', db.Float, nullable=False)
    put_through_value = db.Column('putThroughValue', db.Float, nullable=False)
    change = db.Column('change', db.Float, nullable=False)
    adjust_change = db.Column('adjustChange', db.Float, nullable=False)
    percentage_change = db.Column('percentageChange', db.Float, nullable=False)

    __table_args__ = (
        db.Index(
            'uixDateSymbol',
            'date',
            'symbol',
            unique=True
        ),
    )

    def __init__(self,
                 symbol,
                 date,
                 time,
                 stockOperator,
                 type,
                 basicPrice,
                 ceilingPrice,
                 floorPrice,
                 open,
                 high,
                 low,
                 close,
                 average,
                 adjustOpen,
                 adjustHigh,
                 adjustLow,
                 adjustClose,
                 adjustAverage,
                 normalVolume,
                 normalValue,
                 putThroughVolume,
                 putThroughValue,
                 change,
                 adjustChange,
                 percentageChange,
                 **kwargs):
        if 'id' in kwargs:
            self.id = kwargs.pop('id')
        if len(kwargs) > 0:
            raise TypeError("%r is an invalid keyword argument for %s" % (kwargs.keys(), self.__name__))
        self.symbol = symbol
        self.date = date
        self.time = time
        self.stock_operator = stockOperator
        self.type = type
        self.basic_price = basicPrice
        self.ceiling_price = ceilingPrice
        self.floor_price = floorPrice
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.average = average
        self.adjust_open = adjustOpen
        self.adjust_bigh = adjustHigh
        self.adjust_low = adjustLow
        self.adjust_close = adjustClose
        self.adjust_average = adjustAverage
        self.normal_volume = normalVolume
        self.normal_value = normalValue
        self.put_through_volume = putThroughVolume
        self.put_through_value = putThroughValue
        self.change = change
        self.adjust_change = adjustChange
        self.percentage_change = percentageChange
