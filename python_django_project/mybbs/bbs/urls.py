"""mybbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from bbs import views


urlpatterns = [
    path('', views.index),
    re_path('category/(\d+)/', views.category),
    re_path('detail/(\d+)/', views.article_detail, name="article_detail"),
    re_path('comment/', views.comment, name="post_comment"),
    re_path('comment_list/(\d+)/', views.get_comments, name="get_comments"),
    re_path('new-article/', views.new_article, name="new-article"),
    re_path('file_upload/', views.file_upload, name="file_upload"),
    re_path('latest_article_count/', views.get_latest_article_count, name="get_latest_article_count"),
]