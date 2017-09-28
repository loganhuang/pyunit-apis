#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import json, time
from logger.Logger import BaseLineLogger
from common.selenium.base import BaseLineWebDriver
from config.config import BaselineConfig
from common.const.const import PATH

__author__ = ''


# 测试用例(组)类
class BaseLineNormalCase(unittest.TestCase):
    def __init__(self, methodname='test_normal', api_data=None, web_driver=None):
        super(BaseLineNormalCase, self).__init__(methodname)
        self.api_data = api_data
        self.web_driver = web_driver
        self.case_name = ''
        self.case_id = ''
        self.log = BaseLineLogger.get_log()

    # cases	     description        page_url	    actions	                        checkpoint	                               active	others
    # case_001	    home_page    /market/index.html		     {"xpath":{"html/body/div[1]/div[2]/div[1]/span", "为您推荐贷款产品"}}	TRUE
    def setUp(self):
        if not isinstance(self.api_data, list or tuple):
            raise TypeError

        if not isinstance(self.api_data[2], str):
            raise TypeError

        self.case_id = self.api_data[0]
        self.case_name = self.api_data[1]
        self.web_driver = BaseLineWebDriver(BaselineConfig(PATH.CONFIG_INI_FILE).get_server_by_key('web')[0])
        self.web_driver.open_page(self.api_data[2])

        self.log.info('%s[%s]======================TEST START=======================', *(self.case_id, self.case_name))
        pass

    def test_normal(self):
        actions = self.api_data[3]
        if not isinstance(actions, dict):
            actions = None
        print('case_id:%-14s' % self.case_id)
        print("case_desc:%-30s" % self.case_name)
        # actions: fill txtBox, click button etc.
        # {"txt":{"xpath":{"123456":"admin"}, "id":{"01234":"password"}}, "btn":{"id":"12345678"}}
        if actions and len(actions) > 0:
            for key in actions:
                elems = actions[key]
                if not isinstance(elems, dict):
                    raise TypeError

                if key == "txt":
                    for ele_key in elems:
                        ele = elems[ele_key]
                        if not isinstance(ele, dict):
                            raise TypeError
                        if ele_key == "xpath":
                            self.web_driver.fill_box_by_xpath(ele.keys()[0], ele[ele.keys()[0]])
                            pass
                        elif ele_key == "id":
                            self.web_driver.fill_box_by_id(ele.keys()[0], ele[ele.keys()[0]])
                            pass
                    pass
                elif key == "btn":
                    for ele_key in elems:
                        if ele_key == "xpath":
                            self.web_driver.click_by_xpath(elems[ele_key])
                            pass
                        elif ele_key == "id":
                            self.web_driver.click_by_id(elems[ele_key])
                            pass
                    pass
            pass

        # check points, check if the text is what we expected
        check_points = json.loads(self.api_data[4])
        if not isinstance(check_points, dict):
            check_points = None
        if check_points and len(check_points) > 0:
            for key in check_points:
                ele = check_points[key]
                if not isinstance(ele, dict):
                    raise TypeError
                if key == "xpath":
                    for path in ele:
                        break
                    ret = self.web_driver.get_text_by_xpath(path)
                    self.log.info("content of xpath[%s]: %s, expected content: %s",
                                  *(path, ret, ele[path]))
                    self.assertEqual(ret, ele[path], msg=ret)
                elif key == "id":
                    for path in ele:
                        break
                    ret = self.web_driver.get_text_by_id(path)
                    self.log.info("content of id[%s]: %s, expected content: %s",
                                  *(path, ret, ele[path]))
                    self.assertEqual(ret, ele[path], msg=ret)
                pass
            pass

    def tearDown(self):
        # time.sleep(2)
        self.web_driver.close_all_page()
        self.log.info('%s[%s]======================TEST END======================\n\n', *(self.case_id, self.case_name))
        pass


def load_tests(loader, tests, pattern):
    from utils.xlshandler import BaseLineXls

    # 构造测试集
    suite = unittest.TestSuite()

    case_xls = BaseLineXls(PATH.CASES_XLS_PATH + 'cases.xls')
    cases = case_xls.get_xls('web_kouzi')
    for case in cases:
        if not isinstance(case, list or tuple):
            raise TypeError
        if case[5]:
            suite.addTest(BaseLineNormalCase(api_data=case, web_driver=None))

    # driver.close_all_page()
    return suite


if __name__ == '__main__':
    pass