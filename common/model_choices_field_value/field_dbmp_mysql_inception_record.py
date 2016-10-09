# -*- coding:utf-8 -*-

class FieldDbmpInceptionRecord(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def is_remote_backup(self):
        """审核前是否备份"""
        value = (
            (0, '否'),
            (1, '是'),
        )
        return value
