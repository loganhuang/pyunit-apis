# coding:utf-8
#! /usr/bin/env python

from utils.sqlite3 import BaseLineSqlite3
from config.config import BaselineConfig
from common.const.const import PATH


def save_test_result(data):
    config = BaselineConfig(PATH.CONFIG_INI_FILE)
    t_name = config.get_db_result_table()
    db_name = config.get_db_name()

    if not isinstance(t_name, str) or not isinstance(db_name, str):
        return

    if len(t_name) <= 0 or len(db_name) <= 0:
        return

    sql = """INSERT INTO %(tableName)s ("name", "starttime", "endtime", "total", "passcnt", "fail", "error", "report")
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                  """ % {'tableName': t_name}
    sqlengin = BaseLineSqlite3()
    conn = sqlengin.get_conn(db_name)
    sqlengin.save(conn, sql, data)