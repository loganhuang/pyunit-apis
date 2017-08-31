#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import http.cookiejar
import urllib.parse
import json
from logger.Logger import BaseLineLogger
import re

__author__ = ''


# 配置类
class BaseLineHttp:
    # 封装http请求方法，http头设置

    def __init__(self, host, port):
        self.headers = {}  # http 头
        self.host = host
        self.port = port
        self.paras = {}
        self.data ={}
        self.log = BaseLineLogger.get_log()
        # install cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

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

        # substitution reference
        self.sub_ref(params, self.paras)

        if len(params) > 0:
            params = urllib.parse.urlencode(params)  # 将参数转为url编码字符串
            url = 'http://' + self.host + ':' + str(self.port) + url + "?" + params
        else:
            url = 'http://' + self.host + ':' + str(self.port) + url

        self.log.info("get-url=" + url)
        self.log.info("get-headers=%s", *(self.headers,))
        request = urllib.request.Request(url, headers=self.headers)

        try:
            response = urllib.request.urlopen(request)
            response = response.read().decode('utf-8')  ## decode函数对获取的字节数据进行解码
            json_response = json.loads(response)  # 将返回数据转为json格式的数据
            self.log.info("get-response=" + response)
            return json_response
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
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request, data)
            response = response.read().decode('utf-8')
            json_response = json.loads(response)
            self.log.info("post-response=" + response)
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装HTTP xxx请求方法
    # 自由扩展

if __name__ == '__main__':
    querystring = json.dumps({
        "phoneNo": "18701082122",
        "smsCode": "111111",
    })

    headers = {
        'Content-Type': "application/json;charset=UTF-8",
        'OPERATOR_TOKEN': "",
        'Submit_token': ""
    }

    http = BaseLineHttp('apptest.e-zhilu.com', '80')
    http.set_header(headers)
    ret = http.post('/login/login', querystring)
    print(ret)
