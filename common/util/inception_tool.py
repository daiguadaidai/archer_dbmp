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
    def inception_check_only(self, inception_host='127.0.0.1', inception_port = 6669,
                                   mysql_user='root', mysql_password='root',
                                   mysql_host='127.0.0.1', mysql_port=3306, db_name='',
                                   sql_text = '', charset='utf8'):
        """对SQL进行检查不执行"""
    
        sql= """
/*--user={username};--password={password};--host={host};--check=1;--port={port};*/
inception_magic_start;
set names {charset};
use {db_name};
{sql_text}
inception_magic_commit;
        """.format(username = mysql_user,
                   password = mysql_password,
                   host = mysql_host,
                   port = mysql_port,
                   charset = charset,
                   db_name = db_name,
                   sql_text = sql_text)
        logger.info(sql)

        try:
            inception_info = []
            conn=MySQLdb.connect(host = inception_host, port = inception_port,
                                 user ='', passwd = '', db = '')
            cur=conn.cursor()
            ret=cur.execute(sql_text)
            result=cur.fetchall()
            # 获取返回字段
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]

            # 将返回数据构造成dict 类型
            for row in result:
                inception_info.append(zip(field_names, row))

            cur.close()
            conn.close()

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
