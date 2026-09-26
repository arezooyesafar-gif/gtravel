from django.contrib import admin

from .models import ChangeLog, StaffAccess


@admin.register(StaffAccess)
class StaffAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'permissions', 'updated_at']
    search_fields = ['user__username']


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'username', 'action', 'area', 'title']
    list_filter = ['action', 'area']
    search_fields = ['title', 'username']
