#-*- coding: utf-8 -*-

from django import template
from common.util.ip_tool import IpTool
from common.model_choices_field_value.field_dbmp_mysql_instance import FieldDbmpMysqlInstance

register = template.Library()

@register.filter(name='f_run_status') 
def f_run_status(num):
    run_status_dict = dict(FieldDbmpMysqlInstance.run_status())

    return run_status_dict.get(str(num), '无效状态')
