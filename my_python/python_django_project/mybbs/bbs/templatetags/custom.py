# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6


from django import template
from django.utils.http import formatdate

register = template.Library()


# 自定义标签 把图片url 变成不带uploads
@register.filter
def truncate_url(img_obj):
    return img_obj.name.split("/", maxsplit=1)[-1]


# 自定义标签 点赞和评论

@register.simple_tag
def filter_comment(article_obj):
    query_set = article_obj.comment_set.select_related()
    comments = {
        'comment_count': query_set.filter(comment_type=1).count(),
        'thumb_count': query_set.filter(comment_type=2).count(),
    }
    return comments










