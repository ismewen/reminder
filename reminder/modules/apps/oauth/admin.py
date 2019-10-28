from django.contrib import admin

# Register your models here.
from modules.apps.oauth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username", "open_id","status"
    ]
    search_fields = "username", "status",
    list_per_page = 20
    ordering = ('-id',)


admin.site.register(User, UserAdmin)