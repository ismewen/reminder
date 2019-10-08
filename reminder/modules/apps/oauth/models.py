from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    group_name = models.CharField(max_length=128, default="support", verbose_name="Group Name")
    group_id = models.IntegerField(verbose_name="group id", default=100)
    open_id = models.CharField(max_length=128, verbose_name="Wechat Open Id")
