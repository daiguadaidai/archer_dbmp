#-*- coding: utf-8 -*-

from django import template
from common.util.ip_tool import IpTool
from common.model_choices_field_value.field_dbmp_mysql_instance import FieldDbmpMysqlInstance

register = template.Library()

@register.filter(name='f_run_status') 
def f_run_status(num):
    """通过数字获得Model的状态值"""
    run_status = dict(FieldDbmpMysqlInstance.run_status())

    return run_status.get(num, '无效状态')

@register.filter(name='f_run_status_color') 
def f_run_status_color(num):
    """通过数字获得Model的状态值应该显示的颜色"""
    run_status_color = dict(FieldDbmpMysqlInstance.run_status_color())
 
    return run_status_color.get(num, 'default')
