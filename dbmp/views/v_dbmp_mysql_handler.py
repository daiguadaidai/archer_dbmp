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
        # 记录日志
        info_msg = 'host: {host}, port: {port}'.format(
                                            host = mysql_host,
                                            port = mysql_port)
        logger.info(info_msg)

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
        try:
            # 获得传入的MySQL实例ID
            mysql_instance_id = int(request.POST.get('mysql_instance_id', '0'))
        except ValueError:
            logger.error(traceback.format_exc())
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取MySQL实例
        #################################################################
        try:
            dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                'mysql_instance_id',
                                                'os_id',
                                                'username',
                                                'password',
                                                'port',
                                                'host',).get(
                               mysql_instance_id = mysql_instance_id)
            info_msg = 'host: {host}, port: {port}'.format(
                              host = dbmp_mysql_instance.get('host', ''),
                              port = dbmp_mysql_instance.get('port', 0))
            logger.info(info_msg)
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('查找dbmp_mysql_instance失败')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取MySQL而外信息
        #################################################################
        try:
            dbmp_mysql_instance_info = DbmpMysqlInstanceInfo.objects.values(
                                        'mysql_instance_info_id',
                                        'start_cmd').get(
                        mysql_instance_id = mysql_instance_id)
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('查找MySQL实例Info失败DbmpMysqlInstanceInfo')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取 OS 信息
        #################################################################
        try:
            cmdb_os = CmdbOs.objects.values('os_id',
                                            'ip',
                                            'username',
                                            'password').get(
                        os_id = dbmp_mysql_instance.get('os_id', 0))
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('未找到相关的操作系统(OS)信息')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取 当前操作系统存在的 mysqld pid, 通过ps -ef 获得
        #################################################################
        is_ok, exist_pids, errs = MysqlAdminTool.mysqld_pids(
                                   os_ip = IpTool.num2ip(cmdb_os.get('ip', '')),
                                   os_user = cmdb_os.get('username', ''),
                                   os_password = cmdb_os.get('password', ''))
        if not is_ok:
            logger.error('获取 当前操作系统存在的 mysqld pid命令错误')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 执行启动MySQL并获得返回的pid并且将这些pid保存到DbmpMysqlInstance中
        #################################################################
        is_ok, start_pids, errs = MysqlAdminTool.start_mysql_and_pids(
                                   cmd = dbmp_mysql_instance_info.get('start_cmd', ''),
                                   os_ip = IpTool.num2ip(cmdb_os.get('ip', '')),
                                   os_user = cmdb_os.get('username', ''),
                                   os_password = cmdb_os.get('password', ''))
        if not is_ok:
            logger.error('执行启动MySQL命令失败')
            respons_data = json.dumps(is_ok)
            return HttpResponse(respons_data, content_type='application/json')

        # 获得MySQL可能的pid
        possible_pid = '|'.join(list(set(start_pids) - set(exist_pids)))

        # 改变MySQL状态为正在启动(4) 并且 保存 可能的pid
        try:
            DbmpMysqlInstance.objects.filter(
                          mysql_instance_id = mysql_instance_id).update(
                                             run_status = 4,
                                             possible_pid = possible_pid)
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('更新MySQL状态为 正在启动 和 添加 可能的MySQL pid 失败')
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
    """获取和修改MySQL实例状态
    对MySQL状态进行测试
    Args: None
    return: run_status
        1. 数据库停止, 启动失败
        2. 数据库正常运行, 启动成功
        3. 数据库停止, 继续检测
        4. 内部错误, 检测失败
    Raise: None
    """
    
    run_status = 1
    if request.method == 'POST':
        try:
            # 获得传入的MySQL实例ID
            mysql_instance_id = int(request.POST.get('mysql_instance_id', '0'))
        except ValueError:
            logger.error(traceback.format_exc())
            respons_data = json.dumps(run_status)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取MySQL实例
        #################################################################
        try:
            dbmp_mysql_instance = DbmpMysqlInstance.objects.values(
                                                'mysql_instance_id',
                                                'os_id',
                                                'username',
                                                'password',
                                                'run_status',
                                                'possible_pid',
                                                'port',
                                                'host',).get(
                               mysql_instance_id = mysql_instance_id)
            info_msg = 'host: {host}, port: {port}'.format(
                              host = dbmp_mysql_instance.get('host', ''),
                              port = dbmp_mysql_instance.get('port', 0))
            logger.info(info_msg)
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('查找dbmp_mysql_instance失败')
            run_status = 4
            respons_data = json.dumps(run_status)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取MySQL而外信息
        #################################################################
        try:
            dbmp_mysql_instance_info = DbmpMysqlInstanceInfo.objects.values(
                                        'mysql_instance_info_id',
                                        'base_dir').get(
                        mysql_instance_id = mysql_instance_id)
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('查找MySQL实例Info失败DbmpMysqlInstanceInfo')
            run_status = 4
            respons_data = json.dumps(run_status)
            return HttpResponse(respons_data, content_type='application/json')

        #################################################################
        # 获取 OS 信息
        #################################################################
        try:
            cmdb_os = CmdbOs.objects.values('os_id',
                                            'ip',
                                            'username',
                                            'password').get(
                        os_id = dbmp_mysql_instance.get('os_id', 0))
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('未找到相关的操作系统(OS)信息')
            run_status = 4
            respons_data = json.dumps(run_status)
            return HttpResponse(respons_data, content_type='application/json')

        mysqladmin = '{dir}/bin/mysqladmin'.format(
                    dir = dbmp_mysql_instance_info.get('base_dir', ''))
        logger.info(mysqladmin)
        # 执行MySQL ping 命令
        is_ok = MysqlAdminTool.mysql_is_alived(mysqladmin = mysqladmin,
                mysql_user = dbmp_mysql_instance.get('username', ''),
                mysql_password = dbmp_mysql_instance.get('password', ''),
                mysql_host = IpTool.num2ip(dbmp_mysql_instance.get('host', '')),
                mysql_port = dbmp_mysql_instance.get('port', ''),
                os_ip = IpTool.num2ip(cmdb_os.get('ip', '')),
                os_user = cmdb_os.get('username', ''),
                os_password = cmdb_os.get('password', ''))

        # 如果 检测 MySQL还未启动则 查看相关进程是否存在
        if not is_ok:
            logger.warning('mysqladmin ping 失败')

            # 判断相关进程是否存在(通过ps命来查看)
            cmd = ("ps -ef | egrep '{possible_pid}' | grep -v grep "
                   "| awk '{col}'".format(
                     possible_pid = dbmp_mysql_instance.get('possible_pid', ''),
                     col = '{print $2}'))
            is_ok, pids, errs = MysqlAdminTool.get_mysql_start_possible_pids(
                               cmd = cmd,
                               os_ip = IpTool.num2ip(cmdb_os.get('ip', '')),
                               os_user = cmdb_os.get('username', ''),
                               os_password = cmdb_os.get('password', ''))

            # 如果返回的pids个数大于15则判断失败
            if is_ok and len(pids) > 15:
                run_status = 1
                logger.warning('检测返回MySQL pids 大于 15, 判断为启动失败')
                logger.error('!!! 启动失败 !!!')
                # 改变MySQL状态为停止(1)
                try:
                    DbmpMysqlInstance.objects.filter(
                              mysql_instance_id = mysql_instance_id).update(
                                                 run_status = run_status)
                except Exception, e:
                    logger.error(traceback.format_exc())
                    logger.error('更新MySQL状态为 停止(1) 失败')

                respons_data = json.dumps(run_status)
                return HttpResponse(respons_data, content_type='application/json')
            # 如果返回的pids个数 <= 0 则判断失败
            elif is_ok and len(pids) <= 0:
                run_status = 1
                logger.warning('检测返回MySQL pids <= 0, 判断为启动失败')
                logger.error('!!! 启动失败 !!!')
                # 改变MySQL状态为停止(1)
                try:
                    DbmpMysqlInstance.objects.filter(
                              mysql_instance_id = mysql_instance_id).update(
                                                 run_status = run_status)
                except Exception, e:
                    logger.error(traceback.format_exc())
                    logger.error('更新MySQL状态为 停止(1) 失败')

                respons_data = json.dumps(run_status)
                return HttpResponse(respons_data, content_type='application/json')
            elif is_ok:
                run_status = 3
                logger.warning('检测返回MySQL 0 <= pids < 15, 判断为正在启动, 将返回继续检测(3)')
                respons_data = json.dumps(run_status)
                return HttpResponse(respons_data, content_type='application/json')
            else:
                run_status = 4
                logger.error('检测MySQL pids 出错(4)')
                respons_data = json.dumps(run_status)
                return HttpResponse(respons_data, content_type='application/json')
             

        # 记录启动成功, 并改变成功状态(2)
        run_status = 2
        success_info = '启动成功 {host}, {port}'.format(
                          host = IpTool.num2ip(dbmp_mysql_instance.get('host', '')),
                          port = dbmp_mysql_instance.get('port', ''))
        logger.info(success_info)

        try:
            DbmpMysqlInstance.objects.filter(
                      mysql_instance_id = mysql_instance_id).update(
                                         run_status = run_status)
        except Exception, e:
            logger.error(traceback.format_exc())
            logger.error('MySQL启动成功. 但是, 更新MySQL状态为 启动(2) 失败')

        # 最终返回启动成功
        respons_data = json.dumps(run_status)
        return HttpResponse(respons_data, content_type='application/json')

