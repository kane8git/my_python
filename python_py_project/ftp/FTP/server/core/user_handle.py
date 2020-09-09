# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import configparser
import hashlib
import os

from config import settings


class UserHandle(object):
    """
    创建用户名称，密码
    如果用户存在，则返回，如果用户不存在，则注册成功
    """

    def __init__(self, username):
        self.username = username
        self.config = configparser.ConfigParser()
        self.config.read(settings.ACCOUNTS_FILE)

    @property   # 把方法变成属性的装饰器
    def password(self):
        """
        生成用户的默认密码
        :return:
        """
        password_inp = input("\033[32;1mplease input your password>>>\033[0m").strip()
        md5_obj = hashlib.md5()
        md5_obj.update(password_inp.encode())
        md5_password = md5_obj.hexdigest()
        return md5_password

    @property
    def disk_quota(self):
        """
        生成每个用户的磁盘配额
        :return:
        """
        quota = input('\033[32;1mplease input Disk quotas>>>:\033[0m').strip()
        if quota.isdigit():  # 检测字符串是否只由数字组成
            return quota
        else:
            exit('\033[31;1m disk quotas must be integer \033[0m')

    def add_user(self):
        """
        创建用户，存到accounts.ini
        :return:
        """
        if not self.config.has_section(self.username):
            print('\033[31;1mcreating username is :%s \033[0m' %self.username)
            self.config.add_section(self.username)
            self.config.set(self.username, 'password', self.password)
            self.config.set(self.username, 'homedir', 'home/' + self.username)
            self.config.set(self.username, 'quota', self.disk_quota)
            with open(settings.ACCOUNTS_FILE, 'w') as f:
                self.config.write(f)
            os.mkdir(os.path.join(settings.BASE_DIR, 'home', self.username))  # 创建用户的home文件夹
            print ('\033[1;32msuccessfully create userdata\033[0m')
        else:
            print ('\033[1;31musername already existing\033[0m')

    def judge_user(self):
        """
        判断用户是否存在
        :return:
        """
        if self.config.has_section(self.username):
            return self.config.items(self.username)
















