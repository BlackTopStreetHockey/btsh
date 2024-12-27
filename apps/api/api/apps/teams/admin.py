from django.contrib import admin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from common.resources import BaseModelResource, DivisionNameField, SeasonYearField, TeamShortNameField
from games.models import Game
from .models import Team, TeamSeasonRegistration
from .utils import calculate_team_season_registration_stats


class TeamResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        model = Team
        fields = BaseModelResource.Meta.fields + ('name', 'short_name', 'logo', 'jersey_colors')


class TeamSeasonRegistrationResource(BaseModelResource):
    season_year = SeasonYearField()
    team_short_name = TeamShortNameField()
    division_name = DivisionNameField()

    def import_data(self, *args, **kwargs):
        dry_run = kwargs.get('dry_run')
        result = super().import_data(*args, **kwargs)
        if not dry_run:
            calculate_team_season_registration_stats(game_type=Game.REGULAR)
        return result

    class Meta(BaseModelResource.Meta):
        model = TeamSeasonRegistration
        fields = BaseModelResource.Meta.fields + ('season_year', 'team_short_name', 'division_name',)


class TeamSeasonRegistrationInline(BaseModelTabularInline):
    model = TeamSeasonRegistration
    fields = ('season', 'division',)
    autocomplete_fields = ('season', 'team', 'division',)
    ordering = ('-season__start', 'division', 'team',)


@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    list_display = ('name', 'logo', 'jersey_colors', 'short_name')
    search_fields = ('name', 'short_name')
    ordering = ('name',)
    inlines = [TeamSeasonRegistrationInline]

    import_resource_classes = [TeamResource]
    export_resource_classes = [TeamResource]


@admin.register(TeamSeasonRegistration)
class TeamSeasonRegistration(BaseModelAdmin):
    # It doesn't make sense to include place here because the admin shows records across seasons, we could conditionally
    # include place when the user is filtering by season
    list_display = TeamSeasonRegistration.FIELDS
    list_filter = ('season', 'division', 'team',)
    search_fields = ('team__name',)
    ordering = ('-season__start', 'division', 'team',)
    autocomplete_fields = ('season', 'team', 'division',)
    readonly_fields = TeamSeasonRegistration.BASE_FIELDS

    import_resource_classes = [TeamSeasonRegistrationResource]
    export_resource_classes = [TeamSeasonRegistrationResource]
