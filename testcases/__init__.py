#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def load_tests(loader, standard_tests, pattern):
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern="test*.py")
    standard_tests.addTests(package_tests)
    return standard_tests


if __name__ == '__main__':
    from common.const.const import PATH
    from config.config import BaselineConfig
    from utils.httpmethods import BaseLineHttp
    from utils.xlshandler import BaseLineXls
    import unittest
    from testcases import test_normal

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
            suite.addTest(test_normal.BaseLineNormalCase(api_data=case, http=bl_http))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)