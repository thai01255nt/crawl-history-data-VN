from internal.src.utils.postgres_utils import PostgresUtils
from validator.rules import Rule


class CustomValidator:
    class ObjectId(Rule):
        ''' A Class for validating string is valid UUID (POSTGRES ObjectId)'''

        def check(self, arg):
            if not PostgresUtils.is_valid_object_id(arg):
                self.set_error("Invalid object id. Require UUID")
                return False
            return True