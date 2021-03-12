from internal.db.mongo import db


class RawDAO():

    def get_for_create_destination(self, meta_id):
        meta_id = str(meta_id)
        sql_statement = f'''
            SELECT
            m."metaName" AS name,
            d."fieldName" AS field_name, d."dataType" AS data_type, d.opt AS opt
            FROM meta m
            LEFT JOIN destination d
            ON m.id = d."metaId"
            LEFT JOIN workspace w ON m."workspaceId" = w.id
            WHERE m.id = '{meta_id}'
            ;
        '''

        result_objects = db.engine.execute(sql_statement)
        results = [list(row) for row in result_objects]
        return results
