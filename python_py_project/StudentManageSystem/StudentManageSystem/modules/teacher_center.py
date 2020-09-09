from modules import authentication
from models import datasheet
from conf import settings
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

class Teacher(object):
    def __init__(self):
        Session_class = sessionmaker(bind=datasheet.engine)
        self.session = Session_class()
        self.tea_id = self.__auth()
        self.interactive()

    def interactive(self):
        while True:
            menu = '''
1.创建班级
2.招收学员
3.创建学习记录
4.批改作业
q.退出
'''
            print("\033[1;33m欢迎来到学生管理系统/讲师中心\033[0m".center(40, "*"), menu)
            choice = input("请输入选择ID>>>:")
            if choice == "1":
                self.create_class()
            elif choice == "2":
                self.enrolling_student()
            elif choice == "3":
                self.create_record()
            elif choice == "4":
                self.correct_work_score()
            elif choice == "q":
                print("\033[1;34m感谢您使用学生管理系统/讲师中心\033[0m")
                break

    def create_class(self):
        '''创建班级，开设课程'''
        while True:
            max_count = settings.class_days  # 课程最大周期数
            course = input("请输入您创建班级的课程名>>>:")
            if not course: continue
            class_day = int(input("请输入课程周期天数[最大为:%s]>>>:" % (max_count)))
            if class_day > max_count:
                print("输入错误!")
                break
            class_obj = datasheet.Class(course=course)
            tea_obj = self.session.query(datasheet.Teacher).filter(datasheet.Teacher.id == self.tea_id).first()
            class_obj.teacher = [tea_obj, ]
            self.session.add(class_obj)
            self.session.commit()
            self.session.flush()
            class_lesson_list = []
            count = 1
            while count <= class_day:
                lesson_class_obj = datasheet.lesson_MtoM_class(lesson_id=count,class_id=class_obj.id)
                class_lesson_list.append(lesson_class_obj)
                count += 1
            self.session.add_all(class_lesson_list)
            self.session.commit()
            if_continue = input("创建[%s班级]成功，是否继续创建?Y/N>>>:" % (course))
            if if_continue == "Y":
                continue
            else:
                break

    def enrolling_student(self):
        '''招收学员'''
        while True:
            class_list = []
            qq = input("请输入招收学员的QQ号>>>:")
            if not qq: continue
            stu_obj = self.session.query(datasheet.Student).filter(datasheet.Student.qq == qq).first()
            if not stu_obj:
                print("不存在此学生!")
                break
            tea_obj = self.session.query(datasheet.Teacher).filter(datasheet.Teacher.id == self.tea_id).first()
            all_class_obj = tea_obj.banji
            class_obj_list = [] #存放班级实例
            while True:
                class_id = input("请输入学员加入的班级ID>>>:")
                query_class_obj = self.session.query(datasheet.Class).filter(datasheet.Class.id==class_id).first()
                if query_class_obj not in all_class_obj:
                    print("不存在此班级或您对此班级没有权限!")
                    continue
                if stu_obj in query_class_obj.student:
                    print("班级[ID:%s]中已存在此学生!"%(class_id))
                    continue
                if_continue = input("该学生是否要加入其他班级?Y/N>>>:")
                if if_continue == "Y":
                    class_obj_list.append(query_class_obj)
                    continue
                else:
                    class_obj_list.append(query_class_obj)
                    break
            stu_obj.banji = class_obj_list
            self.session.add(stu_obj)
            self.session.commit()
            if_continue = input("招收[学员%s]成功，是否继续招收新的学员?Y/N>>>:" % (stu_obj.name))
            if if_continue == "Y":
                continue
            else:
                break

    def create_record(self):
        '''为学生创建上课记录'''
        while True:
            class_id = input("请输入班级ID:>>>:")
            tea_obj = self.session.query(datasheet.Teacher).filter(datasheet.Teacher.id == self.tea_id).first()
            all_class_obj = tea_obj.banji
            query_class_obj = self.session.query(datasheet.Class).filter(datasheet.Class.id==class_id).first()
            if query_class_obj not in all_class_obj:
                print("班级不存在或您对此班级没有权限!")
                break
            class_day = input("请输入班级lesson day>>>:")
            lesson_obj = self.session.query(datasheet.Lesson).filter(datasheet.Lesson.class_day == class_day).first()
            if not lesson_obj:
                print("输入错误!")
                break
            lesson_class_obj = self.session.query(datasheet.lesson_MtoM_class).filter(
                datasheet.lesson_MtoM_class.lesson_id == lesson_obj.id,
                 datasheet.lesson_MtoM_class.class_id == class_id).first()
            if not lesson_class_obj:
                print("不存在这个班级课节!")
                break
            lesson_class_id = lesson_class_obj.id
            query_learn_record = lesson_class_obj.learn_record
            if not query_learn_record:
                pass
            else:
                print("班级[ID:%s] lesson day[day:%s]的记录已存在!"%(class_id,class_day))
                break
            all_student_obj = query_class_obj.student
            learn_record_list = []  # 存放LearnRecord实例
            for stu_obj in all_student_obj:
                while True:
                    if_absence = input("请输入学生[姓名: %s qq: %s]是否正常上课?Y/N>>>:" % (stu_obj.name, stu_obj.qq))
                    if if_absence == "Y" or if_absence == "N":
                        obj = datasheet.LearnRecord(stu_id=stu_obj.id, lesson_class_id=lesson_class_id,
                                                    status=if_absence)
                        learn_record_list.append(obj)
                        break
                    else:
                        print("输入错误，请重新输入!")
            self.session.add_all(learn_record_list)
            self.session.commit()
            if_continue = input("为班级[ID: %s]创建学习记录完毕,是否为其他班级创建学习记录?Y/N>>>:"%(class_id))
            if if_continue == "Y":
                continue
            else:
                break

    def correct_work_score(self):
        '''为学生批改成绩'''
        while True:
            class_id = input("请输入班级ID:>>>:")
            class_day = input("请输入班级lesson day>>>:")
            if not class_id or not class_day:continue
            lesson_obj = self.session.query(datasheet.Lesson).filter(datasheet.Lesson.class_day==class_day).first()
            if not lesson_obj:
                print("不存在此班级lesson day!")
                break
            lesson_class_obj = self.session.query(datasheet.lesson_MtoM_class).filter(
                datasheet.lesson_MtoM_class.class_id==class_id,
                datasheet.lesson_MtoM_class.lesson_id==lesson_obj.id).first()
            if not lesson_class_obj:
                print("不存在此班级课节!")
                break
            all_learn_record = lesson_class_obj.learn_record
            if not all_learn_record:
                print("此班级课节未完成，无法批改成绩!")
                break
            for learn_record_obj in all_learn_record:
                while True:
                    print("学号ID: %s 作业完成情况: %s 考勤记录: %s"%(learn_record_obj.stu_id,
                                                      learn_record_obj.homework,learn_record_obj.status))

                    score = int(input("请为该学生打上成绩>>>:"))
                    if score >= settings.min_score and score <= settings.max_score:
                        learn_record_obj.score = score
                        break
                    else:
                        print("输入范围超过限制,请重新输入!")
            self.session.commit()
            if_continue = input("班级[ID:%s]的作业以批改完毕，是否继续批改其他班级的作业?Y/N>>>:")
            if if_continue == "Y":
                continue
            else:
                break

    def __auth(self):
        res = authentication.auth_teacher_center()
        if res[0] == "false":
            return
        return res[1]