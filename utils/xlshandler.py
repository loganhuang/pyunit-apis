#!/usr/bin/env python
# -*- coding:utf-8 -*-

from xlrd import open_workbook
import os

__author__ = ''


class BaseLineXls:
    def __init__(self, xls_name):
        self.xls = xls_name
        if os.path.exists(xls_name):
            self.fd = open_workbook(xls_name)
        else:
            self.fd = None

    # 从excel文件中读取测试用例
    def get_xls(self, sheet_name):
        if self.fd is None:
            return []

        cls = []
        # get sheet by name
        sheet = self.fd.sheet_by_name(sheet_name)
        # get one sheet's rows
        nrows = sheet.nrows
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'cases':
                cls.append(sheet.row_values(i))
        return cls

    def get_sheets_name(self):
        if self.fd is None:
            return []
        return self.fd.sheet_names()

if __name__ == '__main__':
    from common.const import const
    from logger import Logger

    log = Logger.BaseLineLog.get_log()
    caseXls = BaseLineXls(const.PATH.CASES_XLS_PATH + 'cases.xls')
    log.info(caseXls.get_xls('api_cases'))
