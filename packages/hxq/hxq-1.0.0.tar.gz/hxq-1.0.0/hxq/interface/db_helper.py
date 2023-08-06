# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 23:38
# @Author  : hxq
# @Software: PyCharm
# @File    : db_helper.py
from hxq.libs.db.db_helper import DBHelper

if __name__ == '__main__':
    CONFIG = {
        'SQL_CREATOR': 'MySQL',
        'SQL_HOST': '127.0.0.1',
        'SQL_USER': 'root',
        'SQL_PASSWORD': 'key123123',
        'SQL_DATABASE': 'blog'
    }
    db = DBHelper(config=CONFIG)
    print(db.first("SELECT * FROM  rule_group")[0].get("update_time"))
