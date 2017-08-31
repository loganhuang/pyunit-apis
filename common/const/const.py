#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

curPath = os.path.split(os.path.realpath(__file__))[0]


class LOGGER:
    pass


class PATH:
    PROJ_PATH= curPath + '/../../'
    CASES_XLS_PATH = curPath + '/../../testcases/'
    CONFIG_INI_FILE = curPath + '/../../config/config.ini'
    REPORT_PATH = curPath + '/../../report'
    pass

