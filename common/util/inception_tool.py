#-*- coding: utf-8 -*-

import sys
import logging
import MySQLdb
import traceback
import time

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('default')

class InceptionTool(object):
    """Inception审核工具"""

    def __init__(self):
        pass

    @classmethod
    def inception_check_only(self, inception_host='127.0.0.1', inception_port=6669,
                            mysql_user='root', mysql_password='root',
                            mysql_host='127.0.0.1', mysql_port=3306,
                            db_name='', sql_text='', charset='utf8'):
        """对SQL进行检查不执行"""
        sql= """
/*--user={username};--password={password};--host={host};--check=1;--enable-remote-backup;--port={port};*/
inception_magic_start;
set names {charset};
use {db_name};
{sql_text}
inception_magic_commit;
        """.format(username = mysql_user,
                   password = mysql_password,
                   host = mysql_host,
                   port = mysql_port,
                   db_name = db_name,
                   sql_text = sql_text,
                   charset = charset)

        logger.info(sql)

        try:
            conn=MySQLdb.connect(host = inception_host,
                                 port = inception_port,
                                 user = '',
                                 passwd = '',
                                 db = '')
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()

            # 获取返回字段
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]

            cur.close()
            conn.close()

            # 将返回数据构造成dict 类型
            logger.info(' | '.join(field_names))
            inception_info = []
            for row in result:
                logger.info( ' | '.join([str(col) for col in row]))
                inception_info.append(dict(zip(field_names, row)))

            return True, inception_info
        except MySQLdb.Error, e:
            err_msg = 'Mysql Error {arg1}: {arg2}'.format(
                                             arg1 = e.args[0],
                                             arg2 = e.args[1])
            logger.error(err_msg)
            return False, err_msg

    @classmethod
    def inception_execute(self, inception_host='127.0.0.1', inception_port=6669,
                            mysql_user='root', mysql_password='root',
                            mysql_host='127.0.0.1', mysql_port=3306,
                            db_name='', sql_text='', charset='utf8'):
        """对SQL进行检查不执行"""
        sql= """
/*--user={username};--password={password};--host={host};--execute=1;--enable-remote-backup;--port={port};*/
inception_magic_start;
set names {charset};
use {db_name};
{sql_text}
inception_magic_commit;
        """.format(username = mysql_user,
                   password = mysql_password,
                   host = mysql_host,
                   port = mysql_port,
                   db_name = db_name,
                   sql_text = sql_text,
                   charset = charset)

        logger.info(sql)

        try:
            conn=MySQLdb.connect(host = inception_host,
                                 port = inception_port,
                                 user = '',
                                 passwd = '',
                                 db = '')
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()

            # 获取返回字段
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]

            cur.close()
            conn.close()

            # 将返回数据构造成dict 类型
            logger.info(' | '.join(field_names))
            inception_info = []
            for row in result:
                logger.info( ' | '.join([str(col) for col in row]))
                inception_info.append(dict(zip(field_names, row)))

            return True, inception_info
        except MySQLdb.Error, e:
            err_msg = 'Mysql Error {arg1}: {arg2}'.format(
                                             arg1 = e.args[0],
                                             arg2 = e.args[1])
            logger.error(err_msg)
            return False, err_msg

def main():
    pass

if __name__ == '__main__':
    main()
