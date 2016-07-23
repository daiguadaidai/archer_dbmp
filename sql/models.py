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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class CmdbOs(models.Model):
    os_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=50)
    alias = models.CharField(max_length=40)
    ip = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cmdb_os'


class DbmpMysqlBackupInfo(models.Model):
    mysql_backup_info_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField()
    backup_status = models.IntegerField()
    backup_data_status = models.IntegerField()
    check_status = models.IntegerField()
    binlog_status = models.IntegerField()
    trans_data_status = models.IntegerField()
    trans_binlog_status = models.IntegerField()
    compress_status = models.IntegerField()
    thread_id = models.IntegerField()
    backup_dir = models.CharField(max_length=250)
    remote_backup_dir = models.CharField(max_length=250)
    backup_size = models.BigIntegerField()
    backup_start_time = models.DateTimeField()
    backup_end_time = models.DateTimeField(blank=True, null=True)
    check_start_time = models.DateTimeField(blank=True, null=True)
    check_end_time = models.DateTimeField(blank=True, null=True)
    trans_start_time = models.DateTimeField(blank=True, null=True)
    trans_end_time = models.DateTimeField(blank=True, null=True)
    message = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_backup_info'


class DbmpMysqlBackupInstance(models.Model):
    mysql_backup_instance_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField(unique=True)
    backup_tool = models.IntegerField()
    backup_type = models.IntegerField()
    is_all_instance = models.IntegerField()
    is_binlog = models.IntegerField()
    is_compress = models.IntegerField()
    is_to_remote = models.IntegerField()
    backup_dir = models.CharField(max_length=200)
    backup_tool_file = models.CharField(max_length=200)
    backup_tool_param = models.CharField(max_length=200)
    backup_name = models.CharField(max_length=100)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_backup_instance'


class DbmpMysqlBackupRemote(models.Model):
    mysql_backup_remote_id = models.AutoField(primary_key=True)
    os_id = models.IntegerField()
    mysql_instance_id = models.IntegerField(unique=True)
    remote_dir = models.CharField(max_length=200)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_backup_remote'


class DbmpMysqlBusinessGroup(models.Model):
    mysql_business_group_id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=40)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_business_group'


class DbmpMysqlHaGroup(models.Model):
    mysql_ha_group_id = models.AutoField(primary_key=True)
    alias = models.CharField(max_length=40)
    remark = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_ha_group'


class DbmpMysqlHaGroupDetail(models.Model):
    mysql_ha_group_detail_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField(unique=True)
    mysql_ha_group_id = models.IntegerField()
    backup_priority = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

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
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_instance'
        unique_together = (('os_id', 'port'),)


class DbmpMysqlInstanceInfo(models.Model):
    mysql_instance_info_id = models.AutoField(primary_key=True)
    mysql_instance_id = models.IntegerField()
    my_cnf_path = models.CharField(max_length=200)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dbmp_mysql_instance_info'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
