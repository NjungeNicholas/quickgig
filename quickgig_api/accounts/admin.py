from django.contrib import admin
from .models import BaseUser

@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_client', 'is_tasker', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_client', 'is_tasker', 'is_active', 'is_staff')
