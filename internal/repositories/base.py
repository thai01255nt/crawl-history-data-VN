from pymongo import UpdateOne
from internal.db.mongo import db


class BaseRepository:
    def __init__(self, entity):
        self.entity: db.Document = entity

    def insert_record(self, record_data):
        record = self.entity(**record_data)
        inserted_record = record.save()
        return inserted_record

    def insert_records(self, records_data):
        inserted_records = self.entity.objects.insert([self.entity(**record_data) for record_data in records_data])
        return inserted_records

    def delete_record(self, record):
        record.delete()
        return record

    def update_record(self, record, update_data):
        for update_field in update_data.keys():
            setattr(record, update_field, update_data[update_field])
        record = record.save()
        return record

    def update_records_by_id(self, update_data):
        bulk_operations = []
        for data in update_data:
            bulk_operations.append(
                UpdateOne({'_id': data['_id']}, {'$set': update_data})
            )
        if bulk_operations:
            records = self.entity._get_collection().bulk_write(bulk_operations, ordered=False)
        else:
            return None
        return records

    def get_record_by_id(self, record_id):
        record = self.entity.objects(id=record_id).first()
        return record

    def get_all_records(self):
        records = self.entity.objects({})
        return records

# class OperatorRepository:
#     def __init__(self, entity):
#         self.entity = entity
#
#     def get_max_record_by_field(self, field):
#         record = self.entity.objects.order_by(field).limit(-1).first()
#         return record
