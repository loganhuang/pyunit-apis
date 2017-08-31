#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import json
from logger.Logger import BaseLineLogger
from utils.httpmethods import BaseLineHttp


__author__ = ''


# 测试用例(组)类
class BaseLineNormalCase(unittest.TestCase):

    def __init__(self, methodname='test_normal', api_data=None, http=None):
        super(BaseLineNormalCase, self).__init__(methodname)
        self.api_data = api_data
        self.http = http
        self.log = BaseLineLogger.get_log()
        self.__doc__ = 'api_data'

    def setUp(self):
        pass

    # {"header":{"result":{"submitToken":"Submit_token", "userToken":"OPERATOR_TOKEN"}}}
    def get_key_val(self, ret_dict, cache_dict, out_dict):
        for key in cache_dict:
            if isinstance(cache_dict[key], dict) and isinstance(ret_dict[key], dict):
                self.get_key_val(ret_dict[key], cache_dict[key], out_dict)
            else:
                out_dict[cache_dict[key]] = ret_dict[key]

    def check_cache(self, http, ret_dict, cache_dict):
        if not isinstance(self.http, BaseLineHttp):
            raise TypeError

        for key in cache_dict:
            out_dict = {}
            self.get_key_val(ret_dict, cache_dict[key], out_dict)
            if key == 'header':
                self.http.set_header(out_dict)

            elif key == 'paras':
                self.http.set_paras(out_dict)
            elif key == 'data':
                self.http.set_data(out_dict)
            else:
                pass

        pass

    # case_id    desc	  api_path	   methods	type	data	                                      checkpoint	cache    active	others
    # Case_001  login	/login/login	post	form	{"phoneNo":"18701082122", "smsCode":"111111"}	success	              TRUE
    def test_normal(self):
        if not isinstance(self.api_data, list or tuple):
            raise TypeError

        bl_http = None
        if isinstance(self.http, BaseLineHttp):
            bl_http = self.http
        else:
            raise TypeError
        case_id = self.api_data[0]
        case_name = self.api_data[1]
        print("case_id:" + case_id)
        print("case_desc:" + case_name)

        api_path = self.api_data[2]
        method = self.api_data[3]
        # data_type = self.api_data[4]
        data = self.api_data[5]
        check_point = json.loads(self.api_data[6])
        cache_dict = {}
        if self.api_data[7] != "":
            cache_dict = json.loads(self.api_data[7])

        ret = None
        if method == 'post':
            ret = bl_http.post(api_path, data)
        elif method == 'get':
            ret = bl_http.get(api_path, data)
        else:
            pass

        if ret:
            for key in check_point:
                self.log.info("[%s]: check_point: %s=%s, response: %s=%s",
                              *(case_name, key, check_point[key], key, ret[key]))
                self.assertEqual(ret[key], check_point[key], ret[key])
            if len(cache_dict) > 0:
                self.check_cache(bl_http, ret, cache_dict)
        else:
            self.log.info("[%s]: expected response: %s, but no any response", *(case_name, check_point))
            self.assertIsNone(check_point, msg=None)


def load_tests(loader, tests, pattern):
    from utils.xlshandler import BaseLineXls
    from config.config import BaselineConfig
    from common.const.const import PATH

    # 构造测试集
    suite = unittest.TestSuite()
    config = BaselineConfig(PATH.CONFIG_INI_FILE)
    bl_http = BaseLineHttp(config.get_host(), config.get_port())
    headers = {
        'Content-Type': "application/json;charset=UTF-8",
        'OPERATOR_TOKEN': "",
        'Submit_token': ""
    }

    bl_http.set_header(headers)

    caseXls = BaseLineXls(PATH.CASES_XLS_PATH + 'cases.xls')
    cases = caseXls.get_xls('api_cases')
    for case in cases:
        if not isinstance(case, list or tuple):
            raise TypeError
        if case[8]:
            suite.addTest(BaseLineNormalCase(api_data=case, http=bl_http))

    return suite

if __name__ == '__main__':
    pass

