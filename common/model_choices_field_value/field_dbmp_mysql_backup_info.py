# -*- coding:utf-8 -*-

class FieldDbmpMysqlBackupInfo(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def backup_status(self):
        """备份状态"""
        value = (
            (1, '未备份'),
            (2, '正在备份'),
            (3, '备份完成'),
            (4, '备份失败'),
            (5, '备份完成但和指定的有差异'),
        )
        return value

    @classmethod
    def backup_data_status(self):
        """备份数据状态"""
        value = (
            (1, '未备份'),
            (2, '备份失败'),
            (3, '备份完成'),
        )
        return value

    @classmethod
    def check_status(self):
        """校验备份集状态"""
        value = (
            (1, '未校验'),
            (2, '正在校验'),
            (3, '校验完成'),
            (4, '校验失败'),
        )
        return value

    @classmethod
    def binlog_status(self):
        """binlog备份状态"""
        value = (
            (1, '未备份'),
            (2, '备份失败'),
            (3, '备份完成'),
        )
        return value

    @classmethod
    def trans_data_status(self):
        """备份数据远程传输状态"""
        value = (
            (1, '未传输'),
            (2, '传输失败'),
            (3, '传输完成'),
        )
        return value

    @classmethod
    def trans_binlog_status(self):
        """备份binlog远程传输状态"""
        value = (
            (1, '未传输'),
            (2, '传输失败'),
            (3, '传输完成'),
        )
        return value

    @classmethod
    def compress_status(self):
        """binlog备份状态"""
        value = (
            (1, '未压缩'),
            (2, '压缩失败'),
            (3, '压缩完成未传输'),
        )
        return value
