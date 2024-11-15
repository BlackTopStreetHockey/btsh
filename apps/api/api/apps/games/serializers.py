from common.models import BASE_MODEL_FIELDS
from common.serializers import BaseReadOnlyModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.serializers import TeamReadOnlySerializer
from users.serializers import UserReadOnlySerializer
from .models import Game, GameDay, GamePlayer, GameReferee


class GameDayReadOnlySerializer(BaseReadOnlyModelSerializer):
    season = SeasonReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('day', 'season')


class GameReadOnlySerializer(BaseReadOnlyModelSerializer):
    game_day = GameDayReadOnlySerializer()
    home_team = TeamReadOnlySerializer()
    away_team = TeamReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Game
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'get_court_display',
            'type', 'get_type_display',
        )


class GameDayGameReadOnlySerializer(BaseReadOnlyModelSerializer):
    home_team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)
    away_team = TeamReadOnlySerializer(exclude=BASE_MODEL_FIELDS)

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Game
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'get_court_display', 'type',
            'get_type_display',
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
