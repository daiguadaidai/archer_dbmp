#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from common.util.pagination import Pagination
from common.util.view_url_path import ViewUrlPath
import simplejson as json
# from dbmp.models.cmdb_os import CmdbOs
from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance

# Create your views here.

def home(request):
    return render(request, 'home.html')

def index(request):
    params = {}

    try:  
        cur_page = int(request.GET.get('cur_page', '1'))  
    except ValueError:  
        cur_page = 1  
  
    # 创建分页数据
    pagination = Pagination.create_pagination(
                             from_name='dbmp.models.dbmp_mysql_instance', 
                             model_name='DbmpMysqlInstance',
                             cur_page=cur_page,
                             start_page_omit_symbol = '...',
                             end_page_omit_symbol = '...',
                             one_page_data_size=10,
                             show_page_item_len=9)
    # 获得MySQL实例列表
    params['pagination'] = pagination
    
    return render(request, 'dbmp_mysql_instance/index.html', params)

def add(request):
    pass

def view(request):
    pass

def edit(request):
    pass

def delete(request):
    try:  
        cur_page = int(request.GET.get('cur_page', '1'))  
        mysql_instance_id = int(request.GET.get('mysql_instance_id', '0'))  
    except ValueError:  
        cur_page = 1  

    redirect_url = '{path}/index?cur_page={cur_page}'.format(
                   path = ViewUrlPath.path_dbmp_mysql_instance(),
                   cur_page = cur_page)
    return HttpResponseRedirect(redirect_url)

def ajax_delete(request):
    """ajax 的方式删除MySQL实例"""

    is_delete = False
    if request.method == 'POST':
        mysql_instance_id = int(request.POST.get('mysql_instance_id', '0'))  
        if mysql_instance_id:
            DbmpMysqlInstance.objects.filter(
                            mysql_instance_id = mysql_instance_id).delete()
            is_delete = True

    respons_data = json.dumps(is_delete)
    return HttpResponse(respons_data, content_type='application/json')

def test(request):
    return render(request, 'test.html')
