#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import json
from logger.Logger import BaseLineLogger
from utils.httpmethods import BaseLineHttp
from common.checkpoints.cpnormal import BaseLineCpNormal
from common.caches.cachesnormal import BaseLineCachesNormal


__author__ = ''


# 测试用例(组)类
class BaseLineNormalCase(unittest.TestCase):

    def __init__(self, methodname='test_normal', api_data=None, http=None):
        super(BaseLineNormalCase, self).__init__(methodname)
        self.api_data = api_data
        self.http = http
        self.case_name = ''
        self.case_id = ''
        self.check_point = {}
        self.cache_dict = {}
        self.log = BaseLineLogger.get_log()
        self.__doc__ = 'api_data'

    def setUp(self):
        if not isinstance(self.api_data, list or tuple):
            raise TypeError

        if not isinstance(self.http, BaseLineHttp):
            raise TypeError

        self.case_id = self.api_data[0]
        self.case_name = self.api_data[1]

        self.log.info('%s[%s]======================TEST START=======================', *(self.case_id, self.case_name))
        pass

    # case_id    desc	  api_path	   methods	type	data	                                      checkpoint	cache    active	others
    # Case_001  login	/login/login	post	form	{"phoneNo":"18701082122", "smsCode":"111111"}	success	              TRUE
    def test_normal(self):
        print('case_id:%-14s' % self.case_id)
        print("case_desc:%-30s" % self.case_name)

        api_path = self.api_data[2]
        method = self.api_data[3]
        # data_type = self.api_data[4]
        data = self.api_data[5]
        self.check_point = json.loads(self.api_data[6])
        if self.api_data[7] != "":
            self.cache_dict = json.loads(self.api_data[7])

        ret = None
        if method == 'post':
            ret = self.http.post(api_path, data)
        elif method == 'get':
            ret = self.http.get(api_path, data)
        else:
            pass

        if ret:
            rtn, rtn_msg = BaseLineCpNormal.check_points(self.check_point, ret, self.case_name, self.case_id)
            self.assertTrue(rtn, msg=rtn_msg)
            print('because ' + rtn_msg + ', so the test Passed')
            if len(self.cache_dict) > 0:
                BaseLineCachesNormal.check_caches(self.cache_dict, ret, self.http)
        else:
            self.log.info("[%s]: expected response: %s, but no any response", *(self.case_name, self.check_point))
            self.assertIsNone(self.check_point, msg=None)

    def tearDown(self):
        self.log.info('%s[%s]======================TEST END======================\n\n', *(self.case_id, self.case_name))


def load_tests(loader, tests, pattern):
    from utils.xlshandler import BaseLineXls
    from config.config import BaselineConfig
    from common.const.const import PATH

    # 构造测试集
    suite = unittest.TestSuite()
    config = BaselineConfig(PATH.CONFIG_INI_FILE)
    server = config.get_server_by_key('monitor')
    bl_http = BaseLineHttp(server[0], server[1])
    headers = {
        'Content-Type': "application/json;charset=UTF-8",
        'OPERATOR_TOKEN': "",
        'Submit_token': ""
    }

    bl_http.set_header(headers)

    caseXls = BaseLineXls(PATH.CASES_XLS_PATH + 'cases.xls')
    for sheet in caseXls.get_sheets_name():
        if sheet.find('monitor') >= 0:
            cases = caseXls.get_xls(sheet)
            for case in cases:
                if not isinstance(case, list or tuple):
                    raise TypeError
                if case[8]:
                    suite.addTest(BaseLineNormalCase(api_data=case, http=bl_http))

    return suite

if __name__ == '__main__':
    pass

