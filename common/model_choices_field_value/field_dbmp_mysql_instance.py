# -*- coding:utf-8 -*-

class FieldDbmpMysqlInstance(object):
    """用于Model字段值的选择"""

    def __init__(self):
        pass

    @classmethod
    def run_status(self):
        """MySQL实例正在运行状态"""
        value = (
            (1, '已停止'),
            (2, '运行中'),
            (3, '未知'),
        )
        return value

    @classmethod
    def run_status_color(self):
        """MySQL实例正在运行状态 对应显示的颜色"""
        value = (
            (1, 'danger'),
            (2, 'success'),
            (3, 'warning'),
        )
        return value
