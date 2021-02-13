from sqlalchemy.sql.expression import func

from .base import BaseDAO
from internal.src.schema.history_resolution_1 import HistoryResolution1Model
from internal.db.psql import db


class HistoryResolution1DAO(BaseDAO):
    def __init__(self):
        super().__init__(HistoryResolution1Model)

    def get_last_timestamp_by_symbol(self, symbol):
        # result = db.session.query(self.model).filter(self.model.ticket_id == ticket_id).order_by(
        #     self.model.t.desc()).first()
        # return result
        sql_statement = db.session.query(func.max(HistoryResolution1Model.t)).filter(
            HistoryResolution1Model.symbol == symbol)
        result_objects = db.session.execute(sql_statement)
        results = [list(row) for row in result_objects]
        if len(results) == 0:
            return None
        elif len(results) == 1:
            return results[0][0]
        raise Exception(f'Wrong query in {self.get_last_timestamp_by_symbol} function')

    def get_by_symbol(self, symbol):
        results = db.session.query(self.model).filter(
            db.and_(self.model.symbol == symbol)
        ).all()
        return results
