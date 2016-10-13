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

    @classmethod
    def inc_rec_execute_status(self):
        """数据库执行SQL审核状态"""
        value = (
            (1, '未执行'),
            (2, '执行成功'),
            (3, '执行失败'),
            (4, '部分失败'),
        )
        return value

    @classmethod
    def inc_rec_execute_status_color(self):
        """MySQL实例正在运行状态 对应显示的颜色"""
        value = (
            (1, 'success'),
            (2, 'primary'),
            (3, 'danger'),
            (4, 'warning'),
        )
        return value
