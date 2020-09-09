# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6
# 数据库表模块


import datetime
from sqlalchemy import Table, Column, Integer, String, DATE, ForeignKey, Enum, UniqueConstraint, DateTime, Text
# uniqueconstraint 联合唯一
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType, PasswordType  # sqlalchemy_utils sqalchemy_utils插件
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # 基类

# 多对多关联
# 关联表堡垒机用户ID和远程主机ID
user_m2m_bindhost = Table('user_m2m_bindhost', Base.metadata,
                          Column('userprofile_id', Integer, ForeignKey('user_profile.id')),
                          Column('bind_host_id', Integer, ForeignKey('bind_host.id')),)
# 关联表远程主机ID和组
bindhost_m2m_hostgroup = Table('bindhost_m2m_hostgroup', Base.metadata,
                               Column('bindhost_id', Integer, ForeignKey('bind_host.id')),
                               Column('hostgroup_id', Integer, ForeignKey('host_group.id')),)

# 关联表堡垒机用户和组
user_m2m_hostgroup = Table('userprofile_m2m_hostgroup', Base.metadata,
                           Column('userprofile_id', Integer, ForeignKey('user_profile.id')),
                           Column('hostgroup_id', Integer, ForeignKey('host_group.id')),)


class BindHost(Base):
    '''
    关联关系
    192.168.1.11 web
    192.168.1.11 mysql
    '''
    __tablename__ = "bind_host"
    # 联合唯一
    __table_args__ = (UniqueConstraint('host_id', 'remoteuser_id', name='_host_remoteuser_uc'),)

    id = Column(Integer, primary_key=True)
    # 外键
    host_id = Column(Integer, ForeignKey('host.id'))
    remoteuser_id = Column(Integer, ForeignKey('remote_user.id'))
    # 外键关联远程主机，反响查绑定的主机
    host = relationship('Host', backref='bind_hosts')
    # 外键关联堡垒机用户,backref，反向查绑定的堡垒机用户
    remote_user = relationship("RemoteUser", backref='bind_hosts')

    def __repr__(self):
        # return "<%s -- %s -- %s>" % (self.host.ip,
        #                              self.remote_user.username,
        #                              self.host_group.name)

        return "<%s -- %s >" % (self.host.ip, self.remote_user.username)

class Host(Base):
    '''
    远程主机
    '''
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64), unique=True)
    ip = Column(String(64), unique=True)
    port = Column(Integer, default=22)
    # 不要让主机关联主机组，这样权限给主机组了，应该是将用户密码和主机组绑定，
    # 比如root 123 sh root 123 bj 这样他可以用所有的权限,

    def __repr__(self):
        return self.hostname

class HostGroup(Base):
    '''
    远程主机组
    '''
    __tablename__ = 'host_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    # 通过bindhost_m2m_hostgroup 关联绑定主机和主机组反查到主机组
    bind_hosts = relationship("BindHost", secondary="bindhost_m2m_hostgroup", backref="host_groups")

    def __repr__(self):
        return self.name


class RemoteUser(Base):
    '''
    远程主机密码表
    '''
    __tablename__ = 'remote_user'
    #  联合唯一,验证类型,用户名密码
    __table_args__ = (UniqueConstraint('auth_type', 'username', 'password', name='_user_passwd_uc'),)
    id = Column(Integer, primary_key=True)
    AuthTypes = [
        ('ssh-password', 'SSH/Password'),  # 第一个是存在数据库里的,第二个具体的值
        ('ssh-key', 'SSH/KEY')
    ]
    auth_type = Column(ChoiceType(AuthTypes))
    username = Column(String(32))
    password = Column(String(128))

    def __repr__(self):
        return self.username

class Userprofile(Base):
    '''
    堡垒机用户密码表
    '''
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(128))

    # 多对多关联通过user_m2m_bindhost关联堡垒机表和主机表能反查到堡垒机用户
    bind_hosts = relationship("BindHost", secondary='user_m2m_bindhost', backref='user_profiles')
    # 多对多关联通过userprofile_m2m_hostgroup关联堡垒机表和组反查到堡垒机用户
    host_groups = relationship("HostGroup", secondary='userprofile_m2m_hostgroup', backref='user_profiles')

    def __repr__(self):
        return self.username

class AuditLog(Base):
    '''
    用户操作日志表
    '''
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    bind_host_id = Column(Integer, ForeignKey('bind_host.id'))
    # # action_choices
    # action_choices = [
    #     (0, 'CMD'),
    #     (1, 'Login'),
    #     (2, 'Logout'),
    #     (3, 'GetFile'),
    #     (4, 'SendFile'),
    #     (5, 'Exception'),
    # ]
    action_choices = [
        (u'cmd', u'CMD'),
        (u'login', u'Login'),
        (u'logout', u'Logout'),
    ]

    action_type = Column(ChoiceType(action_choices))
    # 命令可能存的数值更大
    # cmd = Column(String(255))
    cmd = Column(Text(65535))
    date = Column(DateTime)

    user_profile = relationship("Userprofile")
    bind_host = relationship("BindHost")





