import uuid


class PostgresUtils:

    @staticmethod
    def is_valid_object_id(value):
        if isinstance(value, uuid.UUID):
            return True
        try:
            uuid.UUID(value)
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def string_to_object_id(value):
        if not PostgresUtils.is_valid_object_id(value):
            raise Exception("Invalid object id")
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)
