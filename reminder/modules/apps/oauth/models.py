from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    open_id = models.CharField(max_length=128, verbose_name="Wechat Open Id")
