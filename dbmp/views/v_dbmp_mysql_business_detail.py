#-*- coding: utf-8 -*-

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
    sql_business_detail_handler = SQLDbmpMysqlBusinessDetail()
    sql_business_detail_handler.get_business_detail_index(1)
    return render(request, 'dbmp_mysql_business_detail/index.html', params)

@DecoratorTool.get_request_alert_message
def add(request):
    params = {}
    return render(request, 'dbmp_mysql_business_detail/add.html', params)

@DecoratorTool.get_request_alert_message
def ajax_delete(request):

    is_delete = False

    respons_data = json.dumps(is_delete)
    return HttpResponse(respons_data, content_type='application/json')
