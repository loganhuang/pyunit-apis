#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import os

__author__ = ''


# 配置类
class BaselineConfig:
    # 配置要测试接口服务器的ip、端口、域名等信息

    def __init__(self, ini_file):
        if not os.path.exists(ini_file):
            # TODO
            pass

        config = configparser.ConfigParser()
        # 从配置文件中读取接口服务器IP、域名，端口
        config.read(ini_file)
        # self.server_host = config['HTTP']['host']
        # self.server_port = config['HTTP']['port']
        self.service_dict = {
            'api': {'host': config['APISERVER']['host'], 'port': config['APISERVER']['port']},
            'web': {'host': config['WEBSERVER']['host'], 'port': config['WEBSERVER']['port']},
            'monitor': {'host': config['MONSERVER']['host'], 'port': config['MONSERVER']['port']}
        }


        self.email_smtp = config['EMAIL']['smtp']
        self.email_user = config['EMAIL']['user']
        self.email_pwd = config['EMAIL']['pwd']
        self.email_receiver = config['EMAIL']['receiver']
        self.db_path = None
        self.db_api_table = None
        self.db_monitor_table = None
        self.db_web_table = None


        try:
            self.test_categories = config['OTHER']['test_categories'].split(';')
        except Exception as e:
            self.test_categories = ['api']
            print('%s' % e)

        try:
            self.db_path = config['DATABASE']['path']
            if 'api' in self.test_categories:
                self.db_api_table = config['DATABASE']['apitable']

            if 'monitor' in self.test_categories:
                self.db_monitor_table = config['DATABASE']['monitortable']

            if 'web' in self.test_categories:
                self.db_web_table = config['DATABASE']['webtable']

        except Exception as e:
            print('%s' % e)

    def get_server_by_key(self, key):
        service_dict = self.service_dict[key]
        return tuple([service_dict['host'], service_dict['port']])


    # def set_host(self, host):
    #     self.server_host = host
    #
    # def get_host(self):
    #     return self.server_host
    #
    # def set_port(self, port):
    #     self.server_port = port
    #
    # def get_port(self):
    #     return self.server_port

    def set_email_smtp(self, smtp):
        self.email_smtp = smtp

    def get_email_smtp(self):
        return self.email_smtp

    def set_email_user(self, user):
        self.email_user = user

    def get_email_user(self):
        return self.email_user

    def set_email_pwd(self, pwd):
        self.email_pwd = pwd

    def get_email_pwd(self):
        return self.email_pwd

    def set_email_receiver(self, receivers):
        self.email_receiver.append(receivers)

    def get_email_receiver(self):
        return self.email_receiver

    def get_db_name(self):
        return self.db_path

    def get_db_api_table(self):
        return self.db_api_table

    def get_db_web_table(self):
        return self.db_web_table

    def get_db_monitor_table(self):
        return self.db_monitor_table


if __name__ == '__main__':
    this_dir = os.path.dirname(__file__)
    config = BaselineConfig(this_dir + "/config.ini")
    print("ip=%s, port=%s" % (config.get_host(), config.get_port()))
    print("smtp=%s, user=%s, pwd=%s" % (config.get_email_smtp(), config.get_email_user(), config.get_email_pwd()))
    print("receivers=" + config.get_email_receiver())
