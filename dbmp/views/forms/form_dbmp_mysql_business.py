#-*- coding: utf-8 -*-

from django import forms

class EditForm(forms.Form):
    mysql_business_id = forms.IntegerField(required = True, min_value = 0,
        error_messages = {'required': '找不到业务组', 'invalid': '不合法业务组'})
    name = forms.CharField(required = True, min_length = 1, max_length = 50,
        error_messages = {'required': '业务组名称不能为空', 'invalid': '业务组名称长度范围应该1到50'})
    remark = forms.CharField(required = True, min_length = 1, max_length = 200,
        error_messages = {'required': '业务组备注不能为空', 'invalid': '业务组备注长度范围应该1到200'})

class AddForm(forms.Form):
    name = forms.CharField(required = True, min_length = 1, max_length = 50,
        error_messages = {'required': '业务组名称不能为空', 'invalid': '业务组名称长度范围应该1到50'})
    remark = forms.CharField(required = True, min_length = 1, max_length = 200,
        error_messages = {'required': '业务组备注不能为空', 'invalid': '业务组备注长度范围应该1到200'})
