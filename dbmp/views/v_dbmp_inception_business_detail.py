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
from dbmp.models.dbmp_mysql_business import DbmpMysqlBusiness
from dbmp.models.dbmp_mysql_database import DbmpMysqlDatabase
from dbmp.models.dbmp_inception_instance import DbmpInceptionInstance
from dbmp.models.dbmp_inception_record import DbmpInceptionRecord
from dbmp.models.dbmp_inception_database import DbmpInceptionDatabase
from dbmp.models.dbmp_inception_business import DbmpInceptionBusiness
from dbmp.models.dbmp_inception_business_detail import DbmpInceptionBusinessDetail
from dbmp.views.sql_handler.s_dbmp_inception_business import SQLDbmpInceptionBusiness
from dbmp.views.sql_handler.s_dbmp_inception_business_detail import SQLDbmpInceptionBusinessDetail

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

@DecoratorTool.clean_alert_message
def index(request):
    """展示某个业务组的明细"""
    params = {}
    params['error_msg'] = []
    if request.method == 'GET':
        try:  
            # 获得传入的MySQL实例ID
            inception_business_id = int(request.GET.get('inception_business_id', '0'))  
        except ValueError:  
            logger.info(traceback.format_exc())
            inception_record_id = 0
            inception_database_id = 0

        if inception_business_id:
            try:
                # 审核业务组
                dbmp_inception_business = DbmpInceptionBusiness.objects.values(
                                        'inception_business_id',
                                        'inception_record_id',
                                        'mysql_business_id',).get(
                                     inception_business_id = inception_business_id)
                params['dbmp_inception_business'] = dbmp_inception_business
            except DbmpInceptionBusiness.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回点击编辑页面
                request.session['danger_msg'].append('对不起! 找不到指定的SQL审核数据')
                index_url = '{base_url}/index/'.format(
                                base_url = ViewUrlPath.path_dbmp_inception_record())
                return HttpResponseRedirect(index_url)

            try:
                # 业务组
                dbmp_mysql_business = DbmpMysqlBusiness.objects.values(
                                        'name',
                                        'remark').get(
                                     mysql_business_id = dbmp_inception_business.get('mysql_business_id', 0))
                params['dbmp_mysql_business'] = dbmp_mysql_business
            except DbmpMysqlBusiness.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回主页
                request.session['danger_msg'].append('对不起! 找不到指定的业务组')
                index_url = '{base_url}/index/'.format(
                                base_url = ViewUrlPath.path_dbmp_inception_record())
                return HttpResponseRedirect(index_url)

            try:
                # 序号审核的sql信息
                dbmp_inception_record = DbmpInceptionRecord.objects.get(
                                     inception_record_id = dbmp_inception_business.get('inception_record_id', 0))
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

            try:
                # 查找需要审核的业务组明细
                s_dbmp_inception_business_detail = SQLDbmpInceptionBusinessDetail()
                # 获得 DbmpInceptionBusinessDetail, DbmpInceptionInstance
                #      DbmpMysqlDatabase, DbmpMysqlInstance 信息
                dbmp_inception_business_details = s_dbmp_inception_business_detail.find_business_detail_by_business_id(
                                                                         inception_business_id)
                params['dbmp_inception_business_details'] = dbmp_inception_business_details
            except Exception, e:
                logger.info(traceback.format_exc())
                params['error_msg'].append('查找需要执行的业务组明细出错')

        return render(request, 'dbmp_inception_business_detail/index.html', params)

@DecoratorTool.clean_alert_message
def run_inception(request):
    """转调到执行SQL窗口"""
    params = {}
    params['error_msg'] = []

    if request.method == 'GET':
        try:  
            # 获得传入的MySQL实例ID
            inception_business_detail_id = int(request.GET.get('inception_business_detail_id', '0'))  
        except ValueError:  
            logger.info(traceback.format_exc())
            inception_record_id = 0
            inception_database_id = 0

        if not inception_business_detail_id:
            params['error_msg'].append('输入的inception_business_detail_id有问题') 

        try:
            # 查找需要审核的实例
            s_dbmp_inception_business_detail = SQLDbmpInceptionBusinessDetail()
            # 获得 DbmpInceptionBusinessDetail, DbmpMysqlDatabase, DbmpMysqlInstance 信息
            dbmp_inception_business_detail = s_dbmp_inception_business_detail.get_business_detail_by_id_1(
                                                                     inception_business_detail_id)
            print dbmp_inception_business_detail
            params['dbmp_inception_business_detail'] = dbmp_inception_business_detail

            if not dbmp_inception_business_detail:
                params['error_msg'].append('不能找到需要执行的数据库') 
            elif dbmp_inception_business_detail.get('execute_status') == 2:
                params['error_msg'].append('此SQL已经在该数据库执行过了') 
        except Exception, e:
            logger.info(traceback.format_exc())
            params['error_msg'].append('查找需要执行的业务组明细出错')

        return render(request, 'dbmp_inception_business_detail/run_inception.html', params)

def ajax_run_inception(request):
    """Ajax执行SQL"""
    params = {}
    params['is_ok'] = False
    params['inception_info'] = ''
    params['err_msg'] = ''

    if request.method == 'POST':
        try:
            inception_business_detail_id = int(request.POST.get('inception_business_detail_id', '0'))
            s_dbmp_inception_business_detail = SQLDbmpInceptionBusinessDetail()
            # 获得 DbmpInceptionBusinessDetail, DbmpInceptionRecord, DbmpInceptionInstance
            #      DbmpMysqlDatabase, DbmpMysqlInstance 信息
            dbmp_inception_business_detail = s_dbmp_inception_business_detail.get_business_detail_by_id_2(
                                                                     inception_business_detail_id)
            if not dbmp_inception_business_detail:
                logger.error('没有获取到执行SQL的业务组明细信息')
                params['err_msg'] = '没有获取到执行SQL的业务组明细信息'
                respons_data = json.dumps(params)
                return HttpResponse(respons_data, content_type='application/json')
        except:
            logger.error(traceback.format_exc())
            params['err_msg'] = '(获取执行SQL的业务组明细信息错误)'
            params['err_msg'] += traceback.format_exc()
            respons_data = json.dumps(params)
            return HttpResponse(respons_data, content_type='application/json')

        # 对SQL进行审核
        is_ok, inception_info = InceptionTool.inception_execute(
                                    inception_host = dbmp_inception_business_detail.get('inc_host', 0),
                                    inception_port = dbmp_inception_business_detail.get('inc_port', 0),
                                    mysql_user = dbmp_inception_business_detail.get('mysql_username', ''),
                                    mysql_password = dbmp_inception_business_detail.get('mysql_password', ''),
                                    mysql_host = dbmp_inception_business_detail.get('mysql_host', 0),
                                    mysql_port = dbmp_inception_business_detail.get('mysql_port', 0),
                                    db_name = dbmp_inception_business_detail.get('db_name', ''),
                                    sql_text = dbmp_inception_business_detail.get('sql_text', ''),
                                    charset = dbmp_inception_business_detail.get('charset', 'utf8'))
        # 更新执行业务组明细状态
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
            # 更新 dbmp_inception_business_detail 状态
            DbmpInceptionBusinessDetail.objects.filter(
                inception_business_detail_id = inception_business_detail_id).update(
                                            execute_status = execute_status)
        except Exception, e:
            logger.info(traceback.format_exc())
            logger.info('执行SQL成功, 但是更新失败执行sql业务组明细状态失败')
            params['err_msg'].append('执行SQL成功, 但是更新失败执行sql业务组明细状态失败')

        params['is_ok'] = is_ok
        params['execute_status'] = execute_status
        params['inception_info'] = inception_info

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')
