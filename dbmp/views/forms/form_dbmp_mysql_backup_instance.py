#-*- coding: utf-8 -*-

from django import forms

class EditForm(forms.Form):
    mysql_instance_id = forms.IntegerField(required = True, min_value = 0, 
        error_messages = {'required': '找不到MySQL实例', 'invalid': '不合法MySQL实例'})
    backup_tool = forms.IntegerField(required = True, min_value = 1, max_value = 4,
        error_messages = {'required': 'MySQL备份工具不能为空', 'invalid': '支持的MySQL备份工具：1、mysqldump，2、mysqlpump、3、mydumper、4、xtrabackup'})
    backup_type = forms.IntegerField(required = True, min_value = 1, max_value = 3,
        error_messages = {'required': '备份类型不能为空', 'invalid': '支持的备份类型为：1、强制指定实例备份，2、强制寻找备份，3、最优型备份'})
    is_all_instance = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '您还未选择是否全实例备份', 'invalid': '选择是否备份整个实例失败：0、否，1、是'})
    is_binlog = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否备份binlog', 'invalid': '选择是否备份binlog失败：0、否，1、是'})
    is_compress = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份压缩', 'invalid': '选择备份集是否压缩失败：0、否，1、是'})
    is_to_remote = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份发送至远程', 'invalid': '选择是否将备份发送至远程失败：0、否，1、是'})
    backup_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '本地备份路径(backup_dir)不能为空', 'invalid': '本地备份路径(backup_dir)长度范围应该5到200'})
    backup_name = forms.CharField(required = True, min_length = 1, max_length = 100,
        error_messages = {'required': '备份集名称不能为空', 'invalid': '备份集名称长度范围应该1到100'})
    backup_tool_file = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '备份工具命令路径(backup_tool_file)不能为空', 'invalid': '备份工具命令路径长度范围应该5到200'})

    # 备份指定的而外参数
    backup_tool_param = forms.CharField(required=False)

class EditHasRemoteForm(forms.Form):
    """编辑包含远程备份表单"""
    mysql_instance_id = forms.IntegerField(required = True, min_value = 0, 
        error_messages = {'required': '找不到MySQL实例', 'invalid': '不合法MySQL实例'})
    backup_tool = forms.IntegerField(required = True, min_value = 1, max_value = 4,
        error_messages = {'required': 'MySQL备份工具不能为空', 'invalid': '支持的MySQL备份工具：1、mysqldump，2、mysqlpump、3、mydumper、4、xtrabackup'})
    backup_type = forms.IntegerField(required = True, min_value = 1, max_value = 3,
        error_messages = {'required': '备份类型不能为空', 'invalid': '支持的备份类型为：1、强制指定实例备份，2、强制寻找备份，3、最优型备份'})
    is_all_instance = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '您还未选择是否全实例备份', 'invalid': '选择是否备份整个实例失败：0、否，1、是'})
    is_binlog = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否备份binlog', 'invalid': '选择是否备份binlog失败：0、否，1、是'})
    is_compress = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份压缩', 'invalid': '选择备份集是否压缩失败：0、否，1、是'})
    is_to_remote = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份发送至远程', 'invalid': '选择是否将备份发送至远程失败：0、否，1、是'})
    backup_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '本地备份路径(backup_dir)不能为空', 'invalid': '本地备份路径(backup_dir)长度范围应该5到200'})
    backup_name = forms.CharField(required = True, min_length = 1, max_length = 100,
        error_messages = {'required': '备份集名称不能为空', 'invalid': '备份集名称长度范围应该1到100'})
    backup_tool_file = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '备份工具命令路径(backup_tool_file)不能为空', 'invalid': '备份工具命令路径长度范围应该5到200'})

    # 备份指定的而外参数
    backup_tool_param = forms.CharField(required=False)
    # 远程备份操作系统
    os_id = forms.IntegerField(required = True, min_value = 0,
        error_messages = {'required': '找不到MySQL实例对应的OS', 'invalid': '不合法的OS信息'})
    # 远程备份目录
    remote_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '远程备份路径(remote_dir)不能为空', 'invalid': '远程备份路径(remote_dir)长度范围应该5到200'})

class AddForm(forms.Form):
    mysql_instance_id = forms.IntegerField(required = True, min_value = 0, 
        error_messages = {'required': '找不到MySQL实例', 'invalid': '不合法MySQL实例'})
    backup_tool = forms.IntegerField(required = True, min_value = 1, max_value = 4,
        error_messages = {'required': 'MySQL备份工具不能为空', 'invalid': '支持的MySQL备份工具：1、mysqldump，2、mysqlpump、3、mydumper、4、xtrabackup'})
    backup_type = forms.IntegerField(required = True, min_value = 1, max_value = 3,
        error_messages = {'required': '备份类型不能为空', 'invalid': '支持的备份类型为：1、强制指定实例备份，2、强制寻找备份，3、最优型备份'})
    is_all_instance = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '您还未选择是否全实例备份', 'invalid': '选择是否备份整个实例失败：0、否，1、是'})
    is_binlog = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否备份binlog', 'invalid': '选择是否备份binlog失败：0、否，1、是'})
    is_compress = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份压缩', 'invalid': '选择备份集是否压缩失败：0、否，1、是'})
    is_to_remote = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份发送至远程', 'invalid': '选择是否将备份发送至远程失败：0、否，1、是'})
    backup_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '本地备份路径(backup_dir)不能为空', 'invalid': '本地备份路径(backup_dir)长度范围应该5到200'})
    backup_name = forms.CharField(required = True, min_length = 1, max_length = 100,
        error_messages = {'required': '备份集名称不能为空', 'invalid': '备份集名称长度范围应该1到100'})
    backup_tool_file = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '备份工具命令路径(backup_tool_file)不能为空', 'invalid': '备份工具命令路径长度范围应该5到200'})

    # 备份指定的而外参数
    backup_tool_param = forms.CharField(required=False)

class AddHasRemoteForm(forms.Form):
    """包含添加远程备份表单"""
    mysql_instance_id = forms.IntegerField(required = True, min_value = 0, 
        error_messages = {'required': '找不到MySQL实例', 'invalid': '不合法MySQL实例'})
    backup_tool = forms.IntegerField(required = True, min_value = 1, max_value = 4,
        error_messages = {'required': 'MySQL备份工具不能为空', 'invalid': '支持的MySQL备份工具：1、mysqldump，2、mysqlpump、3、mydumper、4、xtrabackup'})
    backup_type = forms.IntegerField(required = True, min_value = 1, max_value = 3,
        error_messages = {'required': '备份类型不能为空', 'invalid': '支持的备份类型为：1、强制指定实例备份，2、强制寻找备份，3、最优型备份'})
    is_all_instance = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '您还未选择是否全实例备份', 'invalid': '选择是否备份整个实例失败：0、否，1、是'})
    is_binlog = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否备份binlog', 'invalid': '选择是否备份binlog失败：0、否，1、是'})
    is_compress = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份压缩', 'invalid': '选择备份集是否压缩失败：0、否，1、是'})
    is_to_remote = forms.IntegerField(required = True, min_value = 0, max_value = 1,
        error_messages = {'required': '必须选择是否将备份发送至远程', 'invalid': '选择是否将备份发送至远程失败：0、否，1、是'})
    backup_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '本地备份路径(backup_dir)不能为空', 'invalid': '本地备份路径(backup_dir)长度范围应该5到200'})
    backup_name = forms.CharField(required = True, min_length = 1, max_length = 100,
        error_messages = {'required': '备份集名称不能为空', 'invalid': '备份集名称长度范围应该1到100'})
    backup_tool_file = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '备份工具命令路径(backup_tool_file)不能为空', 'invalid': '备份工具命令路径长度范围应该5到200'})

    # 备份指定的而外参数
    backup_tool_param = forms.CharField(required=False)
    # 远程备份操作系统
    os_id = forms.IntegerField(required = True, min_value = 0,
        error_messages = {'required': '找不到MySQL实例对应的OS', 'invalid': '不合法的OS信息'})
    # 远程备份目录
    remote_dir = forms.CharField(required = True, min_length = 5, max_length = 200,
        error_messages = {'required': '远程备份路径(remote_dir)不能为空', 'invalid': '远程备份路径(remote_dir)长度范围应该5到200'})
