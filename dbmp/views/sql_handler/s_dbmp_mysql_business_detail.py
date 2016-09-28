#-*- coding:utf-8 -*-

from django.db import connection

class SQLDbmpMysqlBusinessDetail(object):

    def get_business_detail_index(self, mysql_business_id):
        """获得MySQL 业务Detail index 页面的信息"""
        if not mysql_business_id:
            return None

        sql = """
            SELECT dmb.mysql_business_id AS mysql_business_id,
                dmbd.mysql_business_detail_id AS mysql_business_detail_id,
                dmb.name AS business_name,
                dmb.remark AS business_remark,
                dmd.name AS database_name,
                dmi.host AS instance_host,
                dmi.port AS instance_port,
                dmi.remark AS instance_remark
            FROM dbmp_mysql_business AS dmb
            INNER JOIN dbmp_mysql_business_detail AS dmbd
                ON dmb.mysql_business_id = dmbd.mysql_business_id
                AND dmb.mysql_business_id = {mysql_business_id}
            INNER JOIN dbmp_mysql_database AS dmd
                ON dmbd.mysql_database_id = dmd.mysql_database_id
            INNER JOIN dbmp_mysql_instance AS dmi
                ON dmd.mysql_instance_id = dmi.mysql_instance_id
        """.format(mysql_business_id = mysql_business_id)

        cursor = connection.cursor()
        cursor.execute(sql)
        results = self._dict_fetchall(cursor)
        return results

    def get_business_detail_by_id(self, mysql_business_detail_id):
        """通过mysql_business_detail_id(主键) 获得MysqlBusinessDetail数据"""
        
        if not mysql_business_id:
            return None

        sql = """
            SELECT dmb.mysql_business_id AS mysql_business_id,
                dmbd.mysql_business_detail_id AS mysql_business_detail_id,
                dmb.name AS business_name,
                dmb.remark AS business_remark,
                dmd.name AS database_name,
                dmi.host AS instance_host,
                dmi.port AS instance_port,
                dmi.remark AS instance_remark
            FROM dbmp_mysql_business AS dmb
            INNER JOIN dbmp_mysql_business_detail AS dmbd
                ON dmb.mysql_business_id = dmbd.mysql_business_id
                AND dmbd.mysql_business_detail_id = {mysql_business_detail_id}
            INNER JOIN dbmp_mysql_database AS dmd
                ON dmbd.mysql_database_id = dmd.mysql_database_id
            INNER JOIN dbmp_mysql_instance AS dmi
                ON dmd.mysql_instance_id = dmi.mysql_instance_id
        """.format(mysql_business_detail_id = mysql_business_detail_id)

        cursor = connection.cursor()
        cursor.execute(sql)
        results = self._dict_fetchone(cursor)

    def _dict_fetchone(self, cursor):
        "转化所有的行为dict"
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))

    def _dict_fetchall(self, cursor):
        "转化所有的行为dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchone()
        ]
