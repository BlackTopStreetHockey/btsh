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
