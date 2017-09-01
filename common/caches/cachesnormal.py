#!/usr/bin/env python
# -*- coding:utf-8 -*-

from logger.Logger import BaseLineLogger
from utils.httpmethods import BaseLineHttp

__author__ = ''


class BaseLineCachesNormal:
    log = BaseLineLogger.get_log()

    def __init__(self):
        pass

    @staticmethod
    def check_caches(dict_cache, dict_ret, http):
        if not isinstance(dict_ret, dict) or not isinstance(dict_cache, dict)\
                or not isinstance(http, BaseLineHttp):
            raise TypeError

        # {"result":{"submitToken":"Submit_token", "userToken":"OPERATOR_TOKEN"}}
        # iterator the expected cache-key-value with recursive function
        def get_key_val(ret_dict, cache_dict, out_dict):
            for key in cache_dict:
                if key not in ret_dict.keys():
                    break

                if isinstance(cache_dict[key], dict) and isinstance(ret_dict[key], dict):
                    get_key_val(ret_dict[key], cache_dict[key], out_dict)
                else:
                    out_dict[cache_dict[key]] = ret_dict[key]

        # {"header":{"result":{"submitToken":"Submit_token", "userToken":"OPERATOR_TOKEN"}}}
        # iterator the expected cache categories: header, paras, data
        for key_cache in dict_cache:
            dict_out = {}
            get_key_val(dict_ret, dict_cache[key_cache], dict_out)
            if key_cache == 'header':
                http.set_header(dict_out)

            elif key_cache == 'paras':
                http.set_paras(dict_out)
            elif key_cache == 'data':
                http.set_data(dict_out)
            else:
                pass

        pass
