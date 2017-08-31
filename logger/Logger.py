#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
from _datetime import datetime
import logging
import threading

__author__ = ''

proDir = os.path.split(os.path.realpath(__file__))[0]
logPath = ""
resultPath = ""


# Logger
class Logger:
    def __init__(self, log2file=True, log2console=None):
        global logPath, resultPath, proDir
        # defined logger
        self.logger = logging.getLogger()
        # defined log level
        self.logger.setLevel(logging.INFO)

        if log2file:
            resultPath = os.path.join(proDir, "result")
            # create result file if it doesn't exist
            if not os.path.exists(resultPath):
                os.mkdir(resultPath)
            # defined test result file name by localtime
            logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
            # create test result file if it doesn't exist
            if not os.path.exists(logPath):
                os.mkdir(logPath)

            # defined handler
            handler = logging.FileHandler(os.path.join(logPath, "output.log"))
            # defined formatter
            formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s] %(message)s')
            # defined formatter
            handler.setFormatter(formatter)
            # add handler
            self.logger.addHandler(handler)

        if log2console:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s] %(message)s')
            console.setFormatter(formatter)
            self.logger.addHandler(console)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def cir(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


class BaseLineLogger:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if BaseLineLogger.log is None:
            BaseLineLogger.mutex.acquire()
            BaseLineLogger.log = Logger(log2file=None, log2console=True)
            BaseLineLogger.mutex.release()
        return BaseLineLogger.log


if __name__ == '__main__':
    log = BaseLineLogger.get_log()
    # logger = log.get_logger()
    log.info("this is a debug test")
