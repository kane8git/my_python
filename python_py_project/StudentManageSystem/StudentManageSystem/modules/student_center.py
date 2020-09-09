# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import random
from models import datasheet
from modules import authentication
from sqlalchemy.orm import sessionmaker

class Student(object):
    def __init__(self):
        Session_obj = sessionmaker(bind=datasheet.engine)
        self.session = Session_obj()
        self.interactive()

    def interactive(self):
        while True:
            menu = '''
            1、学员注册
            2、上传作业
            3、查看成绩
            q、退出
            '''
            print('\033[1;33m 欢迎来到学生管理系统/学员中心 \033[0m'.center(40, '*'), menu)
            user_choice = input("input your choice ID >>>:")
            if user_choice == "1":
                self.sign_up()
            elif user_choice == '2':
                self.up_work()
            elif user_choice == '3':
                self.check_grage()
            elif user_choice == 'q':
                print("\033[1;34m 感谢您使用学生管理系统/学员中心 \033[0m")
                break

    def sign_up(self):
        """ 学员注册"""
        while True:
            name = input('input your name>>>:')
            qq = input("input your QQ number>>>:")
            if not name or not qq:
                continue
            query_student = self.session.query(datasheet.Student).filter(datasheet.Student.qq == qq).first()
            if not query_student:
                password = str(random.randint(1000, 10000))  # 随机生产1000-10000中的一个整数
                stu_obj = datasheet.Student(name=name, qq=qq, password=password)
                self.session.add(stu_obj)
                self.session.commit()
                query_stu_obj = self.session.query(datasheet.Student).filter(datasheet.Student.qq == qq).first()
                print('学员 [name: %s]注册成功' % name)
                print('请记住登陆信息:\n'
                      '学号[ID :%s] \n'
                      '密码[password: %s]' % (query_stu_obj.id, password))
                break
            else:
                print('此学员已注册成功！')
                break

    def up_work(self):
        """ 上传作业"""
        learn_record_obj, lesson_day, lesson_class_id = self.__learn_record()
        if learn_record_obj.homework:
            print('[lesson day: %s]作业已上传！' % (lesson_day))
        else:
            learn_record_obj.homework = 'Y'
            self.session.commit()
            print("【lesson day: %s】作业上传完毕"% (lesson_day))

    def check_grade(self):
        """ 查看成绩、排名"""
        learn_record_obj, lesson_day, lesson_class_id = self.__learn_record()
        score = learn_record_obj.score
        if not score:
            print("作业还未批改完毕!")
        else:
            fewer_score_count = self.session.query(datasheet.LearnRecord).filter(
                                                                                 datasheet.LearnRecord.score > score,
                                                                                 datasheet.LearnRecord.lesson_class_id == lesson_class_id
                                                                                ).count()
            print("【lesson_day: %s】【grade: %s】【ranking: %s】" % (lesson_day, score, fewer_score_count+1))

    def __learn_record(self):
        """ 登陆后，获取learn_record_obj"""
        res = authentication.auth_student_center()
        if res[0] == "false":
            return
        stu_id = res[1]
        stu_obj = self.session.query(datasheet.Student).filter(datasheet.Student.id == stu_id).first()
        while True:
            class_id = input('请输入班级ID>>>:')
            lesson_day = input('请输入班级lesson day>>>:')
            query_lesson_obj = self.session.query(datasheet.Lesson).filter(
                                                                          datasheet.Lesson.class_day == lesson_day
                                                                          ).first()
            if not query_lesson_obj:
                print("此班级lesson day不存在，请重新输入!")
                continue
            query_class_obj = self.session.query(datasheet.Class).filter(datasheet.Class.id == class_id).first()
            if not query_class_obj:
                print("此班级不存在，请重新输入!")
                continue
            if stu_obj not in query_class_obj.student:
                print("您不是此班级的学生!")
                continue
            lesson_class_obj = self.session.query(datasheet.lesson_MtoM_class).filter(
                datasheet.lesson_MtoM_class.class_id == class_id,
                datasheet.lesson_MtoM_class.lesson_id == query_lesson_obj.id
            ).first()
            learn_record_obj = self.session.query(datasheet.LearnRecord).filter(
                datasheet.LearnRecord.stu_id == stu_id,
                datasheet.LearnRecord.lesson_class_id == lesson_class_obj.id
            ).first()

            if not learn_record_obj:
                print("此次班级课节还未完成,无法查询!")
                continue
            break
        return learn_record_obj, lesson_day, lesson_class_obj.id























































