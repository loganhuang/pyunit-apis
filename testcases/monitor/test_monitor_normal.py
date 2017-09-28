#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import json, datetime
from logger.Logger import BaseLineLogger
from utils.httpmethods import BaseLineHttp
from common.checkpoints.cpnormal import BaseLineCpNormal
from common.caches.cachesnormal import BaseLineCachesNormal
from common.database.BaseLineTestResult import save_monitor_test_result


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
        self.tries = 1
        self.starttime = datetime.datetime.now()
        self.endtime = datetime.datetime.now()
        self.__doc__ = 'api_data'

    def setUp(self):
        if not isinstance(self.api_data, list or tuple):
            raise TypeError

        if not isinstance(self.http, BaseLineHttp):
            raise TypeError

        self.case_id = self.api_data[0]
        self.case_name = self.api_data[1]
        self.starttime = datetime.datetime.now()
        self.log.info('%s[%s]======================TEST START=======================', *(self.case_id, self.case_name))
        pass

    # case_id    desc	  api_path	   methods	type	data	                                      checkpoint	cache  retries  active	others
    # Case_001  login	/login/login	post	form	{"phoneNo":"18701082122", "smsCode":"111111"}	success	              7      TRUE
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

        if self.api_data[8] != "":
            self.tries = int(self.api_data[8])

        retries = 0
        while retries < self.tries:
            retries = retries + 1

            ret = None
            if method == 'post':
                ret = self.http.post(api_path, data)
            elif method == 'get':
                ret = self.http.get(api_path, data)
            else:
                pass

            self.endtime = datetime.datetime.now()
            if ret:
                rtn, rtn_msg = BaseLineCpNormal.check_points(self.check_point, ret, self.case_name, self.case_id)
                if rtn is True:
                    print('after tried %d time, the result is ' + rtn_msg + ', so the test Passed' % retries)

                    # save the test result
                    result = "checked successfully after tried %d times" % retries
                    data = [(0, "case", "montest", self.case_name, self.starttime.timestamp(), self.endtime.timestamp(),
                             1, 1, 0, 0, retries, self.tries, result, "None"), ]
                    save_monitor_test_result(data)

                    if len(self.cache_dict) > 0:
                        BaseLineCachesNormal.check_caches(self.cache_dict, ret, self.http)
                    break

                if retries >= self.tries:

                    # save the test result
                    result = "did not get expected data after tried %d times" % retries
                    data = [(0, "case", "montest", self.case_name, self.starttime.timestamp(), self.endtime.timestamp(),
                             1, 1, 0, 0, retries, self.tries, result, "None"), ]
                    save_monitor_test_result(data)

                    self.assertTrue(rtn, msg=rtn_msg)

            elif retries >= self.tries:
                self.log.info("[%s]: expected response: %s, but no any response after retied %d times",
                              *(self.case_name, self.check_point, self.retries))

                # save the test result
                result = "net error, time out after tried %d times" % retries
                data = [(0, "case", "montest", self.case_name, self.starttime.timestamp(), self.endtime.timestamp(),
                         1, 1, 0, 0, retries, self.tries, result, "None"), ]
                save_monitor_test_result(data)

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
                if case[9]:
                    suite.addTest(BaseLineNormalCase(api_data=case, http=bl_http))

    return suite

if __name__ == '__main__':
    pass

