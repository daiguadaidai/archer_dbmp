# -*- coding:utf-8 -*-

class FieldDbmpMysqlInstance(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def run_status(self):
        """使用备份工具"""
        value = (
            (1, '已停止'),
            (2, '运行中'),
            (3, '未知'),
        )
        return value
