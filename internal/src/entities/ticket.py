import datetime
from internal.db.mongo import db
from internal.src.common.consts.database_consts import DbAliasType


class Tick(db.Document):
    symbol = db.StringField(required=True, db_field='symbol', unique=True)
    full_name = db.StringField(required=True, db_field='fullName')
    description = db.StringField(required=True, db_field='description')
    stock_operator = db.StringField(required=True, db_field='stockOperator')
    type = db.StringField(required=True, db_field='type')
    security_name = db.StringField(required=True, db_field='securityName')

    created_at = db.DateTimeField(required=True, db_field="createdAt")
    updated_at = db.DateTimeField(required=True, db_field="updatedAt")

    meta = {"db_alias": DbAliasType.API_HISTORY_DATA_VN, "collection": "tickets"}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)
