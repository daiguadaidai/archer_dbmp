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

class DbmpInceptionBusinessDetail(models.Model):
    inception_business_detail_id = models.AutoField(primary_key=True)
    inception_business_id = models.IntegerField()
    inception_record_id = models.IntegerField()
    mysql_business_id = models.IntegerField()
    mysql_database_id = models.IntegerField()
    execute_status = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Java toString 方法"""
        print_str = ('DbmpInceptionBusiness({inception_business_detail_id},'
                                           '{inception_business_id},'
                                           '{inception_record_id},'
                                           '{mysql_business_id},'
                                           '{mysql_database_id})'.format(
                     inception_business_detail_id = self.inception_business_detail_id,
                     inception_business_id = self.inception_business_id,
                     inception_record_id = self.inception_record_id,
                     mysql_business_id = self.mysql_business_id,
                     mysql_database_id = self.mysql_database_id))
        return print_str

    class Meta:
        managed = False
        db_table = 'dbmp_inception_business_detail'
        unique_together = (('inception_record_id', 'mysql_database_id'),)
