from import_export import fields

from common.resources import BaseModelResource, GameDayDayField, SeasonYearField, TeamShortNameField
from .models import Game, GameDay


class GameDayResource(BaseModelResource):
    season_year = SeasonYearField(attribute='season')
    opening_team_short_name = TeamShortNameField(attribute='opening_team', column_name='opening_team_short_name')
    closing_team_short_name = TeamShortNameField(attribute='closing_team', column_name='closing_team_short_name')

    class Meta(BaseModelResource.Meta):
        model = GameDay
        fields = BaseModelResource.Meta.fields + (
            'day', 'season_year', 'opening_team_short_name', 'closing_team_short_name',
        )


class GameResource(BaseModelResource):
    game_day = GameDayDayField(attribute='game_day')
    home_team_short_name = TeamShortNameField(attribute='home_team', column_name='home_team_short_name')
    away_team_short_name = TeamShortNameField(attribute='away_team', column_name='away_team_short_name')

    home_team_display = fields.Field(attribute='home_team_display', column_name='home_team_display', readonly=True)
    away_team_display = fields.Field(attribute='away_team_display', column_name='away_team_display', readonly=True)
    result = fields.Field(attribute='result', column_name='result', readonly=True)

    class Meta(BaseModelResource.Meta):
        model = Game
        fields = BaseModelResource.Meta.fields + (
            'game_day', 'start', 'duration', 'home_team_short_name', 'away_team_short_name', 'location', 'court',
            'type', 'status', 'home_team_display', 'away_team_display', 'result',
        )
