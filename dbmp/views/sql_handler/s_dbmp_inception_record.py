#-*- coding:utf-8 -*-

from django.db import connection
from collections import Counter 
from dbmp.models.dbmp_mysql_business_detail import DbmpMysqlBusinessDetail

class SQLDbmpInceptionRecord(object):

    def check_inception_database_business_duplicate(self, database_ids='',
                                                          business_ids='',
                                                          inception_target=2):
        """判断执行审核的数据库和业务组的数据库/业务组和业务组的数据库是否有重复"""
        if inception_target not in [2, 3]: # 如果传入的不是 业务组 或混合型 返回不重复
            return False, ''

        if inception_target == 2 and len(business_ids) < 2: # 如果是业务组, 但是只有一个业务组则无需判断
            return False, ''

        # 查询业务组中的所有数据库并比较
        dbmp_mysql_business_details = DbmpMysqlBusinessDetail.objects.values(
                                              'mysql_business_id',
                                              'mysql_database_id').filter(
                                              mysql_business_id__in = business_ids)

        ###################################################################
        # 业务组和业务组对比
        ###################################################################
        # 获得所有的数据库ID
        database_ids_all = [
            item['mysql_database_id']
            for item in dbmp_mysql_business_details
        ]
        
        # 获得数据库id出现次数
        database_ids_count = Counter(database_ids_all)
        
        # 获得重复的数据库ID
        database_ids_dup = [
            key 
            for key, value in database_ids_count.iteritems()
            if value > 1
        ]
        if database_ids_dup:
            # 获得在哪个业务组中有这些ID
            business_database_ids_all = [
                [item['mysql_database_id'], item['mysql_business_id']]
                for item in dbmp_mysql_business_details
            ]
            
            # 获得重复的 数据库ID 和 业务组ID
            business_database_ids_dup = [
                {'database_id': database_id, 'business_id': business_id}
                for database_id, business_id in business_database_ids_all
                if database_id in database_ids_dup
            ]

            message = '业务组和业务组之间有数据库重复({business_database_ids_dup})'.format(
                                     business_database_ids_dup = business_database_ids_dup)
            return True, message

        ###################################################################
        # 数据库和业务组对比
        ###################################################################
        if inception_target == 3:
            # 获得数据库和业务组重复ID
            database_ids_dup = [
                database_id
                for database_id in database_ids
                if database_id in database_ids_all
            ]

            if database_ids_dup:
                # 获得重复的 数据库ID 和 业务组ID
                business_database_ids_all = [
                    [item['mysql_database_id'], item['mysql_business_id']]
                    for item in dbmp_mysql_business_details
                ]
                
                # 获得重复的 数据库ID 和 业务组ID
                business_database_ids_dup = [
                    {'database_id': database_id, 'business_id': business_id}
                    for database_id, business_id in business_database_ids_all
                    if database_id in database_ids_dup
                ]

                message = ('数据库和业务组中的数据库重复。重复数据库id:{database_ids_dup},'
                           '对应的业务组:{business_database_ids_dup}'.format(
                           database_ids_dup = database_ids_dup,
                           business_database_ids_dup = business_database_ids_dup))

                return True, message

        return False, ''

