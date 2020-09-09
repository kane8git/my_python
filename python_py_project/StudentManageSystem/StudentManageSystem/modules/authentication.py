# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

from sqlalchemy.orm import sessionmaker
from models import datasheet

Session_class = sessionmaker(bind=datasheet.engine)
session = Session_class()


def auth(auth_type):
    def out_wrapper(func):
        def wrapper():
            if auth_type == 'auth_student':
                stu_id = input('请输入学号ID>>>:')
                password = input('请输入密码password>>>:')
                query_stu_obj = session.query(datasheet.Student).filter(
                                                                        datasheet.Student.id == stu_id,
                                                                        datasheet.Student.password == password
                                                                        ).first()
                if query_stu_obj:
                    res = func()
                    return res, stu_id
                else:
                    print('学员ID或密码输入错误！')
                    return 'false'
            elif auth_type == 'auth_teacher':
                tea_id = input('请输入职工号ID>>>:')
                password = input('请输入密码password>>>:')
                query_tea_obj = session.query(datasheet.Teacher).filter(
                                                                        datasheet.Teacher.id == tea_id,
                                                                        datasheet.Teacher.password == password
                                                                       ).first()
                if query_tea_obj:
                    res = func()
                    return res, tea_id
                else:
                    print('教职工号ID或密码输入错误！')
                    return 'false'
        return wrapper
    return out_wrapper


@auth(auth_type='auth_student')
def auth_student_center():
    return 'true'


@auth(auth_type='auth_teacher')
def auth_teacher_center():
    return 'true'















