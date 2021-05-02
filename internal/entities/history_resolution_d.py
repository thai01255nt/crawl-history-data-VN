import datetime
from internal.db.mongo import db
from internal.common.consts.database_consts import DbAliasType


class HistoryResolutionD(db.Document):
    symbol = db.StringField(required=True, db_field='symbol')
    date = db.StringField(required=True, db_field='date')
    time = db.StringField(required=True, db_field='time')
    stock_operator = db.StringField(required=True, db_field='stockOperator')
    type = db.StringField(required=True, db_field='type')
    basic_price = db.FloatField(required=True, db_field='basicPrice')
    ceiling_price = db.FloatField(required=True, db_field='ceilingPrice')
    floor_price = db.FloatField(required=True, db_field='floorPrice')
    open = db.FloatField(required=True, db_field='open')
    high = db.FloatField(required=True, db_field='high')
    low = db.FloatField(required=True, db_field='low')
    close = db.FloatField(required=True, db_field='close')
    average = db.FloatField(required=True, db_field='average')
    adjust_open = db.FloatField(required=True, db_field='adjustOpen')
    adjust_high = db.FloatField(required=True, db_field='adjustHigh')
    adjust_low = db.FloatField(required=True, db_field='adjustLow')
    adjust_close = db.FloatField(required=True, db_field='adjustClose')
    adjust_average = db.FloatField(required=True, db_field='adjustAverage')
    normal_volume = db.FloatField(required=True, db_field='normalVolume')
    normal_value = db.FloatField(required=True, db_field='normalValue')
    put_through_volume = db.FloatField(required=True, db_field='putThroughVolume')
    put_through_value = db.FloatField(required=True, db_field='putThroughValue')
    change = db.FloatField(required=True, db_field='change')
    adjust_change = db.FloatField(required=True, db_field='adjustChange')
    percentage_change = db.FloatField(required=True, db_field='percentageChange')

    created_at = db.DateTimeField(required=True, db_field="createdAt")
    updated_at = db.DateTimeField(required=True, db_field="updatedAt")

    meta = {
        "db_alias": DbAliasType.API_HISTORY_DATA_VN,
        "collection": "historyResolutionD",
        'indexes': [
            {'fields': ('date', 'symbol'), 'unique': True},
        ],
    }

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    def as_camel_case_dict(self):
        return {
            'symbol': self.symbol,
            'date': self.date,
            'time': self.time,
            'stockOperator': self.stock_operator,
            'type': self.type,
            'basicPrice': self.basic_price,
            'ceilingPrice': self.ceiling_price,
            'floorPrice': self.floor_price,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'average': self.average,
            'adjustOpen': self.adjust_open,
            'adjustHigh': self.adjust_high,
            'adjustLow': self.adjust_low,
            'adjustClose': self.adjust_close,
            'adjustAverage': self.adjust_average,
            'normalVolume': self.normal_volume,
            'normalValue': self.normal_value,
            'putThroughVolume': self.put_through_volume,
            'putThroughValue': self.put_through_value,
            'change': self.change,
            'adjustChange': self.adjust_change,
            'percentageChange': self.percentage_change,

            'createdAt': str(self.created_at),
            'updatedAt': str(self.updated_at)
        }
