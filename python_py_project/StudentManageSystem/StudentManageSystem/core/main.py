# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

from modules import student_center, teacher_center
from models import datasheet
from conf import settings
from sqlalchemy.orm import sessionmaker

class MainLogic(object):
    def __init__(self):
        self.__initialization()
        self.interactive()

    def interactive(self):
        while True:
            menu = '''
            1、学生中心
            2、讲师中心
            q、退出'''
            print('\033[1;33m 欢迎来到学员管理系统 \033[0m'.center(40, '*').strip(), menu)
            user_choice = input('input your choice ID >>>:')
            if user_choice == '1':
                student_center.Student()
            elif user_choice == '2':
                teacher_center.Teacher()
            elif user_choice == 'q':
                print('感谢您使用学员管理系统，退出ing.....')
                break

    def __initialization(self):
        """ 初始化数据库"""
        Session = sessionmaker(bind=datasheet.engine)
        session = Session()
        query_teacher = session.query(datasheet.Teacher).filter(
            datasheet.Teacher.id >= 1
        ).all()
        if not query_teacher:
            tea_obj = datasheet.Teacher(name='alex', password='111111')
            tea_obj2 = datasheet.Teacher(name='MrWu', password='222222')
            session.add_all([tea_obj, tea_obj2])
            session.commit()
            query_lesson = session.query(datasheet.Lesson).filter(
                datasheet.Lesson.id >= 1
            ).all()
            if not query_lesson:
                lesson_list = []
                day = 1
                while day <= settings.class_days:
                    lesson_obj = datasheet.Lesson(class_day=day)
                    lesson_list.append(lesson_obj)
                    day += 1
                session.add_all(lesson_list)
                session.commit()
        session.close()
        return

























