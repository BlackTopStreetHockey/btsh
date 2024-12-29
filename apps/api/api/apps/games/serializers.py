from rest_framework import serializers

from common.serializers import BaseModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.models import Team
from teams.serializers import NestedTeamReadOnlySerializer
from users.serializers import UserReadOnlySerializer
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee


GAME_DAY_FIELDS = ('day', 'season', 'opening_team', 'closing_team',)


class NestedGameDayReadOnlySerializer(BaseModelSerializer):
    """Circular dependency issue hence us re-defining this"""
    opening_team = NestedTeamReadOnlySerializer()
    closing_team = NestedTeamReadOnlySerializer()
    season = SeasonReadOnlySerializer()

    class Meta(BaseModelSerializer.Meta):
        model = GameDay
        fields = BaseModelSerializer.Meta.fields + GAME_DAY_FIELDS


class GameReadOnlySerializer(BaseModelSerializer):
    game_day = NestedGameDayReadOnlySerializer()

    home_team = NestedTeamReadOnlySerializer()
    home_team_division_name = serializers.CharField()
    home_team_num_goals = serializers.IntegerField()

    away_team = NestedTeamReadOnlySerializer()
    away_team_division_name = serializers.CharField()
    away_team_num_goals = serializers.IntegerField()

    winning_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    losing_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    result = serializers.CharField()
    get_result_display = serializers.CharField()

    class Meta(BaseModelSerializer.Meta):
        model = Game
        fields = BaseModelSerializer.Meta.fields + (
            'game_day', 'start', 'duration', 'end', 'home_team', 'home_team_division_name', 'home_team_num_goals',
            'home_team_display', 'away_team', 'away_team_division_name', 'away_team_num_goals', 'away_team_display',
            'location', 'court', 'get_court_display', 'type', 'get_type_display', 'winning_team_id', 'losing_team_id',
            'status', 'get_status_display', 'result', 'get_result_display',
        )


class GameDayReadOnlySerializer(BaseModelSerializer):
    opening_team = NestedTeamReadOnlySerializer()
    closing_team = NestedTeamReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    games = GameReadOnlySerializer(many=True, exclude=('game_day',))

    class Meta(BaseModelSerializer.Meta):
        model = GameDay
        fields = BaseModelSerializer.Meta.fields + (*GAME_DAY_FIELDS, 'games')


class GameRefereeReadOnlySerializer(BaseModelSerializer):
    user = UserReadOnlySerializer()

    class Meta(BaseModelSerializer.Meta):
        model = GameReferee
        fields = BaseModelSerializer.Meta.fields + ('game', 'user', 'type', 'get_type_display',)


class GamePlayerReadOnlySerializer(BaseModelSerializer):
    user = UserReadOnlySerializer()
    team = NestedTeamReadOnlySerializer()

    class Meta(BaseModelSerializer.Meta):
        model = GamePlayer
        fields = BaseModelSerializer.Meta.fields + ('game', 'user', 'team', 'is_substitute', 'is_goalie')


class GameGoalReadOnlySerializer(BaseModelSerializer):
    team = NestedTeamReadOnlySerializer()
    team_against = NestedTeamReadOnlySerializer()
    scored_by = GamePlayerReadOnlySerializer(exclude=('team',))
    assisted_by1 = GamePlayerReadOnlySerializer(exclude=('team',))
    assisted_by2 = GamePlayerReadOnlySerializer(exclude=('team',))

    class Meta(BaseModelSerializer.Meta):
        model = GameGoal
        fields = BaseModelSerializer.Meta.fields + (
            'game', 'team', 'team_against', 'period', 'get_period_display', 'scored_by', 'assisted_by1', 'assisted_by2',
        )
