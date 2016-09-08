#-*- coding: utf-8 -*-

from django.db import transaction
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from common.util.pagination import Pagination
from common.util.ip_tool import IpTool
from common.util.view_url_path import ViewUrlPath
from common.util.decorator_tool import DecoratorTool
from dbmp.models.cmdb_os import CmdbOs
from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance
from dbmp.models.dbmp_mysql_backup_instance import DbmpMysqlBackupInstance
from dbmp.models.dbmp_mysql_backup_remote import DbmpMysqlBackupRemote
from dbmp.views.forms.form_dbmp_mysql_backup_instance import AddForm
from dbmp.views.forms.form_dbmp_mysql_backup_instance import EditForm
from dbmp.views.forms.form_dbmp_mysql_backup_instance import AddHasRemoteForm
from dbmp.views.forms.form_dbmp_mysql_backup_instance import EditHasRemoteForm

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

# Create your views here.

@DecoratorTool.get_request_alert_message
def index(request):
    params = {}

    '''
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
    '''

@DecoratorTool.get_request_alert_message
def add(request):
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    if request.method == 'GET':
        mysql_instance_id = int(request.GET.get('mysql_instance_id', '0'))  
        try:
            # 1.获取MySQL实例
            dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                'mysql_instance_id',
                                                'username',
                                                'port',
                                                'host',).get(
                               mysql_instance_id = mysql_instance_id)
            params['dbmp_mysql_instance'] = dbmp_mysql_instance
        except DbmpMysqlInstance.DoesNotExist: # 没有获取到实例信息则转跳列表页面
            logger.info(traceback.format_exc())
            # 返回点击编辑页面
            request.session['danger_msg'].append('对不起! 找不到指定的MySQL实例')
            mysql_instnace_index_url = '{base_url}/index'.format(
                            base_url = ViewUrlPath.path_dbmp_mysql_instance())
            return HttpResponseRedirect(mysql_instnace_index_url)

        form = AddForm(
            initial = {
                'mysql_instance_id': mysql_instance_id
            }
        )
        params['form'] = form

        return render(request, 'dbmp_mysql_backup_instance/add.html', params)

    ####################################################################
    # POST 请求
    ####################################################################
    if request.method == 'POST':
        mysql_instance_id = int(request.POST.get('mysql_instance_id', 0))
        try:
            # 1.获取MySQL实例
            dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                'mysql_instance_id',
                                                'username',
                                                'port',
                                                'host',).get(
                               mysql_instance_id = mysql_instance_id)
            params['dbmp_mysql_instance'] = dbmp_mysql_instance
        except DbmpMysqlInstance.DoesNotExist: # 没有获取到实例信息则转跳列表页面
            logger.info(traceback.format_exc())
            # 返回点击编辑页面
            request.session['danger_msg'].append('对不起! 找不到指定的MySQL实例')
            mysql_instnace_index_url = '{base_url}/index'.format(
                            base_url = ViewUrlPath.path_dbmp_mysql_instance())
            return HttpResponseRedirect(mysql_instnace_index_url)

        # 通过判断是否使用将备份传输至远程来创建不同的 form 对象
        is_to_remote = int(request.POST.get('is_to_remote', 0))
        if is_to_remote:
            os_id = request.POST.get('os_id', 0)

            form = AddHasRemoteForm(request.POST)

            try: # 如果有设置远程备份则获取相关OS
                cmdb_os = CmdbOs.objects.values('hostname',
                                                'ip',
                                                'alias').get(os_id = os_id)
                params['cmdb_os'] = cmdb_os
            except CmdbOs.DoesNotExist: # 如果获取相关操作系统失败放回添加页面
                params['form'] = form
                logger.info(traceback.format_exc())
                # 如果MySQL实例没有指定OS则告警
                request.session['alert_message_now']['danger_msg'].append(
                                                    '开启了远程备份，却没有选择相关OS')
                return render(request, 'dbmp_mysql_backup_instance/add.html', params)
        else: 
            form = AddForm(request.POST)
  
        params['form'] = form


        # 验证表单
        if form.is_valid():
            mysql_instance_id = form.cleaned_data['mysql_instance_id']
            backup_tool = form.cleaned_data['backup_tool']
            backup_type = form.cleaned_data['backup_type']
            is_all_instance = form.cleaned_data['is_all_instance']
            is_binlog = form.cleaned_data['is_binlog']
            is_compress = form.cleaned_data['is_compress']
            is_to_remote = form.cleaned_data['is_to_remote']
            backup_dir = form.cleaned_data['backup_dir']
            backup_name = form.cleaned_data['backup_name']
            backup_tool_file = form.cleaned_data['backup_tool_file']
            backup_tool_param = form.cleaned_data['backup_tool_param']

            try:
                with transaction.atomic():
                    # 插入dbmp_mysql_backup_instance数据
                    dbmp_mysql_backup_instance = DbmpMysqlBackupInstance(
                                                     mysql_instance_id = mysql_instance_id,
                                                     backup_tool = backup_tool,
                                                     backup_type = backup_type,
                                                     is_all_instance = is_all_instance,
                                                     is_binlog = is_binlog,
                                                     is_compress = is_compress,
                                                     is_to_remote = is_to_remote,
                                                     backup_dir = backup_dir,
                                                     backup_tool_file = backup_tool_file,
                                                     backup_tool_param = backup_tool_param,
                                                     backup_name = backup_name)
                    dbmp_mysql_backup_instance.save()

                    # 如果指定了远程传输备份, 插入数据 dbmp_mysql_backup_remote
                    if is_to_remote:
                        # 备份发送远程相关参数
                        os_id = form.cleaned_data['os_id']
                        remote_dir = form.cleaned_data['remote_dir']
                        DbmpMysqlBackupRemote.objects.create(
                                            mysql_backup_instance_id = dbmp_mysql_backup_instance.mysql_backup_instance_id,
                                            mysql_instance_id = mysql_instance_id,
                                            os_id = os_id,
                                            remote_dir = remote_dir)

                # 保存成功转跳到View页面
                request.session['success_msg'].append('备份设置成功')
                view_url = '{base_url}/view/?mysql_instance_id={id}'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_backup_instance(),
                                id = mysql_instance_id)

                return HttpResponseRedirect(view_url)
            except IntegrityError, e:
                logger.info(traceback.format_exc())
                request.session['danger_msg'].append('添加失败')
                if e.args[0] == 1062:
                    request.session['alert_message_now']['danger_msg'].append(
                                                             '需要添加的相关信息重复')
                request.session['alert_message_now']['danger_msg'].append(e.args)
                return render(request, 'dbmp_mysql_backup_instance/add.html', params)
            except Exception, e:
                logger.info(traceback.format_exc())
                # 保存失败转跳会原页面
                request.session['alert_message_now']['danger_msg'].append(
                                                        '添加失败, 保存数据库错误')
                return render(request, 'dbmp_mysql_backup_instance/add.html', params)
        else: # 表单验证失败
            request.session['alert_message_now']['danger_msg'].append(
                                                     '添加失败, 表单验证失败')
            # form danger信息
            for label, msgs in form.errors.items():
                for msg in msgs:
                    request.session['alert_message_now']['danger_msg'].append(msg)

            return render(request, 'dbmp_mysql_backup_instance/add.html', params)

@DecoratorTool.get_request_alert_message
def edit(request):
    params = {}
    ####################################################################
    # GET 请求
    ####################################################################
    # 点击链接转跳到编辑页面
    if request.method == 'GET':
        # 初始化 form
        form_data = {}

        # 获取MySQL实例ID
        mysql_instance_id = int(request.GET.get('mysql_instance_id', '0'))  

        if mysql_instance_id:
            try:
                # 1.获取MySQL实例
                dbmp_mysql_instance = DbmpMysqlInstance.objects.get(
                                     mysql_instance_id = mysql_instance_id)
                params['dbmp_mysql_instance'] = dbmp_mysql_instance
            except DbmpMysqlInstance.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回点击编辑页面
                request.session['danger_msg'].append('对不起! 找不到指定的MySQL实例')
                return HttpResponseRedirect(request.environ['HTTP_REFERER'])

            # 2.获取MySQL备份信息
            try:
                dbmp_mysql_backup_instance = DbmpMysqlBackupInstance.objects.get(
                       mysql_instance_id = dbmp_mysql_instance.mysql_instance_id)
                # params['dbmp_mysql_backup_instance'] = dbmp_mysql_backup_instance
            except DbmpMysqlBackupInstance.DoesNotExist: # 如果没有查到备份设置信息则转跳到添加备份设置信息页面
                request.session['alert_message_now']['warning_msg'].append(
                                                   '您还未为该MySQL实例设置备份策略, 请进行编辑')
                add_url = '{base_url}/add/?mysql_instance_id={id}'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_backup_instance(),
                                id = dbmp_mysql_instance.mysql_instance_id)
                return HttpResponseRedirect(add_url)

            # 3.远程信息
            if dbmp_mysql_backup_instance.is_to_remote == 1:
                try: # 远程备份信息
                    dbmp_mysql_backup_remote = DbmpMysqlBackupRemote.objects.get(
                                               mysql_instance_id = dbmp_mysql_instance.mysql_instance_id)
                    # params['dbmp_mysql_backup_remote'] = dbmp_mysql_backup_remote
                except CmdbOs.DoesNotExist:
                    logger.info(traceback.format_exc())
                    # 如果MySQL实例没有指定OS则告警
                    request.session['alert_message_now']['wraning_msg'].append(
                                                        '设置了远程备份却没有设置远程信息，请修改')
                try: # 如果有设置远程备份则获取相关OS
                    cmdb_os = CmdbOs.objects.values('hostname',
                                                    'ip',
                                                    'alias').get(os_id = dbmp_mysql_backup_remote.os_id)
                    params['cmdb_os'] = cmdb_os
                except CmdbOs.DoesNotExist: # 如果获取相关操作系统失败放回添加页面
                    logger.info(traceback.format_exc())
                    # 如果MySQL实例没有指定OS则告警
                    request.session['alert_message_now']['warning_msg'].append(
                                                        '设置了远程备份却找不到远程OS，请修改')

            # 将信息都添加到 form 中
            form_data['mysql_instance_id'] = str(dbmp_mysql_instance.mysql_instance_id)
            form_data['mysql_backup_instance_id'] = str(dbmp_mysql_backup_instance.mysql_backup_instance_id)
            form_data['backup_tool'] = str(dbmp_mysql_backup_instance.backup_tool)
            form_data['backup_type'] = str(dbmp_mysql_backup_instance.backup_type)
            form_data['is_all_instance'] = str(dbmp_mysql_backup_instance.is_all_instance)
            form_data['is_binlog'] = str(dbmp_mysql_backup_instance.is_binlog)
            form_data['is_compress'] = str(dbmp_mysql_backup_instance.is_compress)
            form_data['backup_dir'] = str(dbmp_mysql_backup_instance.backup_dir)
            form_data['backup_name'] = str(dbmp_mysql_backup_instance.backup_name)
            form_data['backup_tool_file'] = str(dbmp_mysql_backup_instance.backup_tool_file)
            form_data['backup_tool_param'] = str(dbmp_mysql_backup_instance.backup_tool_param)
            form_data['is_to_remote'] = str(dbmp_mysql_backup_instance.is_to_remote)
            
            # 更具是否有开启远程来生成form
            if dbmp_mysql_backup_instance.is_to_remote == 1: # 开启远程
                form_data['mysql_backup_remote_id'] = str(dbmp_mysql_backup_remote.mysql_backup_remote_id)
                form_data['os_id'] = str(dbmp_mysql_backup_remote.os_id)
                form_data['remote_dir'] = str(dbmp_mysql_backup_remote.remote_dir)

                form = EditHasRemoteForm(initial = form_data)
                params['form'] = form
            else: # 没开启远程
                form = EditForm(initial = form_data)
                params['form'] = form

            return render(request, 'dbmp_mysql_backup_instance/edit.html', params)
        else:
            request.session['danger_msg'] = '对不起! 找不到指定的MySQL实例!'
            # 返回点击编辑页面
            return HttpResponseRedirect(request.environ['HTTP_REFERER'])


    ####################################################################
    # POST 请求
    ####################################################################
    # 修改操作
    if request.method == 'POST':
        mysql_instance_id = int(request.POST.get('mysql_instance_id', 0))
        try:
            # 1.获取MySQL实例
            dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                'mysql_instance_id',
                                                'username',
                                                'port',
                                                'host',).get(
                               mysql_instance_id = mysql_instance_id)
            params['dbmp_mysql_instance'] = dbmp_mysql_instance
        except DbmpMysqlInstance.DoesNotExist: # 没有获取到实例信息则转跳列表页面
            logger.info(traceback.format_exc())
            # 返回点击编辑页面
            request.session['danger_msg'].append('对不起! 找不到指定的MySQL实例')
            mysql_instnace_index_url = '{base_url}/index'.format(
                            base_url = ViewUrlPath.path_dbmp_mysql_instance())
            return HttpResponseRedirect(mysql_instnace_index_url)

        # 通过判断是否使用将备份传输至远程来创建不同的 form 对象
        is_to_remote = int(request.POST.get('is_to_remote', 0))
        if is_to_remote:
            os_id = request.POST.get('os_id', 0)

            form = EditHasRemoteForm(request.POST)

            try: # 如果有设置远程备份则获取相关OS
                cmdb_os = CmdbOs.objects.values('hostname',
                                                'ip',
                                                'alias').get(os_id = os_id)
                params['cmdb_os'] = cmdb_os
            except CmdbOs.DoesNotExist: # 如果获取相关操作系统失败放回添加页面
                params['form'] = form
                logger.info(traceback.format_exc())
                # 如果MySQL实例没有指定OS则告警
                request.session['alert_message_now']['danger_msg'].append(
                                                    '开启了远程备份，却没有选择相关OS')
                return render(request, 'dbmp_mysql_backup_instance/edit.html', params)
        else: 
            form = EditForm(request.POST)
  
        params['form'] = form

        # 验证表单
        if form.is_valid():
            mysql_instance_id = form.cleaned_data['mysql_instance_id']
            mysql_backup_instance_id = form.cleaned_data['mysql_backup_instance_id']
            mysql_backup_remote_id = form.cleaned_data['mysql_backup_remote_id']
            backup_tool = form.cleaned_data['backup_tool']
            backup_type = form.cleaned_data['backup_type']
            is_all_instance = form.cleaned_data['is_all_instance']
            is_binlog = form.cleaned_data['is_binlog']
            is_compress = form.cleaned_data['is_compress']
            is_to_remote = form.cleaned_data['is_to_remote']
            backup_dir = form.cleaned_data['backup_dir']
            backup_name = form.cleaned_data['backup_name']
            backup_tool_file = form.cleaned_data['backup_tool_file']
            backup_tool_param = form.cleaned_data['backup_tool_param']

            try:
                with transaction.atomic():
                    # 插入dbmp_mysql_backup_instance数据
                    DbmpMysqlBackupInstance.objects.filter(
                        mysql_backup_instance_id = mysql_backup_instance_id).update(
                                           mysql_instance_id = mysql_instance_id,
                                           backup_tool = backup_tool,
                                           backup_type = backup_type,
                                           is_all_instance = is_all_instance,
                                           is_binlog = is_binlog,
                                           is_compress = is_compress,
                                           is_to_remote = is_to_remote,
                                           backup_dir = backup_dir,
                                           backup_tool_file = backup_tool_file,
                                           backup_tool_param = backup_tool_param,
                                           backup_name = backup_name)

                    # 远程备份信息相关判断和操作
                    if is_to_remote and mysql_backup_remote_id: # 设置远程并且之前添加过远程信息(修改远程信息)
                        # 备份发送远程相关参数
                        os_id = form.cleaned_data['os_id']
                        remote_dir = form.cleaned_data['remote_dir']
                        DbmpMysqlBackupRemote.objects.filter(
                                mysql_backup_remote_id = mysql_backup_remote_id).update(
                                     mysql_backup_instance_id = mysql_backup_instance_id,
                                     mysql_instance_id = mysql_instance_id,
                                     os_id = os_id,
                                     remote_dir = remote_dir)
                    elif is_to_remote and not mysql_backup_remote_id: # 如果设置远程并且之前没添加过(创建远程信息)
                        # 备份发送远程相关参数
                        os_id = form.cleaned_data['os_id']
                        remote_dir = form.cleaned_data['remote_dir']
                        DbmpMysqlBackupRemote.objects.create(
                                            mysql_backup_instance_id = mysql_backup_instance_id,
                                            mysql_instance_id = mysql_instance_id,
                                            os_id = os_id,
                                            remote_dir = remote_dir)
                        request.session['success_msg'].append('新增备份远程信息')
                    elif not is_to_remote and mysql_backup_remote_id: # 如果没设置远程并且之前添加过(删除远程信息)
                        DbmpMysqlBackupRemote.objects.filter(
                                    mysql_backup_remote_id = mysql_backup_remote_id).delete()
                        request.session['warning_msg'].append('备份远程信息已经删除')
                        logger.info('delete DbmpMysqlBackupInfo: {id}'.format(id=mysql_backup_remote_id))
                    elif not is_to_remote and not mysql_backup_remote_id: # 如果没设置远程并且之前没添加过(不处理)
                        pass

                # 保存成功转跳到View页面
                request.session['success_msg'].append('备份设置修改成功')
                view_url = '{base_url}/view/?mysql_instance_id={id}'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_backup_instance(),
                                id = mysql_instance_id)

                return HttpResponseRedirect(view_url)
            except IntegrityError, e:
                logger.info(traceback.format_exc())
                request.session['danger_msg'].append('修改失败')
                if e.args[0] == 1062:
                    request.session['alert_message_now']['danger_msg'].append(
                                                             '需要修改的相关信息重复')
                request.session['alert_message_now']['danger_msg'].append(e.args)
                return render(request, 'dbmp_mysql_backup_instance/edit.html', params)
            except Exception, e:
                logger.info(traceback.format_exc())
                # 保存失败转跳会原页面
                request.session['alert_message_now']['danger_msg'].append(
                                                        '修改失败, 保存数据库错误')
                return render(request, 'dbmp_mysql_backup_instance/edit.html', params)
        else: # 表单验证失败
            request.session['alert_message_now']['danger_msg'].append(
                                                     '修改失败, 表单验证失败')
            # form danger信息
            for label, msgs in form.errors.items():
                for msg in msgs:
                    request.session['alert_message_now']['danger_msg'].append(msg)

            return render(request, 'dbmp_mysql_backup_instance/edit.html', params)

@DecoratorTool.get_request_alert_message
def view(request):
    params = {}

    ####################################################################
    # GET 请求
    ####################################################################
    # 点击链接转跳到编辑页面
    if request.method == 'GET':
        # 获取MySQL实例ID
        mysql_instance_id = int(request.GET.get('mysql_instance_id', '0'))  

        if mysql_instance_id:

            try:
                # 1.获取MySQL实例
                dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                    'mysql_instance_id',
                                                    'run_status',
                                                    'username',
                                                    'password',
                                                    'port',
                                                    'host',).get(
                                   mysql_instance_id = mysql_instance_id)
                params['dbmp_mysql_instance'] = dbmp_mysql_instance
            except DbmpMysqlInstance.DoesNotExist:
                logger.info(traceback.format_exc())
                # 返回编辑页面
                request.session['danger_msg'].append('对不起! 找不到指定的MySQL实例')
                # 定义错误返回编辑页面链接
                index_url = '{base_url}/index'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_instance())
                return HttpResponseRedirect(index_url)

            # 2.获取MySQL备份设置信息
            try:
                dbmp_mysql_backup_instance = DbmpMysqlBackupInstance.objects.get(
                                                mysql_instance_id = mysql_instance_id)
                params['dbmp_mysql_backup_instance'] = dbmp_mysql_backup_instance
            except DbmpMysqlBackupInstance.DoesNotExist:
                logger.info(traceback.format_exc())
                request.session['danger_msg'].append('对不起! 您还没有设置实例备份信息')
                add_url = '{base_url}/add/?mysql_instance_id={id}'.format(
                                base_url = ViewUrlPath.path_dbmp_mysql_backup_instance(),
                                id = mysql_instance_id)
                return HttpResponseRedirect(add_url)

            # 3.获得远程备份信息
            if dbmp_mysql_backup_instance.is_to_remote:
                # 获得 备份远程信息
                try:
                    dbmp_mysql_backup_remote = DbmpMysqlBackupRemote.objects.get(
                                                mysql_instance_id = mysql_instance_id)
                    params['dbmp_mysql_backup_remote'] = dbmp_mysql_backup_remote
                except CmdbOs.DoesNotExist:
                    logger.info(traceback.format_exc())
                    request.session['danger_msg'].append('对不起! 设置了远程备份却没有找到远程的相关设置')
                    return HttpResponseRedirect(edit_url)

                # 获得 OS 信息
                try:
                    cmdb_os = CmdbOs.objects.get(os_id = dbmp_mysql_backup_remote.os_id)
                    params['cmdb_os'] = cmdb_os
                except CmdbOs.DoesNotExist:
                    logger.info(traceback.format_exc())
                    request.session['danger_msg'].append('对不起! 找不到你指定的远程备份主机')
                    edit_url = '{base_url}/edit/?mysql_instance_id={id}'.format(
                                    base_url = ViewUrlPath.path_dbmp_mysql_backup_instance(),
                                    id = mysql_instance_id)
                    return HttpResponseRedirect(edit_url)

            return render(request, 'dbmp_mysql_backup_instance/view.html', params)
        else:
            # MySQL实例列表页
            request.session['danger_msg'].append('对不起! 没有指定正确的MySQL实例ID!')
            index_url = '{base_url}/index'.format(
                            base_url = ViewUrlPath.path_dbmp_mysql_instance())
            return HttpResponseRedirect(index_url)

# @DecoratorTool.get_request_alert_message
def ajax_delete(request):
    """ajax 的方式删除MySQL备份信息"""

    is_delete = False

    if request.method == 'POST':
        mysql_backup_instance_id = int(request.POST.get('mysql_backup_instance_id', '0'))  
        mysql_backup_remote_id = int(request.POST.get('mysql_backup_remote_id', '0'))  
        try:
            with transaction.atomic():
                if mysql_backup_instance_id and mysql_backup_remote_id: 
                    # 有设置备份和远程信息(删除备份信息, 删除远程信息)
                    # 删除备份信息
                    DbmpMysqlBackupInstance.objects.filter(
                                mysql_backup_instance_id = mysql_backup_instance_id).delete()
                    logger.info('delete DbmpMysqlBackupInstance: {id}'.format(id = mysql_backup_instance_id))

                    # 删除远程信息
                    DbmpMysqlBackupRemote.objects.filter(
                                mysql_backup_remote_id = mysql_backup_remote_id).delete()
                    logger.info('delete DbmpMysqlBackupRemote: {id}'.format(id = mysql_backup_remote_id))
                    is_delete = True
                elif mysql_backup_instance_id and not mysql_backup_remote_id: 
                    # 有设置备份和无远程信息(删备份信息)
                    # 删除备份信息
                    DbmpMysqlBackupInstance.objects.filter(
                                mysql_backup_instance_id = mysql_backup_instance_id).delete()
                    logger.info('delete DbmpMysqlBackupInstance: {id}'.format(id = mysql_backup_instance_id))
                    is_delete = True
                elif not mysql_backup_instance_id and mysql_backup_remote_id: 
                    # 有设置备份和无远程信息(删除远程信息)
                    # 删除远程信息
                    DbmpMysqlBackupRemote.objects.filter(
                                mysql_backup_remote_id = mysql_backup_remote_id).delete()
                    logger.info('delete DbmpMysqlBackupRemote: {id}'.format(id = mysql_backup_remote_id))
                    is_delete = True
                elif not mysql_backup_instance_id and not mysql_backup_remote_id: 
                    # 无设置备份和无远程信息(不错处理)
                    pass

        except Exception, e:
            logger.info(traceback.format_exc())

    respons_data = json.dumps(is_delete)
    return HttpResponse(respons_data, content_type='application/json')
