from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models


# Register your models here.


class BirthDayRecordAdmin(admin.ModelAdmin):
    list_display = [
        "group_name", "name", "birth_day", "is_lunar_calendar", "group_name"
    ]
    search_fields = "name", "type",
    list_per_page = 20
    ordering = ('-id',)

    def custom_name(self, obj):
        return obj.name[:20]

    custom_name.short_description = "Name"

    def lastest_inspect_info_url(self, obj):
        last_inspect_info = obj.last_inspect_info
        link_text = "Latest Inspect Info Record"
        if last_inspect_info:
            change_url = reverse('admin:cloud_cloudinspectrecord_change', args=(last_inspect_info.id,))
            html = format_html("<a href='{url}'>{link_text}</a>", link_text=link_text,url=change_url)
            return html
        return link_text

    lastest_inspect_info_url.short_description = "Latest Record"


class CloudInspectInfoAdmin(admin.ModelAdmin):
    list_display = "pod_num", "node_num", "cpu_lim_avg", "cpu_usage_avg", "mem_lim_avg", "mem_req_avg", "mem_usage_avg", "cloud", "created_by"
    list_filter = list_display
    ordering = ('-id',)


class CloudDeployStrategyAdmin(admin.ModelAdmin):
    list_display = "name", "status", "get_format_str"
    list_filter = "name", "status"
    ordering = "-id",


admin.site.register(models.Cloud, CloudAdmin)
admin.site.register(models.CloudInspectRecord, CloudInspectInfoAdmin)
admin.site.register(models.CloudDeployStrategy, CloudDeployStrategyAdmin)
