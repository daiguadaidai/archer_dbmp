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
from dbmp.models.dbmp_mysql_database import DbmpMysqlDatabase
from dbmp.views.forms.form_dbmp_mysql_instance import AddForm
from dbmp.views.forms.form_dbmp_mysql_instance import EditForm

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

@DecoratorTool.get_request_alert_message
def index(request):
    return render(request, 'dbmp_mysql_database/index.html', params)

@DecoratorTool.get_request_alert_message
def add(request):
    return render(request, 'dbmp_mysql_database/add.html', params)

@DecoratorTool.get_request_alert_message
def edit(request):
    return render(request, 'dbmp_mysql_database/edit.html', params)

@DecoratorTool.get_request_alert_message
def view(request):
    return render(request, 'dbmp_mysql_database/view.html', params)

@DecoratorTool.get_request_alert_message
def delete(request):
    return render(request, 'dbmp_mysql_database/index.html', params)
