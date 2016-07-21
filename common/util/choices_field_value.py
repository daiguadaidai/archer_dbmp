# -*- coding:utf-8 -*-

class ChoicesFieldValue(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def gender(self):
        """获取性别"""
        gender = (
            (1, '男'),
            (2, '女'),
            (3, '其他'),
        )
        return gender
