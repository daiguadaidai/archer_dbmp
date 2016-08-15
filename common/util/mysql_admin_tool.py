#-*- coding: utf-8 -*-

from common.util.ssh_tool import SSHTool

import logging

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
       
        is_alived = False
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
        # 如果命令执行成功并且返回信息是 mysqld is alive就代表MySQL连接成功
        if is_ok and len(err_msg) <= 1:
            if out_msg.pop().strip() == 'Warning: Using a password on the command line interface can be insecure.':
                is_alived = True
        return is_alived

def main():
    pass

if __name__ == '__main__':
    main()
