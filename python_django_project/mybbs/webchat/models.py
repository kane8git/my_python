from django.db import models
from bbs.models import UserProfile
# Create your models here.


# 群
class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # 创建者
    admins = models.ManyToManyField(UserProfile, blank=True, related_name="group_admin")   # 管理员
    members = models.ManyToManyField(UserProfile, blank=True, related_name="group_members")
    max_members = models.IntegerField(default=200)

    def __str__(self):
        return self.name























