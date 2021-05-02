import pandas as pd
from libs.utils import database_utils


class DatabaseUtils(database_utils.DatabaseUtils):
    @staticmethod
    def records_to_dataframe(records, ignore_fields=()):
        if len(records) == 0:
            return None
        result = []
        # Init field
        for record in records:
            element = DatabaseUtils.record_to_dict(record, ignore_fields=ignore_fields)
            # fetch dict to list
            result.append(list(element.values()))
        # first record for the columns
        result = pd.DataFrame(
            result,
            columns=DatabaseUtils.record_to_dict(records[0], ignore_fields=ignore_fields).keys()
        )
        return result
