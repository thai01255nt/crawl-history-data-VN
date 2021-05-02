import datetime
from internal.db.mongo import db
from internal.common.consts.database_consts import DbAliasType


class HistoryResolution1(db.Document):
    t = db.IntField(required=True, db_field='t')
    c = db.FloatField(required=True, db_field='c')
    o = db.FloatField(required=True, db_field='o')
    h = db.FloatField(required=True, db_field='h')
    l = db.FloatField(required=True, db_field='l')
    v = db.IntField(required=True, db_field='v')
    symbol = db.StringField(required=True, db_field='symbol')

    created_at = db.DateTimeField(required=True, db_field="createdAt")
    updated_at = db.DateTimeField(required=True, db_field="updatedAt")

    meta = {
        "db_alias": DbAliasType.API_HISTORY_DATA_VN,
        "collection": "historyResolution1",
        'indexes': [
            {'fields': ('t', 'symbol'), 'unique': True},
        ],
    }

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    def as_camel_case_dict(self):
        return {
            't': self.t,
            'c': self.c,
            'o': self.o,
            'h': self.h,
            'l': self.l,
            'v': self.v,
            'symbol': self.symbol,
            'createdAt': str(self.created_at),
            'updatedAt': str(self.updated_at)
        }
