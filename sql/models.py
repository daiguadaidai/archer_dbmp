#-*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from common.model_choices_field_value.field_dbmp_mysql_backup_info import FieldDbmpMysqlBackupInfo
from common.model_choices_field_value.field_dbmp_mysql_backup_instance import FieldDbmpMysqlBackupInstance


class CmdbOs(models.Model):
    os_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=50)
    alias = models.CharField(max_length=40)
    ip = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'ip({ip}), hostname({hostname}), alias({alias})'.format(
                     ip = self.ip,
                     hostname = self.hostname,
                     alias = self.alias)
        return print_str

    class Meta:
        managed = False
        db_table = 'cmdb_os'


class DbmpMysqlBackupInfo(models.Model):
    mysql_backup_info_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField()
    backup_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.backup_status())
    backup_data_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.backup_data_status())
    check_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.check_status())
    binlog_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.binlog_status())
    trans_data_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.trans_data_status())
    trans_binlog_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.trans_binlog_status())
    compress_status = models.IntegerField(choices=FieldDbmpMysqlBackupInfo.compress_status())
    thread_id = models.IntegerField()
    backup_dir = models.CharField(max_length=250)
    remote_backup_dir = models.CharField(max_length=250)
    backup_size = models.BigIntegerField()
    backup_start_time = models.DateTimeField(auto_now_add=True)
    backup_end_time = models.DateTimeField(blank=True, null=True)
    check_start_time = models.DateTimeField(blank=True, null=True)
    check_end_time = models.DateTimeField(blank=True, null=True)
    trans_start_time = models.DateTimeField(blank=True, null=True)
    trans_end_time = models.DateTimeField(blank=True, null=True)
    message = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = ('mysql_backup_info_id({mysql_backup_info_id}), '
                     'mysql_instance_id({mysql_instance_id})'.format(
                     mysql_backup_info_id = self.mysql_backup_info_id,
                     mysql_instance_id = self.mysql_instance_id))
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_backup_info'


class DbmpMysqlBackupInstance(models.Model):
    mysql_backup_instance_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField(unique=True)
    backup_tool = models.IntegerField(FieldDbmpMysqlBackupInstance.backup_tool())
    backup_type = models.IntegerField(FieldDbmpMysqlBackupInstance.backup_type())
    is_all_instance = models.IntegerField(FieldDbmpMysqlBackupInstance.is_all_instance())
    is_binlog = models.IntegerField(FieldDbmpMysqlBackupInstance.is_binlog())
    is_compress = models.IntegerField(FieldDbmpMysqlBackupInstance.is_compress())
    is_to_remote = models.IntegerField(FieldDbmpMysqlBackupInstance.is_to_remote())
    backup_dir = models.CharField(max_length=200)
    backup_tool_file = models.CharField(max_length=200)
    backup_tool_param = models.CharField(max_length=200)
    backup_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'DbmpMysqlBackupInstance({mysql_backup_instance_id})'.format(
                     mysql_backup_info_id = self.mysql_backup_instance_id)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_backup_instance'


class DbmpMysqlBackupRemote(models.Model):
    mysql_backup_remote_id = models.AutoField(primary_key=True)
    os_id = models.IntegerField()
    mysql_instance_id = models.IntegerField(unique=True)
    remote_dir = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'DbmpMysqlBackupRemote({mysql_backup_remote_id})'.format(
                     mysql_backup_remote_id = self.mysql_backup_remote_id)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_backup_remote'


class DbmpMysqlBusinessGroup(models.Model):
    mysql_business_group_id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=40)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'DbmpMysqlBusinessGroup({alias})'.format(
                     alias = self.alias)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_business_group'


class DbmpMysqlHaGroup(models.Model):
    mysql_ha_group_id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=40)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'DbmpMysqlHaGroup({alias})'.format(
                     alias = self.alias)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_ha_group'


class DbmpMysqlHaGroupDetail(models.Model):
    mysql_ha_group_detail_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField(unique=True)
    mysql_ha_group_id = models.IntegerField()
    backup_priority = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'DbmpMysqlHaGroup({mysql_ha_group_detail_id})'.format(
                     mysql_ha_group_detail_id = self.mysql_ha_group_detail_id)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_ha_group_detail'


class DbmpMysqlInstance(models.Model):
    mysql_instance_id = models.AutoField(primary_key=True)
    os_id = models.IntegerField()
    host = models.IntegerField()
    port = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'host({host}), port({port}), os_id({os_id})'.format(
                     host = self.host,
                     port = self.port,
                     os_id = self.os_id)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_instance'


class DbmpMysqlInstanceInfo(models.Model):
    mysql_instance_info_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField()
    my_cnf_path = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = 'DbmpMysqlInstanceInfo({mysql_instance_info_id})'.format(
                     mysql_instance_info_id = self.mysql_instance_info_id)
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_instance_info'
