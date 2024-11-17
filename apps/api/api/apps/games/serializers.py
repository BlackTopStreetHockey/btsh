from rest_framework import serializers

from common.models import BASE_MODEL_FIELDS
from common.serializers import BaseReadOnlyModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.models import Team
from teams.serializers import TeamReadOnlySerializer
from users.serializers import UserReadOnlySerializer
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee


class GameDayReadOnlySerializer(BaseReadOnlyModelSerializer):
    season = SeasonReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('day', 'season')


class GameReadOnlySerializer(BaseReadOnlyModelSerializer):
    game_day = GameDayReadOnlySerializer()
    home_team = TeamReadOnlySerializer()
    away_team = TeamReadOnlySerializer()

    home_team_num_goals = serializers.IntegerField()
    away_team_num_goals = serializers.IntegerField()
    winning_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    losing_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Game
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'get_court_display',
            'type', 'get_type_display', 'home_team_num_goals', 'away_team_num_goals', 'winning_team_id',
            'losing_team_id',
        )


class GameDayGameReadOnlySerializer(BaseReadOnlyModelSerializer):
    home_team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)
    away_team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)

    home_team_num_goals = serializers.IntegerField()
    away_team_num_goals = serializers.IntegerField()
    winning_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    losing_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Game
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'get_court_display', 'type',
            'get_type_display', 'home_team_num_goals', 'away_team_num_goals', 'winning_team_id',
            'losing_team_id',
        )


class GameDayWithGamesReadOnlySerializer(BaseReadOnlyModelSerializer):
    opening_team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)
    closing_team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)
    season = SeasonReadOnlySerializer(exclude=BASE_MODEL_FIELDS)
    games = GameDayGameReadOnlySerializer(many=True, exclude=BASE_MODEL_FIELDS)

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('day', 'season', 'opening_team', 'closing_team', 'games')


class GameRefereeReadOnlySerializer(BaseReadOnlyModelSerializer):
    user = UserReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameReferee
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('game', 'user', 'type', 'get_type_display',)


class GamePlayerReadOnlySerializer(BaseReadOnlyModelSerializer):
    user = UserReadOnlySerializer()
    team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GamePlayer
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('game', 'user', 'team', 'is_substitute', 'is_goalie')


class GameGoalReadOnlySerializer(BaseReadOnlyModelSerializer):
    team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)
    scored_by = GamePlayerReadOnlySerializer(exclude=(*BASE_MODEL_FIELDS, 'team',))
    assisted_by1 = GamePlayerReadOnlySerializer(exclude=(*BASE_MODEL_FIELDS, 'team',))
    assisted_by2 = GamePlayerReadOnlySerializer(exclude=(*BASE_MODEL_FIELDS, 'team',))

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameGoal
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'game', 'team', 'period', 'get_period_display', 'scored_by', 'assisted_by1', 'assisted_by2',
        )
