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
