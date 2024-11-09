from common.serializers import BaseReadOnlyModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.serializers import TeamReadOnlySerializer
from .models import Game, GameDay




class GameDayGameReadOnlySerializer(BaseReadOnlyModelSerializer):
    season = SeasonReadOnlySerializer()
    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('day', 'season')


class GameReadOnlySerializer(BaseReadOnlyModelSerializer):
    game_day = GameDayGameReadOnlySerializer()
    home_team = TeamReadOnlySerializer()
    away_team = TeamReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Game
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'get_court_display',
        )


class GameDayReadOnlySerializer(BaseReadOnlyModelSerializer):
    opening_team = TeamReadOnlySerializer()
    closing_team = TeamReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    games = GameReadOnlySerializer(many=True)

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('day', 'season', 'opening_team', 'closing_team', 'games')
