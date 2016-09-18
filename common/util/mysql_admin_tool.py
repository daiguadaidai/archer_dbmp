#-*- coding: utf-8 -*-

from common.util.ssh_tool import SSHTool

import logging
import MySQLdb
import traceback
import time

logger = logging.getLogger('default')

class MysqlAdminTool(object):
    """执行MySQL获取结果"""

    __mysqladmin = '/usr/local/mysql/bin/mysqladmin'

    def __init__(self):
        pass

    @classmethod
    def mysql_is_alived(self, mysqladmin='', mysql_user='root', 
                              mysql_password='root', mysql_host='127.0.0.1',
                              mysql_port=3306, os_ip='127.0.0.1', os_user='root',
                              os_password='root', os_port=22):
        """判断MySQL是否启动"""
       
        is_alived = False
        if not mysqladmin:
            mysqladmin = __mysqladmin

        # 拼凑 mysqladmin ping 命令
        cmd = '{mysqladmin} -u{user} -p{pwd} -h{host} -P{port} ping'.format(
                                                mysqladmin = mysqladmin,
                                                user = mysql_user,
                                                pwd = mysql_password,
                                                host = mysql_host,
                                                port = mysql_port)
        # ssh 远程执行命令
        is_ok, out_msg, err_msg = SSHTool.ssh_exec_cmd(cmd,
                                                       host = os_ip,
                                                       username = os_user,
                                                       password = os_password,
                                                       port = os_port)
        # 如果命令执行成功并且返回信息是 mysqld is alive就代表MySQL连接成功
        if is_ok and out_msg:
            if out_msg.pop().strip() == 'mysqld is alive':
                is_alived = True 
        return is_alived

    @classmethod
    def mysqld_pids(self, os_ip='127.0.0.1', os_user='root',
                              os_password='root', os_port=22):
        """使用 grep 命令查看含有mysqld的相关pid"""
        cmd = "ps -ef | grep mysqld | grep -v grep | awk '{print $2}'"

        # ssh 远程执行命令
        is_ok, out_msg, err_msg = SSHTool.ssh_exec_cmd(cmd,
                                                       host = os_ip,
                                                       username = os_user,
                                                       password = os_password,
                                                       port = os_port)
        pids = [pid.strip() for pid in out_msg]
        return is_ok, pids, err_msg

    @classmethod
    def start_mysql_and_pids(self, cmd='', os_ip='127.0.0.1', os_user='root',
                              os_password='root', os_port=22):
        """使用 grep 命令查看含有mysqld的相关pid"""

        # 空命令则返回执行失败
        if not cmd:
            return False, '', []

        cmd = ("`{cmd}` && ps -ef | grep -v grep | grep mysqld |"
               " awk '{col}'".format(cmd = cmd, col = '{print $2}'))

        # ssh 远程执行命令
        is_ok, out_msg, err_msg = SSHTool.ssh_exec_cmd(cmd,
                                                       host = os_ip,
                                                       username = os_user,
                                                       password = os_password,
                                                       port = os_port)
        pids = [pid.strip() for pid in out_msg]
        return is_ok, pids, err_msg

    @classmethod
    def get_mysql_start_possible_pids(self, cmd='', os_ip='127.0.0.1', os_user='root',
                              os_password='root', os_port=22):
        """使用 grep 命令查看含有mysqld的相关pid"""

        # 空命令则返回执行失败
        if not cmd:
            return False, [], []

        # ssh 远程执行命令
        is_ok, out_msg, err_msg = SSHTool.ssh_exec_cmd(cmd,
                                                       host = os_ip,
                                                       username = os_user,
                                                       password = os_password,
                                                       port = os_port)
        pids = [pid.strip() for pid in out_msg]
        return is_ok, pids, err_msg

    @classmethod
    def stop_mysql_instance(self, mysqladmin='', mysql_user='root', 
                              mysql_password='root', mysql_host='127.0.0.1',
                              mysql_port=3306, os_ip='127.0.0.1', os_user='root',
                              os_password='root', os_port=22):
        """判断MySQL是否启动"""
       
        shutdown_ok = False
        if not mysqladmin:
            mysqladmin = __mysqladmin

        # 拼凑 mysqladmin ping 命令
        cmd = '{mysqladmin} -u{user} -p{pwd} -h{host} -P{port} shutdown'.format(
                                                mysqladmin = mysqladmin,
                                                user = mysql_user,
                                                pwd = mysql_password,
                                                host = mysql_host,
                                                port = mysql_port)
        # ssh 远程执行命令
        is_ok, out_msg, err_msg = SSHTool.ssh_exec_cmd(cmd,
                                                       host = os_ip,
                                                       username = os_user,
                                                       password = os_password,
                                                       port = os_port)
        # 命令执行成功，并且error_msg = 'Warning: Using'代表成功
        if is_ok and len(err_msg) == 1:
            if err_msg.pop().strip() == 'Warning: Using a password on the command line interface can be insecure.':
                shutdown_ok = True
        return shutdown_ok

    @classmethod
    def execute_sql(self, host='127.0.0.1', port=3306, user='root',
                    passwd='', db='', sql_text = ''):
        """ 执行SQL返回结果
        Args:
            host: ip
            port: 端口
            passwd: 密码
            user: 用户名
            db: 数据库名
            sql_text: 需要执行的sql
        Return: 
            rows_dict: 行的值
            count: 影响行数
            start_timestamp: 执行开始的时间
            stop_timestamp: 执行结束时间
            interval_timestamp: 执行总时间
            error_msg: 错误信息
        Raise: None
        """
    
        db_conf = {
            'host': host,
            'port': port,
            'user': user,
            'passwd': passwd,
            'db': db,
            'charset': 'utf8',
        }
        # 初始化值
        rows_dict = ()
        count = 0
        start_timestamp = 0
        stop_timestamp = 0
        error_msg = ''

        try:
            conn = MySQLdb.connect(**db_conf)
            cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)

            start_timestamp = time.time()

            count = cursor.execute(sql_text)
            rows_dict = cursor.fetchall()
            conn.commit()

            stop_timestamp = time.time()
        except:
            conn.rollback()
            error_msg = traceback.format_exc()
            logger.error('执行sql失败')
            logger.error(error_msg)
        finally:
            conn.close()

        return rows_dict, count, start_timestamp, stop_timestamp, error_msg

    @classmethod
    def get_terminal_result(self, host='127.0.0.1', port=3306, user='root',
                    passwd='', db='', sql_text = ''):
        result = {
            'rows_str': '',
            'count': 0,
            'start_timestamp': 0,
            'stop_timestamp': 0,
            'interval_timestamp': 0,
            'error_msg': ''
        }
        data = self.execute_sql(host = host, port = port, user = user,
                         passwd = passwd, db = db, sql_text = sql_text)

        result['count'] = data[1]
        result['start_timestamp'] = data[2]
        result['stop_timestamp'] = data[3]

        # 执行时间 单位 ms
        result['interval_timestamp'] = (data[3] - data[2]) * 1000

        # 过滤输出错误信息
        if data[4]:
            error_msg = data[4].split('Error').pop()
            result['error_msg'] = error_msg

        result['rows_str'] = data[0]

        logger.error(result)

        return result

    @classmethod
    def get_database_names(self, host='127.0.0.1', port=3306,
                                 user='root', passwd=''):
        """获取MySQL实例中所有的数据库名"""

        db_conf = {
            'host': host,
            'port': port,
            'user': user,
            'passwd': passwd,
            'sql_text': 'SHOW DATABASES',
        }

        data = self.execute_sql(**db_conf)
        database_names = set(item.get('Database', '') for item in data[0])
        return database_names 
       

def main():
    pass

if __name__ == '__main__':
    main()
