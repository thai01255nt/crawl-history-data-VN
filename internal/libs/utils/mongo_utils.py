import uuid
import enum


class MongoUtils:

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
        if not PostgresUtils.is_valid_object_id(value):
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
            element = PostgresUtils.record_to_dict(record, ignore_fields=ignore_fields)
            result.append(element)
        return result

    # @staticmethod
    # def record_to_dict(record, ignore_fields=()):
    #     result = {}
    #     attributes = record.__mapper__.attrs.keys()
    #     for attr in attributes:
    #         field_name = record.__mapper__.attrs[attr].columns[0].key
    #         if field_name in ignore_fields:
    #             continue
    #         elif isinstance(getattr(record, attr), uuid.UUID):
    #             result[field_name] = getattr(record, attr).__str__()
    #         elif getattr(record, attr).__class__.__class__ is enum.EnumMeta:
    #             result[field_name] = getattr(record, attr).value
    #         else:
    #             result[field_name] = getattr(record, attr)
    #     return result
