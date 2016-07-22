# -*- coding:utf-8 -*-

class FieldDbmpMysqlBackupInstance(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def backup_tool(self):
        """使用备份工具"""
        value = (
            (1, 'mysqldump'),
            (2, 'mysqlpump'),
            (3, 'mydumper'),
            (4, 'xtrabackup'),
        )
        return value

    @classmethod
    def backup_type(self):
        """备份类型"""
        value = (
            (1, '强制指定实例备份'),
            (2, '强制寻找备份'),
            (3, '最优型备份'),
        )
        return value

    @classmethod
    def is_all_instance(self):
        """是否备份整个实例"""
        value = (
            (0, '否'),
            (1, '是'),
        )
        return value

    @classmethod
    def is_binlog(self):
        """是否备份binlog"""
        value = (
            (0, '否'),
            (1, '是'),
        )
        return value

    @classmethod
    def is_compress(self):
        """备份集是否压缩"""
        value = (
            (0, '否'),
            (1, '是'),
        )
        return value

    @classmethod
    def is_to_remote(self):
        """将备份传输至远程"""
        value = (
            (0, '否'),
            (1, '是'),
        )
        return value
