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
from dbmp.views.sql_handler.s_dbmp_inception_business import SQLDbmpInceptionBusiness
from dbmp.views.sql_handler.s_dbmp_inception_business_detail import SQLDbmpInceptionBusinessDetail

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
            inception_business_id = int(request.GET.get('inception_business_id', '0'))  
        except ValueError:  
            logger.info(traceback.format_exc())
            inception_record_id = 0
            inception_business_id = 0

        if not inception_record_id or not inception_business_id:
            params['error_msg'].append('输入的inception_record_id, inception_business_id有问题') 

        try:
            # 查找需要审核的实例
            s_dbmp_inception_business = SQLDbmpInceptionBusiness()
            # DbmpInceptionBusiness, DbmpMysqlBusiness 信息
            dbmp_inception_business = s_dbmp_inception_business.get_business_by_id(
                                                                     inception_business_id)
            params['dbmp_inception_business'] = dbmp_inception_business

            if not dbmp_inception_business:
                params['error_msg'].append('不能找到需要执行的业务组') 
            elif dbmp_inception_business.get('execute_status') == 2:
                params['error_msg'].append('此SQL已经在该数据库执行过了') 
            elif dbmp_inception_business.get('execute_status') == 4:
                params['error_msg'].append('此SQL已经在该业务组执行过了(部分)') 
        except Exception, e:
            logger.info(traceback.format_exc())
            params['error_msg'].append('查找需要执行的业务组有错')

        # 获得审核业务组明细
        try:
            # 查找需要审核明细
            s_dbmp_inception_business_detail = SQLDbmpInceptionBusinessDetail()
            # DbmpInceptionBusinessDetail, DbmpMysqlBusiness, DbmpMysqlDatabase
            # DbmpMysqlInstance 信息
            dbmp_inception_business_details = s_dbmp_inception_business_detail.find_need_inception_detail_by_business_id(
                                                                     inception_business_id)
            params['dbmp_inception_business_details'] = dbmp_inception_business_details

            if not dbmp_inception_business_details:
                params['error_msg'].append('没有需要执行的业务组明细') 
        except Exception, e:
            logger.info(traceback.format_exc())
            params['error_msg'].append('查找需要执行的业务组明细')

        return render(request, 'dbmp_inception_business/run_inception.html', params)

def ajax_find_by_inception_record_id(request):
    """Ajax添加审核记录"""
    params = {}
    params['is_ok'] = False
    params['err_msg'] = ''

    if request.method == 'POST':
        try:
            inception_record_id = int(request.POST.get('inception_record_id', '0'))
            s_dbmp_inception_business = SQLDbmpInceptionBusiness()
            dbmp_inception_businesses = s_dbmp_inception_business.find_businesses_by_inception_record_id(
                                                                     inception_record_id)
            params['is_ok'] = True
            params['businesses'] = dbmp_inception_businesses
        except:
            logger.error(traceback.format_exc())
            params['err_msg'] = traceback.format_exc()

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_change_execute_status(request):
    """Ajax修改业务组执行状态"""
    params = {}
    params['is_ok'] = False
    params['err_msg'] = ''

    if request.method == 'POST':
        try:
            inception_business_id = int(request.POST.get('inception_business_id', '0'))
            execute_status = int(request.POST.get('execute_status', '1'))
            
            # 更新 dbmp_inception_business 状态
            DbmpInceptionBusiness.objects.filter(
                inception_business_id = inception_business_id).update(
                                            execute_status = execute_status)
            params['is_ok'] = True
        except:
            logger.error(traceback.format_exc())
            params['err_msg'] += '修改业务组状态失败'
            params['err_msg'] += traceback.format_exc()

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')
