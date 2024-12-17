from rest_framework import serializers

from common.serializers import BaseReadOnlyModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.models import Team
from teams.serializers import TeamReadOnlySerializer
from users.serializers import UserReadOnlySerializer
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee


GAME_DAY_FIELDS = ('day', 'season', 'opening_team', 'closing_team',)


class NestedGameDayReadOnlySerializer(BaseReadOnlyModelSerializer):
    """Circular dependency issue hence us re-defining this"""
    opening_team = TeamReadOnlySerializer(exclude=('seasons',))
    closing_team = TeamReadOnlySerializer(exclude=('seasons',))
    season = SeasonReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + GAME_DAY_FIELDS


class GameReadOnlySerializer(BaseReadOnlyModelSerializer):
    game_day = NestedGameDayReadOnlySerializer()
    home_team = TeamReadOnlySerializer(exclude=('seasons',))
    away_team = TeamReadOnlySerializer(exclude=('seasons',))

    home_team_num_goals = serializers.IntegerField()
    away_team_num_goals = serializers.IntegerField()
    winning_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    losing_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    result = serializers.CharField()
    get_result_display = serializers.CharField()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Game
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team',
            'location', 'court', 'get_court_display', 'type', 'get_type_display', 'home_team_num_goals',
            'away_team_num_goals', 'winning_team_id', 'losing_team_id', 'status', 'get_status_display',
            'home_team_display', 'away_team_display', 'result', 'get_result_display',
        )


class GameDayReadOnlySerializer(BaseReadOnlyModelSerializer):
    opening_team = TeamReadOnlySerializer(exclude=('seasons',))
    closing_team = TeamReadOnlySerializer(exclude=('seasons',))
    season = SeasonReadOnlySerializer()
    games = GameReadOnlySerializer(many=True, exclude=('game_day',))

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + (*GAME_DAY_FIELDS, 'games')


class GameRefereeReadOnlySerializer(BaseReadOnlyModelSerializer):
    user = UserReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameReferee
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('game', 'user', 'type', 'get_type_display',)


class GamePlayerReadOnlySerializer(BaseReadOnlyModelSerializer):
    user = UserReadOnlySerializer()
    team = TeamReadOnlySerializer(exclude=('seasons',))

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GamePlayer
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('game', 'user', 'team', 'is_substitute', 'is_goalie')


class GameGoalReadOnlySerializer(BaseReadOnlyModelSerializer):
    team = TeamReadOnlySerializer(exclude=('seasons',))
    scored_by = GamePlayerReadOnlySerializer(exclude=('team',))
    assisted_by1 = GamePlayerReadOnlySerializer(exclude=('team',))
    assisted_by2 = GamePlayerReadOnlySerializer(exclude=('team',))

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameGoal
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'game', 'team', 'period', 'get_period_display', 'scored_by', 'assisted_by1', 'assisted_by2',
        )
