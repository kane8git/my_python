# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6
# mysql 连接交互

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import settings

engine = create_engine(settings.ConnParams)
# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
SessionCls = sessionmaker(bind=engine)
session = SessionCls()





