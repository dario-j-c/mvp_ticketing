from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_se_team",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("is_se_team",)}),
    )


admin.site.register(User, CustomUserAdmin)
