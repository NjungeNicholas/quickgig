from django.contrib import admin
from .models import BaseUser, TaskerProfile

@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_client', 'is_tasker', 'is_active', 'is_staff')
    search_fields = ('email', 'username')

@admin.register(TaskerProfile)
class TaskerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'bio', 'get_skills', 'id')
    search_fields = ('user__email', 'user__username', 'bio')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = 'Skills'