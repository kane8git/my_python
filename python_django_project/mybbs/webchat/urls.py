# -*- coding: utf-8 -*-
# author : anthony
# version : python 3.6
from django.urls import path, include

from django.conf.urls import url, include
from webchat import views

urlpatterns = [
    path('', views.dashboard, name='chat_dashboard'),
    path('msg_send', views.send_msg, name='send_msg'),
    path('new_msgs', views.get_new_msgs, name='get_new_msgs'),
    path('file_upload', views.file_upload, name='file_upload'),
    path('upload_progress', views.file_upload_progress, name='file_upload_progress'),
    path('delete_cache_key', views.delete_cache_key, name='delete_cache_key'),
]






