from sqlalchemy.sql.expression import (
    bindparam,
    update
)
from ...db.psql import db


class BaseDAO():
    def __init__(self, model):
        self.model = model

    def add(self, data):
        schema_object = self.model(**data)
        db.session.add(schema_object)
        db.session.commit()
        return schema_object

    def get(self, id):
        record = db.session.query(self.model).get(id)
        return record

    def get_all(self):
        records = db.session.query(self.model).all()
        return records

    def update(self, id, data):
        updated_record = db.session.query(self.model).filter_by(id=id).update(**data)
        return updated_record

    def add_all(self, records):
        if len(records) == 0:
            return []
        schema_objects = [self.model(**record) for record in records]
        db.session.add_all(schema_objects)
        db.session.commit()
        return schema_objects

    def update_all(self, records):
        if len(records) == 0:
            return []
        bind = {}
        for key in self.model.__table__.columns.keys():
            if key == 'id':
                continue
            bind[key] = key
        replace_field = f'{self.model.__table__.key}_id'
        list_id = []
        for record in records:
            record[replace_field] = record['id']
            list_id.append(record['id'])
        sql_statement = update(self.model).where(self.model.id == bindparam(replace_field)).values(bind).returning(
            self.model.id)
        db.engine.execute(sql_statement, records)
        updated_records = db.session.query(self.model).filter(self.model.id.in_(list_id)).all()
        return updated_records

