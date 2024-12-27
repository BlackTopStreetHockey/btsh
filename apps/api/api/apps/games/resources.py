from common.resources import BaseModelResource, SeasonYearField, TeamShortNameField

from .models import GameDay


class GameDayResource(BaseModelResource):
    season_year = SeasonYearField(attribute='season')
    opening_team_short_name = TeamShortNameField(attribute='opening_team', column_name='opening_team_short_name')
    closing_team_short_name = TeamShortNameField(attribute='closing_team', column_name='closing_team_short_name')

    class Meta:
        model = GameDay
        fields = BaseModelResource.Meta.fields + (
            'day', 'season_year', 'opening_team_short_name', 'closing_team_short_name',
        )
