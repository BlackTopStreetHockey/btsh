from import_export import fields

from common.resources import BaseModelResource, EmailWidget, SeasonYearField, TeamShortNameField, UserUsernameField
from .models import User, UserSeasonRegistration


class UserResource(BaseModelResource):
    username = fields.Field(attribute='username', column_name='username', widget=EmailWidget())

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
    username = UserUsernameField(attribute='user')
    season_year = SeasonYearField(attribute='season')
    team_short_name = TeamShortNameField(attribute='team')

    class Meta(BaseModelResource.Meta):
        model = UserSeasonRegistration
        fields = BaseModelResource.Meta.fields + (
            'username', 'season_year', 'team_short_name', 'is_captain', 'position', 'registered_at', 'signature',
            'location', 'interested_in_reffing', 'interested_in_opening_closing', 'interested_in_other',
            'interested_in_next_year', 'mid_season_party_ideas',
        )
