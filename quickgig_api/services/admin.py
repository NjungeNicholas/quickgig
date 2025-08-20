from django.contrib import admin
from .models import Category, Service

# Customize the admin interface
admin.site.site_header = "QuickGig Admin"
admin.site.index_title = "Welcome to the QuickGig Admin Portal"

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'id')
    search_fields = ('name', 'description')
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
