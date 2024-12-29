from rest_framework import serializers

from common.serializers import BaseModelSerializer
from divisions.serializers import DivisionReadOnlySerializer
from seasons.serializers import SeasonReadOnlySerializer
from .models import Team, TeamSeasonRegistration


TEAM_FIELDS = ('name', 'logo', 'jersey_colors', 'short_name',)


class NestedTeamReadOnlySerializer(BaseModelSerializer):
    """Circular dependency issue hence us re-defining this"""

    class Meta(BaseModelSerializer.Meta):
        model = Team
        fields = BaseModelSerializer.Meta.fields + TEAM_FIELDS


class TeamSeasonRegistrationReadOnlySerializer(BaseModelSerializer):
    team = NestedTeamReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    division = DivisionReadOnlySerializer()
    place = serializers.SerializerMethodField()

    def get_place(self, obj):
        # This attribute is added via an annotation
        return getattr(obj, 'place', None)

    class Meta(BaseModelSerializer.Meta):
        model = TeamSeasonRegistration
        fields = BaseModelSerializer.Meta.fields + (*TeamSeasonRegistration.FIELDS, 'place')


class TeamReadOnlySerializer(BaseModelSerializer):
    seasons = TeamSeasonRegistrationReadOnlySerializer(many=True, source='team_season_registrations', exclude=('team',))

    class Meta(BaseModelSerializer.Meta):
        model = Team
        fields = BaseModelSerializer.Meta.fields + (*TEAM_FIELDS, 'seasons',)
