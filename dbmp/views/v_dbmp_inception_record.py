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
from dbmp.models.dbmp_mysql_business import DbmpMysqlBusiness
from dbmp.models.dbmp_mysql_database import DbmpMysqlDatabase
from dbmp.models.dbmp_inception_instance import DbmpInceptionInstance

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

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

def ajax_check(request):
    """对SQL进行审核"""
    params = {}
    params['is_ok'] = False
    # if request.method == 'POST':
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
            respons_data = json.dumps(params)
            return HttpResponse(respons_data, content_type='application/json')

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
        print is_ok, inception_info
        params['is_ok'] = is_ok
        params['inception_info'] = inception_info
    except:
        logger.error(traceback.format_exc())
     

    respons_data = json.dumps(params)
    return HttpResponse(respons_data, content_type='application/json')

'''
@DecoratorTool.get_request_alert_message
def add(request):
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    if request.method == 'GET':
        form = AddForm()
        params['form'] = form

        return render(request, 'dbmp_mysql_business/add.html', params)

   ####################################################################
    # POST 请求
    ####################################################################
    if request.method == 'POST':
        form = AddForm(request.POST)
        params['form'] = form

        print form

        # 验证表单
        if form.is_valid():
            name = form.cleaned_data['name']
            remark = form.cleaned_data['remark']

            try:
                with transaction.atomic():
                    # 添加DbmpMysqlBusiness
                    dbmp_mysql_business = DbmpMysqlBusiness(
                                                     name = name,
                                                     remark = remark)
                    dbmp_mysql_business.save()

                # 保存成功转跳到View页面
                request.session['success_msg'].append('添加成功')
                view_url = '{base_url}/index/?mysql_business_id={id}'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_business(),
                                id = dbmp_mysql_business.mysql_business_id)

                return HttpResponseRedirect(view_url)
            except IntegrityError, e:
                logger.info(traceback.format_exc())
                request.session['danger_msg'].append('添加失败')
                if e.args[0] == 1062:
                    request.session['alert_message_now']['danger_msg'].append(
                                                             '需要添加的相关信息重复')
                request.session['alert_message_now']['danger_msg'].append(e.args)
                return render(request, 'dbmp_mysql_business/add.html', params)
            except Exception, e:
                logger.info(traceback.format_exc())
                # 保存失败转跳会原页面
                request.session['alert_message_now']['danger_msg'].append(
                                                        '添加失败, 保存数据库错误')
                return render(request, 'dbmp_mysql_business/add.html', params)
        else: # 表单验证失败
            request.session['alert_message_now']['danger_msg'].append(
                                                     '添加失败, 表单验证失败')
            # form danger信息
            for label, msgs in form.errors.items():
                for msg in msgs:
                    request.session['alert_message_now']['danger_msg'].append(msg)

            return render(request, 'dbmp_mysql_business/add.html', params)

@DecoratorTool.get_request_alert_message
def edit(request):
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    # 点击链接转跳到编辑页面
    if request.method == 'GET':
        # 获取MySQL实例ID
        mysql_business_id = int(request.GET.get('mysql_business_id', '0'))  

        if mysql_business_id:
            try:
                # 1.获取MySQL实例
                dbmp_mysql_business = DbmpMysqlBusiness.objects.get(
                                     mysql_business_id = mysql_business_id)
                params['dbmp_mysql_business'] = dbmp_mysql_business


                return render(request, 'dbmp_mysql_business/edit.html', params)
            except DbmpMysqlBusiness.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回点击编辑页面
                request.session['danger_msg'].append('对不起! 找不到指定的业务组')
                return HttpResponseRedirect(request.environ['HTTP_REFERER'])
        else:
            request.session['danger_msg'] = '对不起! 找不到指定的业务组!'
            # 返回点击编辑页面
            return HttpResponseRedirect(request.environ['HTTP_REFERER'])



    ####################################################################
    # POST 请求
    ####################################################################
    # 修改操作
    if request.method == 'POST':
        form = EditForm(request.POST)

        # 验证表单
        if form.is_valid():
            mysql_business_id = form.cleaned_data['mysql_business_id']
            name = form.cleaned_data['name']
            remark = form.cleaned_data['remark']
            try:
                with transaction.atomic():
                    # 更新DbmpMysqlBusiness
                    DbmpMysqlBusiness.objects.filter(
                        mysql_business_id = mysql_business_id).update(
                                                           name = name,
                                                           remark = remark)
                # 保存成功转跳到View页面
                request.session['success_msg'].append('修改成功')
                view_url = '{base_url}/index/?mysql_business_id={id}'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_business(),
                                id = mysql_business_id)
                return HttpResponseRedirect(view_url)
            except IntegrityError, e:
                logger.info(traceback.format_exc())
                request.session['danger_msg'].append('编辑失败')
                if e.args[0] == 1062:
                    request.session['danger_msg'].append('需要修改的相关信息重复')

                request.session['danger_msg'].append(e.args)
                return HttpResponseRedirect(request.environ['HTTP_REFERER'])
            except Exception, e:
                logger.info(traceback.format_exc())
                # 保存失败转跳会原页面
                request.session['danger_msg'].append('编辑失败, 保存数据库错误')
                return HttpResponseRedirect(request.environ['HTTP_REFERER'])
        else: # 表单验证失败
            request.session['danger_msg'].append('编辑失败, 表单验证失败')
            request.session['form_danger_message'] = form.errors
            return HttpResponseRedirect(request.environ['HTTP_REFERER'])

@DecoratorTool.get_request_alert_message
def view(request):
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    # 点击链接转跳到编辑页面
    if request.method == 'GET':
        # 获取业务组
        mysql_business_id = int(request.GET.get('mysql_business_id', '0'))  

        if mysql_business_id:
            try:
                # 1.业务组
                dbmp_mysql_business = DbmpMysqlBusiness.objects.get(
                                     mysql_business_id = mysql_business_id)
                params['dbmp_mysql_business'] = dbmp_mysql_business

                return render(request, 'dbmp_mysql_business/view.html', params)
            except DbmpMysqlInstance.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回点击编辑页面
                request.session['danger_msg'].append('对不起! 找不到指定的业务组')
                return HttpResponseRedirect(request.environ['HTTP_REFERER'])
        else:
            request.session['danger_msg'] = '对不起! 找不到指定的业务组!'
            # 返回点击编辑页面
            return HttpResponseRedirect(request.environ['HTTP_REFERER'])

@DecoratorTool.get_request_alert_message
def delete(request):
    return render(request, 'dbmp_mysql_database/index.html', params)

@DecoratorTool.get_request_alert_message
def ajax_delete(request):

    is_delete = False
    if request.method == 'POST':
        mysql_business_id = int(request.POST.get('mysql_business_id', '0'))  
        if mysql_business_id:
            try:
                with transaction.atomic():
                    DbmpMysqlBusiness.objects.filter(
                                mysql_business_id = mysql_business_id).delete()
                    logger.info('delete DbmpMysqlBusiness')

                is_delete = True
            except Exception, e:
                logger.info(traceback.format_exc())

    respons_data = json.dumps(is_delete)
    return HttpResponse(respons_data, content_type='application/json')
'''
