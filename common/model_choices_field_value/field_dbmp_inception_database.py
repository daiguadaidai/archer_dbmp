# -*- coding:utf-8 -*-

class FieldDbmpInceptionDatabase(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def execute_status(self):
        """数据库执行SQL审核状态"""
        value = (
            (1, '未执行'),
            (2, '执行成功'),
            (3, '执行失败'),
        )
        return value

    @classmethod
    def execute_status_color(self):
        """MySQL实例正在运行状态 对应显示的颜色"""
        value = (
            (1, 'info'),
            (2, 'success'),
            (3, 'danger'),
        )
        return value
