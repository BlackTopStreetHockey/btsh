from common.serializers import BaseReadOnlyModelSerializer
from divisions.serializers import DivisionReadOnlySerializer
from seasons.serializers import SeasonReadOnlySerializer
from .models import Team, TeamSeasonRegistration


TEAM_FIELDS = ('name', 'logo', 'jersey_colors', 'short_name',)


class NestedTeamReadOnlySerializer(BaseReadOnlyModelSerializer):
    """Circular dependency issue hence us re-defining this"""

    class Meta:
        model = Team
        fields = BaseReadOnlyModelSerializer.Meta.fields + TEAM_FIELDS


class TeamSeasonRegistrationReadOnlySerializer(BaseReadOnlyModelSerializer):
    team = NestedTeamReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    division = DivisionReadOnlySerializer()

    class Meta:
        model = TeamSeasonRegistration
        fields = ('team', 'season', 'division', 'home_games_played', 'away_games_played', 'games_played')


class TeamReadOnlySerializer(BaseReadOnlyModelSerializer):
    seasons = TeamSeasonRegistrationReadOnlySerializer(many=True, source='team_season_registrations', exclude=('team',))

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Team
        fields = BaseReadOnlyModelSerializer.Meta.fields + (*TEAM_FIELDS, 'seasons',)
