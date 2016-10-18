#-*- coding:utf-8 -*-

from django.db import connection

class SQLDbmpInceptionBusinessDetail(object):

    def __ini__(self):
        pass

    def get_business_detail_by_id(self, inception_business_detail_id):
        """获得审核数据库信息
        DbmpInceptionDatabase, DbmpInceptionRecord, DbmpInceptionIncetance
        DbmpMysqlDatabase, DbmpMysqlInstance 信息
        """
        if not inception_business_detail_id:
            return None

        sql = """
            SELECT dibd.inception_business_detail_id,
                dibd.inception_record_id,
                dibd.mysql_database_id,
                dibd.execute_status,
                dir.sql_text,
                dir.charset,
                INET_NTOA(dii.host) AS inc_host,
                dii.port AS inc_port,
                dmd.name AS db_name,
                INET_NTOA(dmi.host) AS mysql_host,
                dmi.port AS mysql_port,
                dmi.username AS mysql_username,
                dmi.password AS mysql_password
            FROM dbmp_inception_business_detail AS dibd
            INNER JOIN dbmp_inception_record AS dir
                ON dibd.inception_record_id = dir.inception_record_id
                AND dibd.inception_business_detail_id = {inception_business_detail_id}
            INNER JOIN dbmp_inception_instance AS dii
                ON dir.inception_instance_id = dii.inception_instance_id
            INNER JOIN dbmp_mysql_database AS dmd
                ON dibd.mysql_database_id = dmd.mysql_database_id
            INNER JOIN dbmp_mysql_instance AS dmi
                ON dmd.mysql_instance_id = dmi.mysql_instance_id
        """.format(inception_business_detail_id = inception_business_detail_id)

        cursor = connection.cursor()
        cursor.execute(sql)
        results = self._dict_fetchone(cursor)
        return results

    def find_need_inception_detail_by_business_id(self, inception_business_id):
        """获得审核业务组明细信息"""
        if not inception_business_id:
            return None

        sql = """
            SELECT dibd.inception_business_detail_id,
                dibd.mysql_business_id,
                dibd.execute_status,
                dmd.name AS db_name,
                INET_NTOA(dmi.host) AS host,
                dmi.port,
                dmb.name AS business_name
            FROM dbmp_inception_business_detail AS dibd
            INNER JOIN dbmp_mysql_business AS dmb
                ON dibd.mysql_business_id = dmb.mysql_business_id
                AND dibd.inception_business_id = 1
                AND dibd.execute_status <> 2
            INNER JOIN dbmp_mysql_database AS dmd
                ON dibd.mysql_database_id = dmd.mysql_database_id
            INNER JOIN dbmp_mysql_instance AS dmi
                ON dmd.mysql_instance_id = dmi.mysql_instance_id
        """.format(inception_business_id = inception_business_id)

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
