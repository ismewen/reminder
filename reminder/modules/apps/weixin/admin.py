from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models


# Register your models here.


class BirthDayRecordAdmin(admin.ModelAdmin):
    list_display = [
        "user", "name", "birth_day", "is_lunar_calendar", "phone_number"
    ]
    search_fields = "name", "type",
    list_per_page = 20
    ordering = ('-id',)


admin.site.register(models.BirthDayRecord, BirthDayRecordAdmin)
