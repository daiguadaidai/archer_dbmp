#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from dbmp.models.cmdb_os import CmdbOs
from dbmp.models.dbmp_mysql_instance import DbmpMysqlInstance
from dbmp.models.dbmp_mysql_instance_info import DbmpMysqlInstanceInfo
from common.util.decorator_tool import DecoratorTool
from common.util.ip_tool import IpTool
from common.util.mysql_admin_tool import MysqlAdminTool

import simplejson as json
import traceback
import logging

logger = logging.getLogger('default')

@DecoratorTool.clean_alert_message
def ajax_mysql_is_alived(request):
    """ajax 的方式远程执行mysqladmin ping
       从而获得MySQL是否存活
    """

    is_alived = False
    if request.method == 'POST':
        # 获得传来的MySQL连接参数 和 所在的操作系统ID
        os_id = int(request.POST.get('os_id', '0'))
        mysql_host = request.POST.get('mysql_host', '')
        mysql_port = int(request.POST.get('mysql_port', '0'))
        mysql_user = request.POST.get('mysql_user', '')
        mysql_password = request.POST.get('mysql_password', '')
        mysql_base_dir = request.POST.get('mysql_base_dir', '')

        if(os_id):
            try:
                cmdb_os = CmdbOs.objects.get(os_id = os_id)
            except CmdbOs.DoesNotExist:
                logger.info(traceback.format_exc())

        if (cmdb_os and mysql_host and mysql_port and mysql_user
                    and mysql_password and mysql_base_dir):



            # 获得操作系统
            mysqladmin = '{dir}/bin/mysqladmin'.format(dir = mysql_base_dir)
            # 执行MySQL ping 命令
            is_alived = MysqlAdminTool.mysql_is_alived(mysqladmin = mysqladmin,
                                            mysql_user = mysql_user,
                                            mysql_password = mysql_password,
                                            mysql_host = mysql_host,
                                            mysql_port = mysql_port,
                                            os_ip = IpTool.num2ip(cmdb_os.ip),
                                            os_user = cmdb_os.username,
                                            os_password = cmdb_os.password)

    respons_data = json.dumps(is_alived)
    return HttpResponse(respons_data, content_type='application/json')

def ajax_start_instance(request):
    """执行启动MySQL实例命令"""

    is_ok = False
    if request.method == 'POST':
        ###################################
        # 获取MySQL实例信息并执行启动命令
        ###################################
        try:
            # 获得传入的MySQL实例ID
            mysql_instance_id = int(request.POST.get('mysql_instance_id', '0'))
        except ValueError:
            logger.error(traceback.format_exc())
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        try:
            # 获取MySQL实例
            dbmp_mysql_instance_count = DbmpMysqlInstance.objects.filter(
                        mysql_instance_id = mysql_instance_id).count()
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('查找dbmp_mysql_instance_count失败')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        # 如果没有找到或找到多个MySQL实例返回失败
        if dbmp_mysql_instance_count != 1:
            logger.error('没有找到或找到多个MySQL实例')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        try:
            # 获取MySQL而外信息
            dbmp_mysql_instance_info = DbmpMysqlInstanceInfo.objects.values(
                                        'mysql_instance_info_id',
                                        'start_cmd').get(
                        mysql_instance_id = mysql_instance_id)
            print dbmp_mysql_instance
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('查找MySQL实例Info失败DbmpMysqlInstanceInfo')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        respons_data = json.dumps(is_ok)
        return HttpResponse(respons_data, content_type='application/json')

def ajax_stop_instance(request):
    """停止MySQL实例"""
    pass

def ajax_restart_instance(request):
    """启动MySQL实例"""
    pass

def ajax_mysql_instance_status(request):
    """获取和修改MySQL实例状态"""
    pass
