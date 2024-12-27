from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ExportActionMixin, ImportExportMixin
from import_export.fields import Field

from common.admin import BaseModelAdmin, BaseModelTabularInline
from common.resources import (
    BaseModelResource,
    EmailWidget,
    SeasonYearField,
    TeamShortNameField,
    UserUsernameField,
)
from .models import User, UserSeasonRegistration


class UserResource(BaseModelResource):
    username = Field(attribute='username', column_name='username', widget=EmailWidget())

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.set_unusable_password()
        return super().after_init_instance(instance, new, row, **kwargs)

    def before_save_instance(self, instance, row, **kwargs):
        username = row.get('username')
        instance.email = username
        return super().before_save_instance(instance, row, **kwargs)

    class Meta(BaseModelResource.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender',)
        import_id_fields = ('username',)


class UserSeasonRegistrationResource(BaseModelResource):
    username = UserUsernameField()
    season_year = SeasonYearField()
    team_short_name = TeamShortNameField()

    class Meta(BaseModelResource.Meta):
        model = UserSeasonRegistration
        fields = BaseModelResource.Meta.fields + (
            'username', 'season_year', 'team_short_name', 'is_captain', 'position', 'registered_at', 'signature',
            'location', 'interested_in_reffing', 'interested_in_opening_closing', 'interested_in_other',
            'interested_in_next_year', 'mid_season_party_ideas',
        )


class UserSeasonRegistrationInline(BaseModelTabularInline):
    model = UserSeasonRegistration
    fk_name = 'user'
    autocomplete_fields = ('season', 'team',)
    ordering = ('season', 'team')
    fields = ('season', 'team', 'is_captain', 'position', 'registered_at', 'signature', 'location')


@admin.register(User)
class UserAdmin(ImportExportMixin, ExportActionMixin, BaseUserAdmin):
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
    list_filter = (
        'season', 'team', 'is_captain', 'position', 'location', 'interested_in_reffing',
        'interested_in_opening_closing', 'interested_in_next_year',
    )
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'team__name')
    ordering = ('season', 'team', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('user', 'season', 'team',)

    import_resource_classes = [UserSeasonRegistrationResource]
    export_resource_classes = [UserSeasonRegistrationResource]
