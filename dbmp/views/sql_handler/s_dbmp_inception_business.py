#-*- coding:utf-8 -*-

from django.db import connection

class SQLDbmpInceptionBusiness(object):

    def __ini__(self):
        pass

    def find_businesses_by_inception_record_id(self, inception_record_id):
        """获得审核数据库信息"""
        if not inception_record_id:
            return None

        sql = """
            SELECT did.inception_database_id,
                did.inception_record_id,
                did.mysql_database_id,
                did.execute_status,
                dmd.name,
                dmi.host,
                dmi.port
            FROM dbmp_inception_database AS did
            INNER JOIN dbmp_mysql_database AS dmd
                ON did.mysql_database_id = dmd.mysql_database_id
                AND did.inception_record_id = {inception_record_id}
            INNER JOIN dbmp_mysql_instance AS dmi
                ON dmd.mysql_instance_id = dmi.mysql_instance_id
        """.format(inception_record_id = inception_record_id)

        cursor = connection.cursor()
        cursor.execute(sql)
        results = self._dict_fetchall(cursor)
        return results

    def _dict_fetchone(self, cursor):
        "转化所有的行为dict"
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))

    def _dict_fetchall(self, cursor):
        "转化所有的行为dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
