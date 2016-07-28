# -*- coding: utf-8 -*-

import os
import sys
import socket
import struct

class IpTool(object):
    """这是一个IP转化工具类
    """
    def __init__(self):
       pass

    @classmethod
    def num2ip(self, num):
        """将一个10位数转化成一个IP
        Args:
            num: 一个整数
        Return:
            返回一个 字符串 IP
            如: 10.10.10.11
        Raise: None
        """
        if isinstance(num, int) or isinstance(num, long):
            return socket.inet_ntoa(struct.pack('I', socket.htonl(num)))
        else:
            return ''

    @classmethod
    def ip2num(self, ip):
        """将一个IP转化为整数
        Args:
            ip: 一个ip: 10.10.10.11
        Return: 
            返回一个 Long 类型的数字
            如: 123456789
        Raise: None
        """

        return socket.ntohl(struct.unpack('I', socket.inet_aton(str(ip)))[0])


def main():
    print Toolkit.ip2num('127.0.0.1')


if __name__ == '__main__':
    main()
