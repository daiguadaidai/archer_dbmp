#-*- coding: utf-8 -*-

from django.shortcuts import render
from common.util.pagination import Pagination
# from dbmp.models.cmdb_os import CmdbOs
# from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance

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
    pass

def test(request):
    return render(request, 'test.html')
