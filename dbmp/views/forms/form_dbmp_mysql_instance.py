#-*- coding: utf-8 -*-

from django import forms

class EditForm(forms.Form):
    mysql_instance_id = forms.IntegerField(required = True, min_value = 0, 
        error_messages = {'required': '找不到MySQL实例', 'invalid': '不合法MySQL实例'})
    os_id = forms.IntegerField(required = True, min_value = 0,
        error_messages = {'required': '找不到MySQL实例对应的OS', 'invalid': '不合法的OS信息'})
    host = forms.GenericIPAddressField(required = True,
        error_messages = {'required': 'MySQL Host 不能为空', 'invalid': '您输出的 MySQL Host 不符合IP的规范'})
    port = forms.IntegerField(required = True, min_value = 1025, max_value = 65535,
        error_messages = {'required': 'MySQL Port 不能为空', 'invalid': 'Port 的范围应该1025到65535'})
    username = forms.CharField(required = True, min_length = 1, max_length = 200,
        error_messages = {'required': 'MySQL 用户名不能为空', 'invalid': 'MySQL 用户名长度范围应该1到200'})
    password = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 用户密码不能为空', 'invalid': 'MySQL 用户密码长度范围应该1到200'})
    remark = forms.CharField(required = False, max_length = 200,
        error_messages = {'invalid': 'MySQL 备注长度范围应该1到200'})
    my_cnf_path = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 配置文件路径不能为空', 'invalid': 'MySQL 配置文件路径长度范围应该1到200'})
    base_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 软件路径(base_dir)不能为空', 'invalid': 'MySQL 软件路径(base_dir)长度范围应该1到200'})
    start_cmd = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 启动命令不能为空', 'invalid': 'MySQL 启动命令长度范围应该1到200'})

    mysql_instance_info_id = forms.IntegerField(required=False)

class AddForm(forms.Form):
    os_id = forms.IntegerField(required = True, min_value = 0,
        error_messages = {'required': '找不到MySQL实例对应的OS', 'invalid': '不合法的OS信息'})
    host = forms.GenericIPAddressField(required = True,
        error_messages = {'required': 'MySQL Host 不能为空', 'invalid': '您输出的 MySQL Host 不符合IP的规范'})
    port = forms.IntegerField(required = True, min_value = 1025, max_value = 65535,
        error_messages = {'required': 'MySQL Port 不能为空', 'invalid': 'Port 的范围应该1025到65535'})
    username = forms.CharField(required = True, min_length = 1, max_length = 200,
        error_messages = {'required': 'MySQL 用户名不能为空', 'invalid': 'MySQL 用户名长度范围应该1到200'})
    password = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 用户密码不能为空', 'invalid': 'MySQL 用户密码长度范围应该1到200'})
    remark = forms.CharField(required = False, max_length = 200,
        error_messages = {'invalid': 'MySQL 备注长度范围应该1到200'})
    my_cnf_path = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 配置文件路径不能为空', 'invalid': 'MySQL 配置文件路径长度范围应该1到200'})
    base_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 软件路径(base_dir)不能为空', 'invalid': 'MySQL 软件路径(base_dir)长度范围应该1到200'})
    start_cmd = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': 'MySQL 启动命令不能为空', 'invalid': 'MySQL 启动命令长度范围应该1到200'})
