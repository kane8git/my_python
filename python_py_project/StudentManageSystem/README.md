# StudentManageSystem
#学员管理系统
    - 程序要求:
        1.用户角色，讲师＼学员， 用户登陆后根据角色不同，能做的事情不同，分别如下
        2.讲师视图
            - 管理班级，可创建班级，根据学员qq号把学员加入班级
            - 可创建指定班级的上课纪录，注意一节上课纪录对应多条学员的上课纪录， 即每节课都有整班学员上，
            - 为了纪录每位学员的学习成绩，需在创建每节上课纪录是，同时为这个班的每位学员创建一条上课纪录
            - 为学员批改成绩， 一条一条的手动修改成绩
        3.学员视图
            - 提交作业
            - 查看作业成绩
            - 一个学员可以同时属于多个班级，就像报了Linux的同时也可以报名Python一样， 所以提交作业时需先选择班级，再选择具体上课的节数
            - 附加：学员可以查看自己的班级成绩排名
 
#目录结构
    |--StudentManageSystem
        |--bin
            |--start.py #程序入口
        |--conf
            |--settings.py #配置
        |--core
            |--main.py #主逻辑交互
        |--models
            |--datasheet.py #数据表
        |--modules
            |--authentication.py #登陆模块
            |--student_center.py #学生中心
            |--teacher_center.py #讲师中心
        |--logs #可扩展日志模块
        |--ReadMe.txt
 
#初始数据库
    - 默认创建两名教师
        - id: 1 name: alex  password: 111111
        - id: 2 name: MrWu  password: 222222
    - 默认创建20天教学周期
