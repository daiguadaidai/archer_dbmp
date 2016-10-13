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

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

def ajax_find_by_inception_record_id(request):
    """Ajax添加审核记录"""
    params = {}
    params['is_ok'] = False
    params['err_msg'] = ''

    if request.method == 'POST':
        try:
            inception_record_id = int(request.POST.get('inception_record_id', '0'))
            print inception_record_id
            s_dbmp_inception_business = SQLDbmpInceptionBusiness()
            dbmp_inception_businesses = s_dbmp_inception_business.find_businesses_by_inception_record_id(
                                                                     inception_record_id)
            params['is_ok'] = True
            params['databases'] = dbmp_inception_databases
        except:
            logger.error(traceback.format_exc())
            params['err_msg'] = traceback.format_exc()

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')
