#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import http.cookiejar
import urllib.parse
import json
from logger.Logger import BaseLineLogger
import re
import requests

__author__ = ''


# 配置类
class BaseLineHttp:

    def __init__(self, host, port):
        self.headers = {}
        self.host = host
        self.port = port
        self.paras = {}
        self.data ={}
        self.log = BaseLineLogger.get_log()

    # setting op & port
    def set_ip_port(self, host, port):
        self.host = host
        self.port = port

    # 设置http头
    def set_header(self, headers):
        if not isinstance(headers, dict):
            raise TypeError

        for key in headers:
            self.headers[key] = headers[key]

        self.log.info("set_header: %s", *(headers, ))

    def set_paras(self, paras):
        for key in paras:
            self.paras[key] = paras[key]

        self.log.info("set_paras: %s", *(paras,))

    def set_data(self, data):
        for key in data:
            self.data[key] = data[key]

        self.log.info("set_datas: %s", *(data,))

    # substitution reference
    def sub_ref(self, src, dest):
        if not isinstance(src, dict) or not isinstance(dest, dict):
            raise TypeError

        def get_value(matched):
            m_key = matched.group('value')
            m_key = m_key[2:-1]
            if m_key in dest.keys():
                return dest[m_key]
            return ""

        for key in src:
            src[key] = re.sub('(?P<value>\${.*?})', get_value, src[key])

    # 封装HTTP GET请求方法
    def get(self, url, params):
        # print(type(params))
        if not isinstance(params, str or dict or None):
            raise TypeError

        if len(params) > 0:
            params = eval(params)
        if not isinstance(params, dict):
            params = {}

        # substitution referenceparas
        self.sub_ref(params, self.data)

        if len(params) > 0:
            params = urllib.parse.urlencode(params)  # 将参数转为url编码字符串
            url = 'http://' + self.host + ':' + str(self.port) + url + "?" + params
        else:
            url = 'http://' + self.host + ':' + str(self.port) + url

        self.log.info("get-url=" + url)
        self.log.info("get-headers=%s", *(self.headers,))

        try:
            rtn = requests.get(url, headers=self.headers)
            self.log.info("get-response=" + rtn.text)
            return rtn.json()
        except Exception as e:
            print('%s' % e)
            return {}



    # 封装HTTP POST请求方法
    def post(self, url, data):
        # print(type(data))
        if not isinstance(data, str or dict or None):
            raise TypeError

        if len(data) > 0:
            data = eval(data)
        if not isinstance(data, dict):
            data = {}

        # substitution reference
        self.sub_ref(data, self.data)

        data = json.dumps(data)
        data = data.encode('utf-8')
        url = 'http://' + self.host + ':' + str(self.port) + url
        self.log.info("post-url=" + url)
        self.log.info("post-headers=%s", *(self.headers,))
        self.log.info("post-datas=%s", *(data,))

        try:
            rtn = requests.post(url, data=data, headers=self.headers)
            self.log.info("post-response=" + rtn.text)
            return rtn.json()
        except Exception as e:
            print('%s' % e)
            return{}

    # 封装HTTP xxx请求方法
    # 自由扩展

if __name__ == '__main__':
    querystring = json.dumps({
        "mobile": "18701082122",
        "seccode": "111111",
    })

    headers = {
        'Content-Type': "application/json;charset=UTF-8",
        'token': ""
    }

    http = BaseLineHttp('kouzi.beta2.pluosi.com', '80')
    http.set_header(headers)
    ret = http.post('/api/v1/users/login', querystring)
    # print(ret)
