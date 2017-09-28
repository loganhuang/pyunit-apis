#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from logger.Logger import BaseLineLogger

__author__ = ''

class BaseLineWebDriver:

    def __init__(self, base_url, port=None):
        self.base_url = "https://" + base_url
        self.port = port
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)  # 隐性等待时间为30秒
        self.log = BaseLineLogger.get_log()

    def open_page(self, page):
        if not isinstance(page, str):
            raise TypeError
        self.log.info("open_page:" + self.base_url + page)
        self.driver.get(self.base_url + page)

    def close_page(self, page=None):
        self.driver.close()

    def close_all_page(self):
        self.driver.quit()

    def get_text_by_xpath(self, xpath):
        if not isinstance(xpath, str):
            raise TypeError

        ele = self.driver.find_element_by_xpath(xpath)
        if ele:
            return ele.text
        else:
            return None

    def get_text_by_id(self, ele_id):
        if not isinstance(ele_id, str):
            raise TypeError

        ele = self.driver.find_element_by_id(ele_id)
        if ele:
            return ele.text
        else:
            return None

    def fill_box_by_id(self, ele_id, value):
        if not isinstance(ele_id, str):
            raise TypeError

        ele = self.driver.find_element_by_id(ele_id)
        if ele:
            ele.send_keys(value)
        else:
            self.log.info("not found the element by id=" + ele_id)

    def fill_box_by_xpath(self, xpath, value):
        if not isinstance(xpath, str):
            raise TypeError

        ele = self.driver.find_element_by_xpath(xpath)
        if ele:
            ele.send_keys(value)
        else:
            self.log.info("not found the element by xpath=" + xpath)

    def click_by_id(self, ele_id):
        if not isinstance(ele_id, str):
            raise TypeError

        ele = self.driver.find_element_by_id(ele_id)
        if ele:
            ele.click()
        else:
            self.log.info("not found the element by id=" + ele_id)

    def click_by_xpath(self, xpath):
        if not isinstance(xpath, str):
            raise TypeError

        ele = self.driver.find_element_by_xpath(xpath)
        if ele:
            ele.click()
        else:
            self.log.info("not found the element by xpath=" + xpath)

    # TODO, implement more other methods