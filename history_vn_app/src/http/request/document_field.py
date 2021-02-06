from ...common.consts.database_consts import FieldType
from ...utils.data_utils import DataUtils
from ...utils.postgres_utils import PostgresUtils


class DocumentField:
    def __init__(
            self,
            required=False,
            field_type=FieldType.STRING,
            value_sets=None,
            editable=False,
            default=None,
    ):
        self.required = required
        self.field_type = field_type
        self.value_sets = value_sets
        self.editable = editable
        self.default = default

    def is_valid_value(self, value):
        required = self.required

        if not required:
            return not DataUtils.is_has_value(value) or self._is_valid_not_none_value(value)
        else:
            return DataUtils.is_has_value(value) and self._is_valid_not_none_value(value)

    def _is_valid_not_none_value(self, value):
        field_type = self.field_type
        value_sets = self.value_sets
        if field_type == FieldType.DICT:
            if DataUtils.is_dict_type(value):
                if len(value.keys()) > 0:
                    return True
            return False
        elif field_type == FieldType.OID:
            return PostgresUtils.is_valid_object_id(value)
        elif field_type == FieldType.NUMBER:
            return DataUtils.is_valid_common_number(value)
        elif field_type == FieldType.STRING:
            return DataUtils.is_valid_common_string(value)
        elif field_type == FieldType.SELECT:
            return value in value_sets
        elif field_type == FieldType.LIST:
            return isinstance(value, list)
        elif field_type == FieldType.BOOL:
            return isinstance(value, bool)
