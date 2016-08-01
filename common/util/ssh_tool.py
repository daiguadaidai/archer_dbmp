# -*- coding: utf-8 -*-

import os
import sys
import paramiko
import traceback
import datetime
import logging

logger = logging.getLogger('default')

class SSHTool(object):
    """这是一个可以通过ssh远程执行一些东西的类
    """

    def __init__(self):
       pass

    @classmethod
    def ssh_exec_cmd(self, cmd,
                           host='127.0.0.1',
                           username=None,
                           password=None,
                           port=22):
        """将命令在远程执行
        Args:
            cmd: 需要远程执行的命令
            host: 远程的ip
            username: 用户名
            password: 密码
        Return:
            stdout, stderr, True/False 返回执行命令后的相关输出
        Raise: None
        """
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # 创建 SSH 链接
            ssh.connect(host, port, username, password, key_filename=None, timeout=2)
            logger.info('connect host: {host}'.format(host=host))
            logger.info('connect username: {u}'.format(u=username))
            logger.info('connect password: {p}'.format(p=password))
            logger.info('want exec cmd: {cmd}'.format(cmd=cmd))
        except Exception, e:
            logger.error('connect host: {host}'.format(host=host))
            logger.error('connect username: {u}'.format(u=username))
            logger.error('connect password: {p}'.format(p=password))
            logger.error('want exec cmd: {cmd}'.format(cmd=cmd))
            logger.error(e)

        # 执行命令并输出
        stdin, stdout, stderr = ssh.exec_command(cmd)
        err_code = stdout.channel.recv_exit_status()
        out_msg = stdout.readlines()
        err_msg = stderr.readlines()
        ssh.close()
     
        # 返回 True/False
        is_ok = False
        if err_code != 0:
            logger.error(out_msg)
            logger.error(err_msg)
            logger.error('error code: {code}'.format(code=err_code))
        else:
            is_ok = True
            logger.info(out_msg)
            logger.info(err_msg)
            logger.info('error code: {code}'.format(code=err_code))
            
        return is_ok, out_msg, err_msg

    @classmethod
    def ssh_trans(self, host='127.0.0.1',
                        username=None,
                        password=None,
                        local_file=None,
                        remote_file=None,
                        port=22):
        """将文件传输到远程 或目录
        将输入的一个文件从本地传输到远程, 这个文件必须是全路径的

        Args:
            host: IP
            username: 远程OS用户名
            password: 指定username密码
            local_file: 本地的文件路径和文件名
            remote_file: 传输到远程的文件(在远程的路径和文件名)
            port: ssh传输的端口
        Return:
            True/False 是否传输成功
        Raise: None
        """
        is_ok = False
        # 如果是文件则就只需要传输一个文件
        if os.path.isfile(local_file):
            logger.info('is file')
            is_ok = self.ssh_trans_file(host,
                                        username,
                                        password,
                                        local_file,
                                        remote_file)
        # 如果是目录则就需要传输这个目录下的所有文件
        elif os.path.isdir(local_file):
            logger.info('is dir')
            is_ok = self.ssh_trans_dir(host,
                                       username,
                                       password,
                                       local_file,
                                       remote_file)
        return is_ok

    @classmethod
    def ssh_trans_file(self, host='127.0.0.1',
                        username=None,
                        password=None,
                        local_file=None,
                        remote_file=None,
                        port=22):
        """将文件传输到远程
        将输入的一个文件从本地传输到远程, 这个文件必须是全路径的

        Args:
            host: IP
            username: 远程OS用户名
            password: 指定username密码
            local_file: 本地的文件路径和文件名
            remote_file: 传输到远程的文件(在远程的路径和文件名)
            port: ssh传输的端口
        Return:
            True/False 是否传输成功
        Raise: None
        """
        is_ok = False
        try:
            # 创建sftp实例用于远程传输
            t = paramiko.Transport((host, port))
            t.connect(username=username, password=password)
            logger.info('connected {host} successful'.format(host=host))
            sftp = paramiko.SFTPClient.from_transport(t)
            # 获得远程文件路径
            parent_path, file_name = self.get_file_path_and_name(remote_file)
            # 执行远程命令创建相关目录
            mkdir_is_ok = self.ssh_mkdir(parent_path,
                                       host,
                                       username,
                                       password)
            # 传输文件
            sftp.put(local_file, remote_file)
            logger.info('Upload file successful')
            is_ok = True
        except Exception, e:
            logger.error('Upload file failure!!!')
            s = traceback.format_exc()
            logger.error(s)
        finally:
            t.close()
            logger.info('sftp closed!')
            return is_ok

    @classmethod
    def ssh_trans_dir(self, host='127.0.0.1',
                        username=None,
                        password=None,
                        local_dir=None,
                        remote_dir=None,
                        port=22):
        """将目录传输到远程
        将输入的一个目录从本地传输到远程, 这个目录必须是全路径的

        Args:
            host: IP
            username: 远程OS用户名
            password: 指定username密码
            local_file: 本地的文件路径
            remote_file: 传输到远程的路径(在远程的路径)
            port: ssh传输的端口
        Return:
            True/False 是否传输成功
        Raise: None
        """
        is_ok = False
        # 构造一个同一个的目录结构: /aaa/bbb/ccc/
        local_dir = local_dir.rstrip('/')
        local_dir = '{local_dir}/'.format(local_dir=local_dir)
        remote_dir = remote_dir.rstrip('/')
        remote_dir = '{remote_dir}/'.format(remote_dir=remote_dir)

        # 执行远程命令创建相关目录
        mkdir_is_ok = self.ssh_mkdir(remote_dir,
                                     host,
                                     username,
                                     password)
        try:
            # 创建sftp实例用于远程传输
            t = paramiko.Transport((host, port))
            t.connect(username=username, password=password)
            logger.info('connected {host} successful'.format(host=host))
            sftp = paramiko.SFTPClient.from_transport(t)

            logger.info(
                'upload file start {time} '.format(
                                            time=datetime.datetime.now())
            )
            # 获得本地文件的路径已经文件
            for root, dirs, files in os.walk(local_dir):
                is_ok = False
                for filespath in files:
                    local_file = os.path.join(root, filespath)
                    # 构造临时的文件 如: /tmp/bb/a.txt -> bb/a.txt
                    a = local_file.replace(local_dir, '', 1)
                    remote_file = os.path.join(remote_dir, a)
                    try:
                        sftp.put(local_file, remote_file)
                    except Exception, e:
                        tmp_dir, tmp_file = self.get_file_path_and_name(remote_file)
                        sftp.mkdir(tmp_dir)
                        sftp.put(local_file, remote_file)
                            

                    logger.info(
                        'upload {local_file} to remote {remote_file}'.format(
                            local_file = local_file,
                            remote_file = remote_file
                        )
                    )
                for name in dirs:
                    local_path = os.path.join(root, name)
                    a = local_path.replace(local_dir, '', 1)
                    remote_path = os.path.join(remote_dir, a)
                    try:
                        sftp.mkdir(remote_path)
                        logger.info(
                            'mkdir path {remote_path}'.format(
                                remote_path = remote_path
                            )
                        )
                    except Exception, e:
                        logger.error(
                            'mkdir {remote_path}'.format(
                                remote_path = remote_path
                            )
                        )
                        logger.error(e)
                        logger.error(traceback.format_stack())

            logger.info(
                'upload file success %s {time}'.format(
                    time = datetime.datetime.now()
                )
            )
            
            # 传输文件
            is_ok = True
        except Exception, e:
            logger.error('Upload file failure!!!')
            s = traceback.format_exc()
            logger.error(s)
        finally:
            t.close()
            logger.info('sftp closed!')
            return is_ok

    
    @classmethod
    def ssh_mkdir(self, path, host='127.0.0.1', username=None, 
                        password=None, port=22):
        """远程创建目录
        通过传入的 path 和远程OS用户信息在远程创建一个目录
        
        Args: 
            path: 目录路径
            host: OS IP
            username: 用户名
            password: 密码
            port: 端口
        """
        # 执行远程命令创建相关目录
        cmd = ('source ~/.bash_profile && '
               'mkdir -p {path}'.format(path=path))
        is_ok, stdout, stderr = self.ssh_exec_cmd(
                                cmd,
                                host,
                                username,
                                password)
        if is_ok:
            logger.info('mkdir: {path} successful!'.format(path=path))
        else:
            logger.error('mkdir: {path} failure!!!'.format(path=path))
        return is_ok


    @classmethod
    def get_file_path_and_name(self, path):
        """获得文件所在目录和文件名称名称
        Args:
            path: 文件的完整路径
        Return:
            (parent_path, file_name) 文件或目录的父路径 和 文件名称
        Raise: None
        """
        file_name = os.path.basename(path)
        parent_path = os.path.dirname(path)
      
        return parent_path, file_name



def main():
    # ToolSSH.ssh_exec_cmd(cmd = 'source ~/.bash_profile && md5sum /tmp/mysqldump_1.sql',
    #                      username = 'root',
    #                      password = 'oracle')

    print SSHTool.ssh_trans(host = '127.0.0.1',
                      username = 'root',
                      password = 'oracle',
                      local_file = '/tmp',
                      remote_file = '/u02/backup_test')


if __name__ == '__main__':
    main()
