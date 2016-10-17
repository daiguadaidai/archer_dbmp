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
            SELECT dib.inception_business_id,
                dib.inception_record_id,
                dib.mysql_business_id,
                dib.execute_status,
                dmb.name,
                dmb.remark
            FROM dbmp_inception_business AS dib
            INNER JOIN dbmp_mysql_business AS dmb
                ON dib.mysql_business_id = dmb.mysql_business_id
                AND dib.inception_record_id = {inception_record_id}
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
