# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

"""
处理所有数据库交互
"""

import json,time, os
from conf import settings


def file_db_handle(conn_params):
    """
    解析数据库文件路径   文件类型数据库
    :param conn_params: 在设置中设置的数据库连接参数
    :return:
    """
    print('file db:', conn_params)
    return file_execute   # 统一处理规定的sql语句


def db_handler():    # 解耦出不同数据库类型  增加可扩展性
    """
    链接db
    :return:
    """
    conn_params = settings.DATABASE
    # 功能解耦
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass


def file_execute(sql, **kwargs):     # 所有数据库，统一处理规定的sql语句
    conn_params = settings.DATABASE
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])

    print(sql, db_path)
    sql_list = sql.split("where")
    print(sql_list)
    if sql_list[0].startswith("select") and len(sql_list) > 1:
        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)
            print(account_file)
            if os.path.isfile(account_file):
                with open(account_file, "r") as f:
                    account_data = json.load(f)
                    return account_data
                #account_file.close()
            else:
                exit("\033[31;1m 账号不存在 %s \033[0m]]" % val)
    elif sql_list[0].startswith("update") and len(sql_list) > 1:#has where clause
        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)
            #print(account_file)
            if os.path.isfile(account_file):
                account_data = kwargs.get("account_data")
                with open(account_file, 'w') as f:
                    acc_data = json.dump(account_data, f)
                return True
