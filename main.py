#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import unittest
from common.const.const import PATH
from utils.HTMLTestReportEN import HTMLTestRunner
from utils.report import BaseLineReport
from utils.sendemail import BaseLineEmail
from common.database.BaseLineTestResult import save_api_test_result
from common.database.BaseLineTestResult import save_monitor_test_result
from config.config import BaselineConfig


def api_test_main():
    # search test cases
    test_dir = PATH.PROJ_PATH + 'testcases/api'
    print(test_dir)
    discover = unittest.TestLoader().discover(test_dir, pattern='test*.py')

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
    # save_api_test_result(data)

    # send email
    if ret.error_count > 0 or ret.failure_count > 0:
        email = BaseLineEmail(report_file)
        email.send_email()
    pass


def web_test_main():
    # search test cases
    test_dir = PATH.PROJ_PATH + 'testcases/web'
    discover = unittest.TestLoader().discover(test_dir, pattern='test*.py')

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

    # send email
    if ret.error_count > 0 or ret.failure_count > 0:
        email = BaseLineEmail(report_file)
        email.send_email()
    pass


def monitor_test_main():
    # search test cases
    test_dir = PATH.PROJ_PATH + 'testcases/monitor'
    print(test_dir)
    discover = unittest.TestLoader().discover(test_dir, pattern='test*.py')

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
    save_monitor_test_result(data)

    # send email
    if ret.error_count > 0 or ret.failure_count > 0:
        email = BaseLineEmail(report_file)
        email.send_email()
    pass


if __name__ == '__main__':
    import sys
    callback = {'api': api_test_main, 'web': web_test_main, 'monitor': monitor_test_main}
    categories = BaselineConfig(PATH.CONFIG_INI_FILE).test_categories

    usage = '''
        Usage:
        python3 %(sript_name)s test_categories
        example:
        python3 %(sript_name)s api
        python3 %(sript_name)s api web monitor
        support test categories:
        %(categories)s
        '''% {'sript_name': sys.argv[0], 'categories': categories}
    if len(sys.argv) < 2:
        print(usage)
        pass

    for i in range(1, len(sys.argv)):
        if sys.argv[i] in categories:
            entry = callback[sys.argv[i]]
            entry()
        else:
            print('wrong parameters')
            print(usage)

    pass


