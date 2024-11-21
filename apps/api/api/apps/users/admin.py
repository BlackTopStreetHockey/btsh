from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'gender', 'date_joined', 'last_login', 'is_staff',
        'is_superuser',
    )
    list_filter = ('gender', 'date_joined', 'last_login',) + BaseUserAdmin.list_filter
    search_fields = ('id',) + BaseUserAdmin.search_fields
    date_hierarchy = 'date_joined'
    ordering = ('first_name', 'last_name')

    def get_fieldsets(self, request, obj=None):
        fieldsets = deepcopy(super().get_fieldsets(request, obj))
        if obj:
            personal_info_fields = fieldsets[1][1]['fields']
            fieldsets[1][1]['fields'] = (*personal_info_fields, 'gender',)
        return fieldsets
