# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import os
import json
import time

from core import db_handler
from conf import settings
from core import logger


def login_required(func):
    """
    验证用户是否登陆
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        if args[0].get('is_authenticated'):
            return func(*args, **kwargs)
        else:
            exit("User is not authenticated.")
    return wrapper


def acc_auth2(account, password):
    """
    优化版认证接口
    :param account:
    :param password:
    :return:
    """
    db_api = db_handler.db_handler()
    data = db_api("select * from accounts where account=%s" % account)
    if data['password'] == password:
        exp_time_stamp = time.mktime(time.strptime(data['expire_date'], "%Y-%m-%d"))
        if time.time() > exp_time_stamp:
            print("\033[31;1m 账户已过期 \033[0m")
        else:   # 通过认证
            return data
    else:
        print("\033[31;1m 账户id不正确\033[0m")


def acc_login(user_data, log_obj):
    """
    帐户登录功能
    :param user_data: 用户信息数据，仅保存在内存中
    :param log_obj:  写日志
    :return:
    """
    retry_count = 0    # 重试次数
    while user_data['is_authenticated'] is not True and retry_count < 3:
        account = input("\033[32;1m account: \033[0m").strip()
        password = input("\033[32;1m password: \033[0m").strip()
        auth = acc_auth2(account, password)
        if auth:  # None = False auth != None  没有None 意思通过认证
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            return auth
        retry_count += 1
    else:
        log_obj.error("account [%s] too many login attempts" % account)
        exit()






