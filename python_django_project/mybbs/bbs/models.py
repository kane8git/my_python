from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
import os

# Create your models here.


# 帖子
class Article(models.Model):
    title = models.CharField(max_length=255)   # 标题
    brief = models.CharField(null=True, blank=True, max_length=255)  # 简介
    category = models.ForeignKey("Category", on_delete=models.CASCADE)  # 版块 要加引号自动反射找到下面的表
    content = models.TextField(u"文章内容")    # 内容
    author = models.ForeignKey("UserProfile", on_delete=models.CASCADE)   # 作者
    pub_date = models.DateTimeField(blank=True, null=True)   # 文件发布时间
    last_modify = models.DateTimeField(auto_now=True)   # 最后一次修改时间
    priority = models.IntegerField(u"优先级", default=1000)  # 帖子优先级
    head_img = models.ImageField(u'文章标题图片', upload_to="uploads")  # 每个文章关联一个图片
    status_choices = (
        ('draft', u"草稿"),
        ('published', u"已发布"),
        ('hidden', u"隐藏"),
    )
    status = models.CharField(choices=status_choices, default='published', max_length=64)

    def __str__(self):
        return self.title

    def clean(self):
        # Don't allow draft entries to have a pub_date
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError('Draft entries may not have a publication date.')
        # Set the pub_date for published items if it hasn't been set already.
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()


# 评论
class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name=u"所属文章", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', related_name='my_children', blank=True, null=True, on_delete=models.CASCADE)
    comment_choices = (
        (1, u'评论'),
        (2, u'点赞'),
    )   # 评论类型列表（评论，点赞）
    comment_type = models.IntegerField(choices=comment_choices, default=1)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)  # 评论用户
    comment = models.TextField(blank=True, null=True)  # 评论内容
    date = models.DateTimeField(auto_now_add=True)  # 评论时间

    def clean(self):
        if self.comment_type == 1 and len(self.comment) == 0:
            raise ValidationError(u'评论内容不能为空。')

    def __str__(self):
        return "C:%s" % (self.comment)


# 板块
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    brief = models.CharField(null=True, blank=True, max_length=255)  # 简介
    set_as_top_menu = models.BooleanField(default=False)   # 该板块是否展示
    position_index = models.SmallIntegerField()  # 板块展示的位置
    admins = models.ManyToManyField("UserProfile", blank=True)  # 板块和用户表的外键

    def __str__(self):
        return self.name


# 用户信息
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    signature = models.CharField(max_length=255, blank=True, null=True)  # 个人简介
    head_img = models.ImageField(height_field=150, width_field=150, blank=True, null=True)  # 头像
    # for web qq
    friends = models.ManyToManyField('self', related_name="my_friends", blank=True)
    def __str__(self):
        return self.name









