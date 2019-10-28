from datetime import datetime

import arrow
import sxtwl

from django.db import models

# Create your models here.
lunar = sxtwl.Lunar()  # 实例化日历库


class BirthDayRecord(models.Model):
    user = models.ForeignKey('oauth.User', verbose_name="user", on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(verbose_name="姓名", max_length=255)
    birth_day = models.DateField(verbose_name="生日")
    __lunar_calendar_choices__ = (
        (1, "农历"),
        (2, "公历")
    )
    is_lunar_calendar = models.IntegerField(default=1, verbose_name="历法", choices=__lunar_calendar_choices__)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="姓名")
    utime = models.DateTimeField(auto_now=True)

    def today_is_birth_day(self):
        now = datetime.now()
        if self.is_lunar_calendar == 1:
            # 农历生日
            compare_date = lunar.getDayByLunar(self.birth_day.year, self.birth_day.month, self.birth_day.day)
        else:
            # 公历生日
            compare_date = lunar.getDayBySolar(self.birth_day.year, self.birth_day.month, self.birth_day.day)
        return now.month == compare_date.m and now.day == compare_date.d

    @property
    def age(self):
        return datetime.now().year - self.birth_day.year
