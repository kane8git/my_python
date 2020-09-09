# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6

import sqlalchemy
from conf import settings
from sqlalchemy import Column, Table, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, UniqueConstraint

engine = create_engine(settings.conn)
Base = declarative_base()


stu_MtoM_class = Table(
    "stu_MtoM_class", Base.metadata,
    Column('stu_id', Integer, ForeignKey("student.id")),
    Column('class_id', Integer, ForeignKey("banji.id"))
)

tea_MtoM_class = Table(
    "tea_MtoM_class", Base.metadata,
    Column("tea_id", Integer, ForeignKey("teacher.id")),
    Column("class_id", Integer, ForeignKey("banji.id"))
)


class lesson_MtoM_class(Base):
    __tablename__ = "lesson_MtoM_class"
    # 建立联合唯一索引
    __table_args__ = (UniqueConstraint("lesson_id", "class_id", name="lesson_class_id"),)
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    class_id = Column(Integer, ForeignKey("banji.id"))


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    qq = Column(String(32), unique=True, nullable=False)
    password = Column(String(16), nullable=False)
    banji = relationship("Class", secondary='stu_MtoM_class', backref='student')
    learn_record = relationship('LearnRecord', backref='student')


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    password = Column(String(16), nullable=False)
    banji = relationship("Class", secondary='tea_MtoM_class', backref='teacher')


class Class(Base):
    __tablename__ = 'banji'
    id = Column(Integer, primary_key=True)
    course = Column(String(32),nullable=False)


class Lesson(Base):
    __tablename__ = 'lesson'
    id = Column(Integer, primary_key=True)
    class_day = Column(Integer, unique=True, nullable=False)


class LearnRecord(Base):
    __tablename__ = 'learn_record'
    __table_args__ = (UniqueConstraint('stu_id', 'lesson_class_id', name='stu_lesson_class_id'),)
    id = Column(Integer, primary_key=True)
    stu_id = Column(Integer, ForeignKey('student.id'))
    lesson_class_id = Column(Integer, ForeignKey('lesson_MtoM_class.id'))
    status = Column(Enum('Y', 'N'), nullable=False)
    homework = Column(Enum('Y', 'N'))
    score = Column(Integer)
    lesson_MtoM_class = relationship('lesson_MtoM_class', backref='learn_record')


Base.metadata.create_all(engine)



