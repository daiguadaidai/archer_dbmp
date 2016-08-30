#-*- coding: utf-8 -*-

from django import template
from common.model_choices_field_value.field_dbmp_mysql_backup_instance import FieldDbmpMysqlBackupInstance

register = template.Library()

@register.filter(name='f_backup_tool') 
def f_backup_tool(num):
    """通过数字获得Model的状态值"""
    backup_tool = dict(FieldDbmpMysqlBackupInstance.backup_tool())

    return backup_tool.get(num, '未知')

@register.filter(name='f_backup_type')
def f_backup_type(num):
    """通过数字获得Model的状态值"""
    backup_type = dict(FieldDbmpMysqlBackupInstance.backup_type())

    return backup_type.get(num, '未知')

@register.filter(name='f_is_all_instance')
def f_is_all_instance(num):
    """通过数字获得Model的状态值"""
    is_all_instance = dict(FieldDbmpMysqlBackupInstance.is_all_instance())

    return is_all_instance.get(num, '未知')

@register.filter(name='f_is_binlog')
def f_is_binlog(num):
    """通过数字获得Model的状态值"""
    is_binlog = dict(FieldDbmpMysqlBackupInstance.is_binlog())

    return is_binlog.get(num, '未知')

@register.filter(name='f_is_compress')
def f_is_compress(num):
    """通过数字获得Model的状态值"""
    is_compress = dict(FieldDbmpMysqlBackupInstance.is_compress())

    return is_compress.get(num, '未知')

@register.filter(name='f_is_to_remote')
def f_is_to_remote(num):
    """通过数字获得Model的状态值"""
    is_to_remote = dict(FieldDbmpMysqlBackupInstance.is_to_remote())

    return is_to_remote.get(num, '未知')
