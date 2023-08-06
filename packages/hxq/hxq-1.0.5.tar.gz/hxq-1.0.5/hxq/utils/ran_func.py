# -*- coding: utf-8 -*-
# @Time    : 2022/7/9 22:21
# @Author  : hxq
# @Software: PyCharm
# @File    : ran_func.py
import string
import random


def random_password(length=12):
    """
    随机密码生成
    """
    return ''.join(random.sample(string.digits + string.ascii_letters * 1, length))
