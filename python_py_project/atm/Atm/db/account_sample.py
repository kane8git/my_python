# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6


import json

acc_dic = {
    'id': 1234,
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2030-01-02',
    'pay_day': 22,
    'status': 0  # 0 = normal, 1 = locked, 2 = disabled
}

print(json.dumps(acc_dic))





