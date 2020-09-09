# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

from conf import settings
from core import accounts
from core import logger


def make_transaction(log_obj, account_data, tran_type, amount, **others):
    """
    处理所有的用户交易
    :param log_obj: 日志记录
    :param account_data: 用户账号信息
    :param tran_type: 交易类型
    :param amount: 交易金额
    :param others: 主要用于扩展其他参数
    :return:
    """
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = account_data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance - amount - interest
            # check credit  检查结果
            if new_balance < 0:
                print("您的信用额度不够！")
                return
        account_data['balance'] = new_balance
        accounts.dump_account(account_data)  # save the new balance back to file
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" % (account_data['id'], tran_type, amount, interest))
        return account_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)

