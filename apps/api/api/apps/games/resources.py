from import_export import fields

from common.resources import (
    BaseModelResource,
    GameDayDayField,
    GamePlayerField, SeasonYearField,
    TeamShortNameField,
    UserUsernameField
)
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee


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


class GameRefereeResource(BaseModelResource):
    username = UserUsernameField(attribute='user')

    class Meta(BaseModelResource.Meta):
        model = GameReferee
        fields = BaseModelResource.Meta.fields + ('game', 'username', 'type')


class GamePlayerResource(BaseModelResource):
    username = UserUsernameField(attribute='user')
    team_short_name = TeamShortNameField(attribute='team')

    class Meta(BaseModelResource.Meta):
        model = GamePlayer
        fields = BaseModelResource.Meta.fields + ('game', 'username', 'team_short_name', 'is_substitute', 'is_goalie')


class GameGoalExportResource(BaseModelResource):
    team_short_name = TeamShortNameField(attribute='team')
    team_against_short_name = TeamShortNameField(attribute='team_against', column_name='team_against_short_name')
    scored_by_username = UserUsernameField(attribute='scored_by__user', column_name='scored_by_username')
    assisted_by1_username = UserUsernameField(attribute='assisted_by1__user', column_name='assisted_by1_username')
    assisted_by2_username = UserUsernameField(attribute='assisted_by2__user', column_name='assisted_by2_username')

    class Meta(BaseModelResource.Meta):
        model = GameGoal
        fields = BaseModelResource.Meta.fields + (
            'game', 'team_short_name', 'team_against_short_name', 'period', 'scored_by_username',
            'assisted_by1_username', 'assisted_by2_username',
        )


class GameGoalImportResource(BaseModelResource):
    team_short_name = TeamShortNameField(attribute='team')
    team_against_short_name = TeamShortNameField(attribute='team_against', column_name='team_against_short_name')
    scored_by_username = GamePlayerField(
        attribute='scored_by',
        column_name='scored_by_username',
        game_column_name='game',
        team_column_name='team_short_name',
    )
    assisted_by1_username = GamePlayerField(
        attribute='assisted_by1',
        column_name='assisted_by1_username',
        game_column_name='game',
        team_column_name='team_short_name',
    )
    assisted_by2_username = GamePlayerField(
        attribute='assisted_by2',
        column_name='assisted_by2_username',
        game_column_name='game',
        team_column_name='team_short_name',
    )

    class Meta(BaseModelResource.Meta):
        model = GameGoal
        fields = BaseModelResource.Meta.fields + (
            'game', 'team_short_name', 'team_against_short_name', 'period', 'scored_by_username',
            'assisted_by1_username', 'assisted_by2_username',
        )
