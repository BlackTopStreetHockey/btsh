from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    AdminUserCreationForm as BaseAdminUserCreationForm,
    UserChangeForm as BaseUserChangeForm
)
from import_export.admin import ExportActionMixin, ImportExportMixin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from .models import User, UserSeasonRegistration
from .resources import UserResource, UserSeasonRegistrationResource


class UserSeasonRegistrationInline(BaseModelTabularInline):
    model = UserSeasonRegistration
    fk_name = 'user'
    autocomplete_fields = ('season', 'team',)
    ordering = ('season', 'team')
    fields = ('season', 'team', 'is_captain', 'position', 'registered_at', 'signature', 'location')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'season', 'team')


BASIC_INFO_FIELDSET_FIELDS = ('username', 'first_name', 'last_name', 'email', 'gender')
BASIC_INFO_ADD_USER_FIELDSET = ('Basic Info', {
    'fields': (*BASIC_INFO_FIELDSET_FIELDS, 'usable_password', 'password1', 'password2',)
})
BASIC_INFO_CHANGE_USER_FIELDSET = ('Basic Info', {
    'fields': (*BASIC_INFO_FIELDSET_FIELDS, 'password',)
})
PERMISSIONS_FIELDSET = ('Permissions', {
    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
})
DATES_FIELDSET = ('Dates', {'fields': ('last_login', 'date_joined')})


class AdminUserCreationForm(BaseAdminUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Please enter an email address, if not available use a unique username.'
        self.fields['email'].help_text = (
            'If username is an email address use the same value here, otherwise leave blank.'
        )
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        # Copied from UserChangeForm since user creation is one step and user permissions are being displayed
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')



class UserChangeForm(BaseUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Please enter an email address, if not available use a unique username.'
        self.fields['email'].help_text = (
            'If username is an email address use the same value here, otherwise leave blank.'
        )
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


@admin.register(User)
class UserAdmin(ImportExportMixin, ExportActionMixin, BaseUserAdmin):
    add_form_template = 'users/admin/add_form.html'
    fieldsets = [BASIC_INFO_CHANGE_USER_FIELDSET, PERMISSIONS_FIELDSET, DATES_FIELDSET]
    add_fieldsets = [BASIC_INFO_ADD_USER_FIELDSET, PERMISSIONS_FIELDSET, DATES_FIELDSET]
    form = UserChangeForm
    add_form = AdminUserCreationForm

    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'gender', 'date_joined', 'last_login', 'is_staff',
        'is_superuser',
    )
    list_filter = ('gender', 'date_joined', 'last_login',) + BaseUserAdmin.list_filter
    search_fields = ('id',) + BaseUserAdmin.search_fields
    date_hierarchy = 'date_joined'
    ordering = ('first_name', 'last_name')
    inlines = [UserSeasonRegistrationInline]

    resource_classes = [UserResource]


@admin.register(UserSeasonRegistration)
class UserSeasonRegistrationAdmin(BaseModelAdmin):
    list_display = (
        'user', 'season', 'team', 'is_captain', 'position', 'registered_at', 'signature', 'location',
    )
    list_filter = (
        'season', 'team', 'is_captain', 'position', 'location', 'interested_in_reffing',
        'interested_in_opening_closing', 'interested_in_next_year',
    )
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'team__name')
    ordering = ('season', 'team', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('user', 'season', 'team',)

    import_resource_classes = [UserSeasonRegistrationResource]
    export_resource_classes = [UserSeasonRegistrationResource]
