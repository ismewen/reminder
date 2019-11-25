from datetime import datetime

import arrow
import sxtwl

from django.db import models

# Create your models here.
from modules.apps.oauth.models import User

lunar = sxtwl.Lunar()  # 实例化日历库
ymc = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rmc = [
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"
]


class BirthDayRecord(models.Model):
    user = models.ForeignKey('oauth.User', verbose_name="user", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name="姓名", max_length=255)
    birth_day = models.DateField(verbose_name="生日")
    phone_number = models.CharField(verbose_name="电话号码", max_length=64, default="")
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

    @property
    def has_reminder_key(self):
        return "HAS:REMINDER:FLAG:%s" % self.id


def create_today_star_user_for_test():
    user = User.objects.filter(username="ethan").first()
    today = arrow.now().date()
    if not user:
        return
    lunar_record = BirthDayRecord.objects.get_or_create(user=user,
                                                        is_lunar_calendar=1, name="农历-ethan", birth_day=today)[0]
    day = lunar.getDayBySolar(today.year, today.month, today.day)
    birth_day = arrow.get("%s-%s-%s" % (today.year, ymc[day.Lmc], day.Ldi + 1)).date()
    lunar_record.birth_day = birth_day
    lunar_record.save()
    solar_record = BirthDayRecord.objects.get_or_create(user=user,
                                                        is_lunar_calendar=2, name="公历-ethan", birth_day=today)[0]
    solar_record.birth_day = today
    solar_record.save()




