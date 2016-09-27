#-*- coding: utf-8 -*-

from django.db import transaction
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance
from dbmp.models.dbmp_mysql_database import DbmpMysqlDatabase
from common.util.mysql_admin_tool import MysqlAdminTool
from common.util.ip_tool import IpTool
from common.util.decorator_tool import DecoratorTool

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

@DecoratorTool.get_request_alert_message
def list_database_use_business_detail(request):
    """展现实例数据库列表"""
    params = {}


    try:
        mysql_instance_id = int(request.GET.get('mysql_instance_id', '0'))
        mysql_business_id = int(request.GET.get('mysql_business_id', '0'))
    except ValueError:
        cur_page = 1
        mysql_business_id = 0

    params['mysql_instance_id'] = mysql_instance_id
    params['mysql_business_id'] = mysql_business_id

    try:
        dbmp_mysql_databases = DbmpMysqlDatabase.objects.values(
                                               'mysql_database_id',
                                               'name',
                                               'update_time').filter(
                            mysql_instance_id = mysql_instance_id)
        params['dbmp_mysql_databases'] = dbmp_mysql_databases
    except: # 没有获取到实例信息则转跳列表页面
        logger.info(traceback.format_exc())
        logger.info('获取DbmpMysqlDatabase失败')
        request.session['alert_message_now']['danger_msg'].append(
                                                '没有找到相关数据库，请同步完成再选择')
        return HttpResponseRedirect(request.environ['HTTP_REFERER'])

    return render(request, 'dbmp_mysql_database/list_database_use_business_detail.html', params)
    

def ajax_sync_database(request):
    """ajax 同步更新当前实例最新数据库列表
    Return:
        is_ok 0/1/2
            0: 获取信息出错
            1: 同步成功
            2: 不用同步
    """

    is_ok = 0
    if request.method == 'POST':
        mysql_instance_id = int(request.POST.get('mysql_instance_id', '0'))  

        if not mysql_instance_id: # 没有传入有效ID返回失败
            logger.info(traceback.format_exc())
            logger.info('传入DbmpMysqlInstance ID 无效: {id}'.format(id=mysql_instance_id))
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        try:
            # 1.获取MySQL实例
            dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                'mysql_instance_id',
                                                'username',
                                                'password',
                                                'port',
                                                'host',).get(
                               mysql_instance_id = mysql_instance_id)
        except DbmpMysqlInstance.DoesNotExist: # 没有获取到实例信息则转跳列表页面
            logger.info(traceback.format_exc())
            logger.info('获取DbmpMysqlInstance实例失败: {id}'.format(id=mysql_instance_id))
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')


        try:
            dbmp_mysql_databases = DbmpMysqlDatabase.objects.values(
                                                   'name').filter(
                                mysql_instance_id = mysql_instance_id)
            database_names_old = set([item.get('name', '') for item in dbmp_mysql_databases])
        except: # 没有获取到实例信息则转跳列表页面
            logger.info(traceback.format_exc())
            logger.info('获取DbmpMysqlDatabase失败')
            database_names_old = set([])

        database_names_real = MysqlAdminTool.get_database_names(
                    user = dbmp_mysql_instance.get('username', ''),
                    passwd = dbmp_mysql_instance.get('password', ''),
                    host = IpTool.num2ip(dbmp_mysql_instance.get('host', '')),
                    port = dbmp_mysql_instance.get('port', 3306))

        # 获得缺少的数据库名
        database_names_lack = list(database_names_real - database_names_old)
        # 构造 list 对象
        dbmp_mysql_database_list = [DbmpMysqlDatabase(mysql_instance_id=mysql_instance_id, name=name) for name in database_names_lack]
        
        # 获得多余过期的数据库名
        database_names_redundant = list(database_names_old - database_names_real)

        try:
            with transaction.atomic():

                # 删除数据多余过期数据
                if database_names_redundant:
                    DbmpMysqlDatabase.objects.filter(
                                mysql_instance_id = mysql_instance_id).filter(
                                name__in = database_names_redundant).delete()
                    is_ok = 1
            

                # 插入缺少的数据库名
                if dbmp_mysql_database_list:
                    DbmpMysqlDatabase.objects.bulk_create(dbmp_mysql_database_list)
                    is_ok = 1

                # 不需要更新
                if not database_names_redundant and not dbmp_mysql_database_list:
                    is_ok = 2
        except IntegrityError, e:
            logger.info(traceback.format_exc())
            logger.info('添加失败')
            if e.args[0] == 1062:
                logger.info('添加失败, 需要添加的相关信息重复')
        except Exception, e:
            logger.info(traceback.format_exc())
            logger.info('保存失败')
            logger.info('添加或删除数据库数据失败')

    respons_data = json.dumps(is_ok)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_search_database(request):
    """ajax 获得数据库"""

    if request.method == 'POST':
        mysql_instance_id = int(request.POST.get('mysql_instance_id', '0'))  

        if not mysql_instance_id: # 没有传入有效ID返回失败
            logger.info(traceback.format_exc())
            logger.info('传入DbmpMysqlInstance ID 无效: {id}'.format(id=mysql_instance_id))
            respons_data = json.dumps(False)
            return HttpResponse(respons_data, content_type='application/json')

        try:
            dbmp_mysql_databases = DbmpMysqlDatabase.objects.values(
                                                   'mysql_database_id',
                                                   'update_time',
                                                   'name').filter(
                                mysql_instance_id = mysql_instance_id)
            for dbmp_mysql_database in dbmp_mysql_databases:
                dbmp_mysql_database['update_time'] = str(dbmp_mysql_database['update_time'])
                print dbmp_mysql_database

            respons_data = json.dumps(list(dbmp_mysql_databases))
            return HttpResponse(respons_data, content_type='application/json')
        except: # 没有获取到实例信息则转跳列表页面
            respons_data = json.dumps(False)
            return HttpResponse(respons_data, content_type='application/json')
            logger.error(traceback.format_exc())
            logger.error('获取DbmpMysqlDatabase失败')
