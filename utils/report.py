#!/usr/bin/env python
# -*- coding:utf-8 -*-


from common.const.const import PATH
import os


class BaseLineReport:
    def __init__(self):
        pass

    @staticmethod
    def get_new_report():
        # 列举test_dir目录下的所有文件，结果以列表形式返回。
        test_dir = PATH.REPORT_PATH
        lists = os.listdir(test_dir)
        # sort按key的关键字进行排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间
        # 最后对lists元素，按文件修改时间大小从小到大排序。
        lists.sort(key=lambda fn: os.path.getmtime(test_dir + '/' + fn))
        # 获取最新文件的绝对路径
        file_path = os.path.join(test_dir, lists[-1])

        return file_path
