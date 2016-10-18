#-*- coding: utf-8 -*-

from django.db import transaction
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from common.util.ip_tool import IpTool
from common.util.pagination import Pagination
from common.util.decorator_tool import DecoratorTool
from common.util.inception_tool import InceptionTool
from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance
from dbmp.models.dbmp_mysql_business_detail import DbmpMysqlBusinessDetail
from dbmp.models.dbmp_mysql_database import DbmpMysqlDatabase
from dbmp.models.dbmp_inception_instance import DbmpInceptionInstance
from dbmp.models.dbmp_inception_record import DbmpInceptionRecord
from dbmp.models.dbmp_inception_database import DbmpInceptionDatabase
from dbmp.models.dbmp_inception_business import DbmpInceptionBusiness
from dbmp.models.dbmp_inception_business_detail import DbmpInceptionBusinessDetail
from dbmp.views.sql_handler.s_dbmp_inception_database import SQLDbmpInceptionDatabase

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.
@DecoratorTool.clean_alert_message
def run_inception(request):
    """转调到执行SQL窗口"""
    params = {}
    params['error_msg'] = []

    if request.method == 'GET':
        try:  
            # 获得传入的MySQL实例ID
            inception_record_id = int(request.GET.get('inception_record_id', '0'))  
            inception_database_id = int(request.GET.get('inception_database_id', '0'))  
        except ValueError:  
            logger.info(traceback.format_exc())
            inception_record_id = 0
            inception_database_id = 0

        if not inception_record_id or not inception_database_id:
            params['error_msg'].append('输入的inception_record_id, inception_database_id有问题') 

        try:
            # 查找需要审核的实例
            s_dbmp_inception_database = SQLDbmpInceptionDatabase()
            # DbmpInceptionDatabase, DbmpMysqlDatabase, DbmpMysqlInstance 信息
            dbmp_inception_database = s_dbmp_inception_database.get_database_by_id_1(
                                                                     inception_database_id)
            params['dbmp_inception_database'] = dbmp_inception_database

            if not dbmp_inception_database:
                params['error_msg'].append('不能找到需要执行的数据库') 
            elif dbmp_inception_database.get('execute_status') == 2:
                params['error_msg'].append('此SQL已经在该数据库执行过了') 
            
        except Exception, e:
            logger.info(traceback.format_exc())
            params['error_msg'].append('查找需要执行的数据库有错')

        return render(request, 'dbmp_inception_database/run_inception.html', params)

def ajax_find_by_inception_record_id(request):
    """Ajax添加审核记录"""
    params = {}
    params['is_ok'] = False
    params['err_msg'] = ''

    if request.method == 'POST':
        try:
            inception_record_id = int(request.POST.get('inception_record_id', '0'))
            s_dbmp_inception_database = SQLDbmpInceptionDatabase()
            
            dbmp_inception_databases = s_dbmp_inception_database.find_databases_by_inception_record_id(
                                                                     inception_record_id)
            params['is_ok'] = True
            params['databases'] = dbmp_inception_databases
        except:
            logger.error(traceback.format_exc())
            params['err_msg'] = traceback.format_exc()

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_run_inception(request):
    """Ajax执行SQL"""
    params = {}
    params['is_ok'] = False
    params['inception_info'] = ''
    params['err_msg'] = ''

    if request.method == 'POST':
        try:
            inception_database_id = int(request.POST.get('inception_database_id', '0'))
            s_dbmp_inception_database = SQLDbmpInceptionDatabase()
            # 获得 DbmpInceptionDatabase, DbmpInceptionRecord, DbmpInceptionInstance
            #      DbmpMysqlDatabase, DbmpMysqlInstance 信息
            dbmp_inception_database = s_dbmp_inception_database.get_database_by_id_2(
                                                                     inception_database_id)
            if not dbmp_inception_database:
                logger.error('没有获取到执行SQL的数据库信息')
                params['err_msg'] = '没有获取到执行SQL的数据库信息'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')
        except:
            logger.error(traceback.format_exc())
            params['err_msg'] = '(获取执行SQL的数据库信息错误)'
            params['err_msg'] += traceback.format_exc()
            respons_data = json.dumps(params)
            return HttpResponse(respons_data, content_type='application/json')

        # 对SQL进行审核
        is_ok, inception_info = InceptionTool.inception_execute(
                                    inception_host = dbmp_inception_database.get('inc_host', 0),
                                    inception_port = dbmp_inception_database.get('inc_port', 0),
                                    mysql_user = dbmp_inception_database.get('mysql_username', ''),
                                    mysql_password = dbmp_inception_database.get('mysql_password', ''),
                                    mysql_host = dbmp_inception_database.get('mysql_host', 0),
                                    mysql_port = dbmp_inception_database.get('mysql_port', 0),
                                    db_name = dbmp_inception_database.get('db_name', ''),
                                    sql_text = dbmp_inception_database.get('sql_text', ''),
                                    charset = dbmp_inception_database.get('charset', 'utf8'))
        # 更新执行数据库状态
        execute_status = 0
        if is_ok:
            errlevel = max([item.get('errlevel') for item in inception_info])
            # 获取执行状态
            if errlevel == 0:
                execute_status = 2 # 成功
            elif errlevel == 1 or errlevel == 2 or not inception_info:
                execute_status = 3 # 失败
        else:
            execute_status = 3 # 失败
            params['err_msg'] = inception_info

        try:
            # 更新 dbmp_inception_database 状态
            DbmpInceptionDatabase.objects.filter(
                inception_database_id = inception_database_id).update(
                                            execute_status = execute_status)
        except Exception, e:
            logger.info(traceback.format_exc())
            logger.info('执行SQL成功, 但是更新失败执行sql数据库状态失败')
            params['err_msg'].append('执行SQL成功, 但是更新失败执行sql数据库状态失败')

        params['is_ok'] = is_ok
        params['execute_status'] = execute_status
        params['inception_info'] = inception_info

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')
