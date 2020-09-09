# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import json
import time
from core import db_handler
from conf import settings

def load_current_balance(account_id):
    """
    查询 账户余额及其他信息
    :param account_id:
    :return:
    """
    db_api = db_handler.db_handler()
    data = db_api("select * from accounts where account=%s" % account_id)
    return data

def dump_account(account_data):
    """
    更新 交易或帐户数据后，将其转回文件db
    :param account_data:
    :return:
    """
    db_api = db_handler.db_handler()
    data = db_api("update accounts where account=%s" % account_data['id'], account_data=account_data)
    return True




