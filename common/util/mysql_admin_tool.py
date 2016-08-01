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


def main():
    pass

if __name__ == '__main__':
    main()
