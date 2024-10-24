#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/25 09:58
# @Author  : 作者名:张铁君
# @Site    : 数据库初始化
# @File    : mysql_operation.py
# @Project : bh5_auto_test
# @Software: PyCharm
from peewee import MySQLDatabase
import pymysql


class mysql_operation:
    def __init__(self, mysql_con):
        self.host = mysql_con["host"]
        self.db = mysql_con["db"]
        self.port = mysql_con["port"]
        self.user = mysql_con["user"]
        self.password = mysql_con["password"]
        self.conn = None
        self.cur = None
        # 私有方法

    def open(self):
        pymysql.install_as_MySQLdb()
        # 创建MySQL数据库连接
        db = MySQLDatabase(self.db, user=self.user, password=self.password, host=self.host, port=self.port)
        return db
