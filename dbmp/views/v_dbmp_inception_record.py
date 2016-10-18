#-*- coding: utf-8 -*-

from django.db import transaction
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from common.util.ip_tool import IpTool
from common.util.pagination import Pagination
from common.util.view_url_path import ViewUrlPath
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
from dbmp.views.sql_handler.s_dbmp_inception_record import SQLDbmpInceptionRecord

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

@DecoratorTool.get_request_alert_message
def view(request):
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    # 点击链接转跳到编辑页面
    if request.method == 'GET':
        # 获取业务组
        inception_record_id = int(request.GET.get('inception_record_id', '0'))  

        if inception_record_id:
            try:
                # 1.业务组
                dbmp_inception_record = DbmpInceptionRecord.objects.get(
                                     inception_record_id = inception_record_id)
                params['dbmp_inception_record'] = dbmp_inception_record
            except DbmpInceptionRecord.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回点击编辑页面
                request.session['danger_msg'].append('对不起! 找不到指定的SQL审核数据')
                index_url = '{base_url}/index/'.format(
                                base_url = ViewUrlPath.path_dbmp_inception_record())
                return HttpResponseRedirect(index_url)

            try:
                # Inception实例
                dbmp_inception_instance = DbmpInceptionInstance.objects.values(
                                      'inception_instance_id',
                                      'host',
                                      'port',
                                      'alias').get(
                                     inception_instance_id = dbmp_inception_record.inception_instance_id)
                params['dbmp_inception_instance'] = dbmp_inception_instance
            except DbmpInceptionInstance.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回点击编辑页面
                request.session['danger_msg'].append('对不起! 找不到审核实例信息')
                index_url = '{base_url}/index/'.format(
                                base_url = ViewUrlPath.path_dbmp_inception_record())
                return HttpResponseRedirect(index_url)
            return render(request, 'dbmp_inception_record/view.html', params)
        else:
            request.session['danger_msg'] = '对不起! 找不到指定的业务组!'
            # 返回点击编辑页面
            request.session['danger_msg'].append('对不起! 找不到指定的SQL审核数据')
            index_url = '{base_url}/index/'.format(
                            base_url = ViewUrlPath.path_dbmp_inception_record())
            return HttpResponseRedirect(index_url)

@DecoratorTool.get_request_alert_message
def check(request):
    """SQL审核界面"""
    params = {}
    params['sql'] = '''
        ALTER TABLE alifeba_user
            MODIFY username VARCHAR(50) NOT NULL DEFAULT '' COMMENT '用户名',
            MODIFY realname VARCHAR(50) NOT NULL DEFAULT '' COMMENT '真实姓名'
    '''

    return render(request, 'dbmp_inception_record/check.html', params)

@DecoratorTool.get_request_alert_message
def add(request):
    """添加需要审核的SQL记录"""
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    if request.method == 'GET':
        check_iframe_name = request.GET.get('check_iframe_name', '')
        params['check_iframe_name'] = check_iframe_name
        return render(request, 'dbmp_inception_record/add.html', params)

def ajax_check(request):
    """对SQL进行审核"""
    params = {}
    params['is_ok'] = False
    if request.method == 'POST':
        try:    
            mysql_database_id = int(request.POST.get('mysql_database_id', '0'))
            inception_instance_id = int(request.POST.get('inception_instance_id', '0'))
            sql_text = request.POST.get('sql_text', '')
            charset = request.POST.get('charset', 'utf8mb4')
            
            # 如果获取的数据有问题直接返回失败
            if not mysql_database_id or not inception_instance_id or not sql_text:
                logger.error('SQL审核传入参数不全')
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')

            try:
                # 获取数据库信息
                dbmp_mysql_database = DbmpMysqlDatabase.objects.values(
                                               'mysql_database_id',
                                               'mysql_instance_id',
                                               'name').get(
                                          mysql_database_id = mysql_database_id)
            except DbmpMysqlDatabase.DoesNotExist:
                logger.error(traceback.format_exc())
                logger.error('对不起! 找不到相关数据库')
                params['inception_info'] =  '对不起! 找不到相关数据库'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')

            try:
                # 数据库实例信息
                dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                               'username',
                                               'password',
                                               'host',
                                               'port').get(
                                      mysql_instance_id = dbmp_mysql_database.get('mysql_instance_id', 0))
            except DbmpMysqlInstance.DoesNotExist:
                logger.error(traceback.format_exc())
                logger.error('对不起! 找不到相关实例信息')
                params['inception_info'] =  '对不起! 找不到相关实例信息'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')

            try:
                # Inception实例信息
                dbmp_inception_instance = DbmpInceptionInstance.objects.values(
                                               'host',
                                               'port').get(
                                     inception_instance_id = inception_instance_id)
            except DbmpInceptionInstance.DoesNotExist:
                logger.error(traceback.format_exc())
                logger.error('对不起! 找不到相关Inception实例')
                params['inception_info'] =  '对不起! 找不到相关Inception实例'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')

            # 对SQL进行审核
            is_ok, inception_info = InceptionTool.inception_check_only(
                                        inception_host = IpTool.num2ip(dbmp_inception_instance.get('host', 0)),
                                        inception_port = dbmp_inception_instance.get('port', 0),
                                        mysql_user = dbmp_mysql_instance.get('username', ''),
                                        mysql_password = dbmp_mysql_instance.get('password', ''),
                                        mysql_host = IpTool.num2ip(dbmp_mysql_instance.get('host', 0)),
                                        mysql_port = dbmp_mysql_instance.get('port', 0),
                                        db_name = dbmp_mysql_database.get('name', ''),
                                        sql_text = sql_text,
                                        charset = charset)

            params['is_ok'] = is_ok
            params['inception_info'] = inception_info
        except:
            logger.error(traceback.format_exc())
     

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_add(request):
    """Ajax添加审核记录"""
    params = {}
    params['is_ok'] = False
    params['err_msg'] = ''
    if request.method == 'POST':
        try:
            inception_instance_id = int(request.POST.get('inception_instance_id', '0'))
            sql_text = request.POST.get('sql_text', '') 
            tag = request.POST.get('tag', '')
            remark = request.POST.get('remark', '')
            charset = request.POST.get('charset', 'utf8mb4')
            database_ids_str = request.POST.get('database_ids', '')
            business_ids_str = request.POST.get('business_ids', '')

            if not tag or not remark:
                logger.error('添加审核SQL，没有填写 标签和备注')
                params['err_msg'] = '没有填写 标签和备注'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')

            # 过滤前后 逗号(,)
            database_ids_str = database_ids_str.strip(',')
            business_ids_str = business_ids_str.strip(',')

            # 获得 数据库id列表 和 业务id列表
            database_ids = [int(id) for id in list(set(database_ids_str.split(','))) if id]
            business_ids = [int(id) for id in list(set(business_ids_str.split(','))) if id]

            inception_target = 3 # 默认审核未混合型(数据库/业务组)
           
            # 判断是哪种审核模式
            if database_ids and not business_ids: # 只有数据库
                inception_target = 1
            elif not database_ids and business_ids: # 只有业务组
                inception_target = 2
            elif database_ids and business_ids: # 混合型
                inception_target = 3
            else:
                logger.error('没有需要审核的数据库ID 和 业务组ID')
                params['err_msg'] = '没有需要审核的数据库ID 和 业务组ID'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')

            # 判断 数据库是否和业务组中的数据库重复，判断业务中之间数据库是否重复
            if inception_target in [2, 3]: # 只有 业务组和混合的才需要验证
                sql_dbmp_inception_record = SQLDbmpInceptionRecord()
                is_duplicate, message = sql_dbmp_inception_record.check_inception_database_business_duplicate(
                                                     database_ids,
                                                     business_ids,
                                                     inception_target)
                if is_duplicate:
                    logger.error(message)
                    params['err_msg'] = message
                    respons_data = json.dumps(params)
                    return HttpResponse(respons_data, content_type='application/json')
                
            try: # 添加审核记录
                with transaction.atomic():
                    # 添加DbmpInceptionRecord
                    dbmp_inception_record = DbmpInceptionRecord(
                                            inception_instance_id = inception_instance_id,
                                            is_remote_backup = 1,
                                            inception_target = inception_target,
                                            tag = tag,
                                            remark = remark,
                                            sql_text = sql_text,
                                            charset = charset,
                                            execute_status = 1)
                    dbmp_inception_record.save()

                    if inception_target in [1, 3]: # 添加审核数据库
                        inception_databases = [
                            DbmpInceptionDatabase(inception_record_id = dbmp_inception_record.inception_record_id,
                                                  mysql_database_id = database_id,
                                                  execute_status = 1)
                            for database_id in database_ids
                        ] 
                        DbmpInceptionDatabase.objects.bulk_create(inception_databases)

                    if inception_target in [2, 3]: # 添加审核业务组
                        for business_id in business_ids: # 循环添加 审核业务组
                            # 添加DbmpInceptionBusiness
                            dbmp_inception_business = DbmpInceptionBusiness(
                                                  inception_record_id = dbmp_inception_record.inception_record_id,
                                                  mysql_business_id = business_id,
                                                  execute_status = 1)
                            dbmp_inception_business.save()

                            # 获得审核业务组的明细(数据库)
                            dbmp_mysql_business_details = DbmpMysqlBusinessDetail.objects.values(
                                                                  'mysql_database_id').filter(
                                                                  mysql_business_id = business_id)
                            # 批量创建审核业务组明细(数据库)
                            inception_business_details = [
                                DbmpInceptionBusinessDetail(
                                                  inception_business_id = dbmp_inception_business.inception_business_id,
                                                  inception_record_id = dbmp_inception_record.inception_record_id,
                                                  mysql_business_id = business_id,
                                                  mysql_database_id = item['mysql_database_id'],
                                                  execute_status = 1)
                                for item in dbmp_mysql_business_details
                            ]
                            DbmpInceptionBusinessDetail.objects.bulk_create(inception_business_details)
                    
                params['is_ok'] = True
                params['inception_record_id'] = dbmp_inception_record.inception_record_id
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')
            except IntegrityError, e:
                logger.error('审核SQL添加(失败)')
                logger.error(traceback.format_exc())
                params['err_msg'] = '审核SQL添加(失败) \n'
                params['err_msg'] += traceback.format_exc()
                if e.args[0] == 1062:
                    logger.error('需要添加的相关信息重复')
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')
            except Exception, e:
                logger.info(traceback.format_exc())
                logger.info('添加失败, 保存数据库错误')
                params['err_msg'] = '添加失败, 保存数据库错误 \n'
                params['err_msg'] += traceback.format_exc()
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')
        except:
            logger.info(traceback.format_exc())

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')
