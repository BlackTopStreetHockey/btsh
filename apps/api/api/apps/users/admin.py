from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id',) + BaseUserAdmin.list_display + ('is_superuser', 'date_joined', 'last_login')
    list_filter = BaseUserAdmin.list_filter + ('date_joined', 'last_login',)
    search_fields = ('id',) + BaseUserAdmin.search_fields
    date_hierarchy = 'date_joined'
