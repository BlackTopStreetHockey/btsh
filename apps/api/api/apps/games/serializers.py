from common.serializers import BaseReadOnlyModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.serializers import TeamReadOnlySerializer
from .models import GameDay


class GameDayReadOnlySerializer(BaseReadOnlyModelSerializer):
    opening_team = TeamReadOnlySerializer()
    closing_team = TeamReadOnlySerializer()
    season = SeasonReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = GameDay
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('day', 'season', 'opening_team', 'closing_team')
