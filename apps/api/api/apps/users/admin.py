from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from .models import User, UserSeasonRegistration


class UserSeasonRegistrationInline(BaseModelTabularInline):
    model = UserSeasonRegistration
    fk_name = 'user'
    autocomplete_fields = ('season', 'team',)
    ordering = ('season', 'team')
    fields = ('season', 'team', 'is_captain', 'position', 'registered_at', 'signature', 'location')


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
    inlines = [UserSeasonRegistrationInline]

    def get_fieldsets(self, request, obj=None):
        fieldsets = deepcopy(super().get_fieldsets(request, obj))
        if obj:
            personal_info_fields = fieldsets[1][1]['fields']
            fieldsets[1][1]['fields'] = (*personal_info_fields, 'gender',)
        return fieldsets


@admin.register(UserSeasonRegistration)
class UserSeasonRegistrationAdmin(BaseModelAdmin):
    list_display = (
        'user', 'season', 'team', 'is_captain', 'position', 'registered_at', 'signature', 'location',
    )
    list_filter = ('season', 'team', 'is_captain', 'position', 'location')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'season', 'team__name')
    ordering = ('season', 'team', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('user', 'season', 'team',)
