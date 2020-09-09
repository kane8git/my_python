# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

'''
主程序处理模块，处理所有用户交互的东西
'''

import time

from core import auth
from core import accounts
from core import logger
from core import accounts
from core import transaction
from core.auth import login_required

# transaction logger  交易记录器
trans_logger = logger.logger('transaction')
# access logger   访问记录器
access_logger = logger.logger('access')

# 临时帐户数据，仅将数据保存在内存中,验证登陆状态需要在每个方法里面用
user_data = {
    'account_id': None,  # 账户id
    'is_authenticated': False,  # 是否已经验证
    'account_data': None  # 账户信息
}


def account_info(acc_data):
    print(user_data)


@login_required
def repay(acc_data):
    '''
    print current balance and let user repay the bill
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    #for k,v in account_data.items():
    #    print(k,v )
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount ('b' exit):\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            print('ddd 00')
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif repay_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)




def withdraw(acc_data):
    """
    打印当前余额并让用户执行提款操作
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = '''
        --------- 余额信息 --------
        Credit : %s
        Banlance: %s
    ''' %(account_data['credit'],account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1m input withdraw amount(if want back use 'b'):\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif withdraw_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)





def transfer(acc_data):
    pass


def pay_check(acc_data):
    pass


def logout(acc_data):
    exit(0)

def interactive(acc_data):
    """
    和用户进行交互
    :param acc_data:  # 账户信息
    :return:
    """
    # 前面加了 u 代表以unicode方式来存储
    menu = u'''    
    ---------  test Bank ------
    \033[32;1m 1. 账号信息
    2. 还款
    3. 取款
    4. 转账
    5. 账单
    6. 退出
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>>:").strip()
        if user_option in menu_dic:
            print('accdata', acc_data)
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1m选项不存在\033[0m")


def run():
    """
    该函数将在程序启动时被正确调用，这里处理用户交互的东西：
    :return:
    """
    acc_data = auth.acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)  # 交互
