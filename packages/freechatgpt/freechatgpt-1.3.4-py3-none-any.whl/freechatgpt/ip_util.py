# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 12:52
# @Author  : abo123456789
# @Desc    : ip_util.py
import requests


class IpTool(object):
    @staticmethod
    def get_host_ip()->[str,None]:

        """
        查询本机ip地址
        :return: ip
        """
        try:
            res = requests.get('http://httpbin.org/ip').json()
            return res.get('origin')
        except(Exception,):
            return None
