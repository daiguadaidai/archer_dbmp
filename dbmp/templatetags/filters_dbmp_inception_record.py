#-*- coding: utf-8 -*-

from django import template
from common.model_choices_field_value.field_dbmp_inception_record import FieldDbmpInceptionRecord

register = template.Library()

@register.filter(name='f_inc_rec_execute_status') 
def f_inc_rec_execute_status(num):
    """通过数字获得Model的状态值"""
    execute_status = dict(FieldDbmpInceptionRecord.inc_rec_execute_status())

    return execute_status.get(num, '无效状态')

@register.filter(name='f_inc_rec_execute_status_color') 
def f_inc_rec_execute_status_color(num):
    """通过数字获得Model的状态值应该显示的颜色"""
    execute_status_color = dict(FieldDbmpInceptionRecord.inc_rec_execute_status_color())
 
    return execute_status_color.get(num, 'default')

@register.filter(name='f_inc_rec_inception_target') 
def f_inc_rec_inception_target(num):
    """通过数字获得Model的状态值"""
    inception_target = dict(FieldDbmpInceptionRecord.inc_rec_inception_target())

    return inception_target.get(num, '未知')
