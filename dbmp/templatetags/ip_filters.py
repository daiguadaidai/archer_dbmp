#-*- coding: utf-8 -*-

from django import template
from common.util.ip_tool import IpTool

register = template.Library()

@register.filter(name='f_ip2num') 
def f_ip2num(ip):
    return IpTool.ip2num(ip)

@register.filter(name='f_num2ip') 
def f_num2ip(num):
    return IpTool.num2ip(num)


