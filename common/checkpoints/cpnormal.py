#!/usr/bin/env python
# -*- coding:utf-8 -*-

from logger.Logger import BaseLineLogger

__author__ = ''


class BaseLineCpNormal:
    log = BaseLineLogger.get_log()

    def __init__(self):
        pass

    @staticmethod
    def check_points(dict_cp, dict_ret, case_name, case_id):
        if not isinstance(dict_ret, dict) or not isinstance(dict_cp, dict):
            raise TypeError

        def compare_val(src, dest):
            for key in src:
                if key not in dest.keys():
                    msg = 'not found expected %s key from response' % (key,)
                    return False, msg

                if isinstance(src[key], dict) and isinstance(dest[key], dict):
                    return compare_val(src[key], dest[key])
                else:
                    print(src[key])
                    rtn = True
                    if src[key] == "*":
                        if dest[key] == "":
                            rtn = False

                    elif src[key] != dest[key]:
                        rtn = False

                    msg = 'expected[%s]=%s, response[%s]=%s' % (key, src[key], key, dest[key])

                    BaseLineCpNormal.log.info("[%s(%s)]: check_point: %s=%s, response: %s=%s",
                                              *(case_name, case_id, key, src[key], key, dest[key]))
                    return rtn, msg

        return compare_val(dict_cp, dict_ret)

