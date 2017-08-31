#!/usr/bin/env python
# -*- coding:utf-8 -*-

from xlrd import open_workbook

__author__ = ''


class BaseLineXls:
    def __init__(self, xls_name):
        self.xls = xls_name

    # 从excel文件中读取测试用例
    def get_xls(self, sheet_name):
        cls = []
        # get xls file's path
        # xlsPath = os.path.join(proDir, "testFile", xls_name)
        # open xls file
        file = open_workbook(self.xls)
        # get sheet by name
        sheet = file.sheet_by_name(sheet_name)
        # get one sheet's rows
        nrows = sheet.nrows
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'cases':
                cls.append(sheet.row_values(i))
        return cls

if __name__ == '__main__':
    from common.const import const
    from logger import Logger

    log = Logger.BaseLineLog.get_log()
    caseXls = BaseLineXls(const.PATH.CASES_XLS_PATH + 'cases.xls')
    log.info(caseXls.get_xls('api_cases'))
