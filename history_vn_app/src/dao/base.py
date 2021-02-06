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
        db.session.bulk_update_mappings(self.model, records)
        updated_record = db.session.commit()
        print(updated_record)
        return updated_record
