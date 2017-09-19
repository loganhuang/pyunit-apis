#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import unittest
from common.const.const import PATH
from utils.HTMLTestReportEN import HTMLTestRunner
from utils.report import BaseLineReport
from utils.sendemail import BaseLineEmail
from common.database.BaseLineTestResult import save_test_result


if __name__ == '__main__':
    # search test cases
    test_dir = PATH.PROJ_PATH + 'testcases'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')

    # about report
    test_report_dir = PATH.REPORT_PATH
    now = time.strftime('%Y-%m-%d_%H_%M_%S_')
    filename = test_report_dir + '/' + now + 'result.html'
    fp = open(filename, 'wb')

    # test runner
    runner = HTMLTestRunner(stream=fp, verbosity=2, title=u'测试报告', description=u'用例执行情况：')
    ret = runner.run(discover)
    fp.close()

    # get report
    report_file = BaseLineReport.get_new_report()

    # save result
    total = ret.failure_count + ret.success_count + ret.error_count
    data = [('ppdapis', ret.starttime, ret.endtime, total, ret.success_count, ret.failure_count, ret.error_count, report_file),]
    save_test_result(data)

    # send email
    if ret.error_count > 0 or ret.failure_count > 0:
        email = BaseLineEmail(report_file)
        email.send_email()
