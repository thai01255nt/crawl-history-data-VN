import uuid
import enum


class DatabaseUtils:

    @staticmethod
    def is_valid_object_id(value):
        if isinstance(value, uuid.UUID):
            return True
        try:
            uuid.UUID(value)
            return True
        except Exception:
            return False

    @staticmethod
    def string_to_object_id(value):
        if not DatabaseUtils.is_valid_object_id(value):
            raise Exception("Invalid object id")
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)

    @staticmethod
    def record_to_dict(record, ignore_fields=()):
        result = {}
        record_dict: dict = record.as_camel_case_dict()
        for key in record_dict.keys():
            if key in ignore_fields:
                continue
            elif isinstance(record_dict[key], uuid.UUID):
                result[key] = record_dict[key].__str__()
            elif record_dict[key].__class__.__class__ is enum.EnumMeta:
                result[key] = record_dict[key].value
            else:
                result[key] = record_dict[key]
        return result

    @staticmethod
    def records_to_dict(records, ignore_fields=()):
        result = []
        for record in records:
            element = DatabaseUtils.record_to_dict(record, ignore_fields=ignore_fields)
            result.append(element)
        return result
