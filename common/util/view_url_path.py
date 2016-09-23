#-*- coding:utf-8 -*-

class ViewUrlPath(object):
    """view中需要转跳的url 路径定义
    """

    def __init__(self):
        pass

    @classmethod
    def path_dbmp_mysql_instance(self):
        """MySQL实例列表"""
        return '/dbmp/dbmp_mysql_instance'

    @classmethod
    def path_dbmp_mysql_backup_instance(self):
        """MySQL备份实例列表"""
        return '/dbmp/dbmp_mysql_backup_instance'

    @classmethod
    def path_dbmp_mysql_business(self):
        """MySQL业务组列表"""
        return '/dbmp/dbmp_mysql_business'
