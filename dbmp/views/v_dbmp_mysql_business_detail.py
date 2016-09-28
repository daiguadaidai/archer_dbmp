#-*- coding: utf-8 -*-

from django.db.models import Q
from django.db import transaction
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from common.util.pagination import Pagination
from common.util.view_url_path import ViewUrlPath
from common.util.decorator_tool import DecoratorTool
from dbmp.models.cmdb_os import CmdbOs
from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance
from dbmp.models.dbmp_mysql_business import DbmpMysqlBusiness
from dbmp.models.dbmp_mysql_business_detail import DbmpMysqlBusinessDetail
from dbmp.models.dbmp_mysql_database import DbmpMysqlDatabase
from dbmp.views.sql_handler.s_dbmp_mysql_business_detail import SQLDbmpMysqlBusinessDetail


import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

@DecoratorTool.get_request_alert_message
def index(request):
    params = {}
    mysql_business_id = int(request.GET.get('mysql_business_id', '0')) 
    params['mysql_business_id'] = mysql_business_id

    if request.method == 'GET':
        sql_business_detail_handler = SQLDbmpMysqlBusinessDetail()
        business_detail_index = sql_business_detail_handler.get_business_detail_index(
                                                                mysql_business_id)
        params['business_detail_index'] = business_detail_index
        return render(request, 'dbmp_mysql_business_detail/index.html', params)

@DecoratorTool.get_request_alert_message
def add(request):
    params = {}
    return render(request, 'dbmp_mysql_business_detail/add.html', params)

def ajax_get_detail_by_id(request):
    """获得业务数据库详细信息通过 mysql_business_detail_id"""

    mysql_business_detail = None
    if request.method == 'POST':
        mysql_business_id = int(request.POST.get('mysql_business_detail_id', '0'))
        sql_business_detail_handler = SQLDbmpMysqlBusinessDetail()
        # 通过 mysql_business_detail_id 获得详细数据
        mysql_business_detail = sql_business_detail_handler.get_business_detail_by_id(
                                                            mysql_business_detail_id)
    respons_data = json.dumps(mysql_business_detail)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_delete(request):

    is_delete = False

    respons_data = json.dumps(is_delete)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_update_database(request):
    """更新选中数据库"""
    is_ok = False

    if request.method == 'POST':
        mysql_business_id = int(request.POST.get('mysql_business_id', '0'))
        mysql_database_id = int(request.POST.get('mysql_database_id', '0'))
        update_tag = request.POST.get('update_tag', '')

        try:
            with transaction.atomic():
                if update_tag == 'add':
                    # # 添加DbmpMysqlInstance
                    dbmp_mysql_business_detail = DbmpMysqlBusinessDetail(
                                                     mysql_business_id = mysql_business_id,
                                                     mysql_database_id = mysql_database_id)
                    dbmp_mysql_business_detail.save()
                    is_ok = dbmp_mysql_business_detail.mysql_business_detail_id
                    logger.info('DbmpMysqlBusinessDetail 添加成功')
                elif update_tag == 'delete':
                    # 获得需要删除业务数据库
                    try:
                        dbmp_mysql_business_detail = DbmpMysqlBusinessDetail.objects.values(
                                                            'mysql_business_detail_id').get(
                                                  Q(mysql_business_id = mysql_business_id),
                                                  Q(mysql_database_id = mysql_database_id))
                        is_ok = dbmp_mysql_business_detail.get('mysql_business_detail_id', 0)
                    except DbmpMysqlBusinessDetail.DoesNotExist:
                        logger.error(traceback.format_exc())
                        logger.error('没有找到相关的业务数据库')
                        respons_data = json.dumps(is_ok)
                        return HttpResponse(respons_data, content_type='application/json')
                    
                    # 删除业务数据库
                    DbmpMysqlBusinessDetail.objects.filter(
                                 mysql_business_detail_id = is_ok).delete()
                    logger.info('DbmpMysqlBusinessDetail 删除成功')
        except IntegrityError, e:
            logger.error(traceback.format_exc())
            logger.error('添加失败')
            if e.args[0] == 1062:
                logger.error('需要添加的相关信息重复')
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('(添加/删除)失败, 执行数据库错误')

    respons_data = json.dumps(is_ok)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_has_database(request):
    """判断业务数据库是否存在"""
    is_ok = False

    if request.method == 'POST':
        mysql_business_id = int(request.POST.get('mysql_business_id', '0'))
        mysql_database_id = int(request.POST.get('mysql_database_id', '0'))

        try:
            count =DbmpMysqlBusinessDetail.objects.filter(
                     mysql_business_id = mysql_business_id).filter(
                     mysql_database_id = mysql_database_id).count()
            print count
            is_ok = count
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('获取DbmpMysqlBusinessDetail Count失败, 执行数据库错误')

    respons_data = json.dumps(is_ok)
    return HttpResponse(respons_data, content_type='application/json')
