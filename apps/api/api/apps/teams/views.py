from common.views import BaseModelViewSet
from .filtersets import TeamFilterSet, TeamSeasonRegistrationFilterSet
from .models import Team, TeamSeasonRegistration
from .serializers import TeamReadOnlySerializer, TeamSeasonRegistrationReadOnlySerializer


class TeamViewSet(BaseModelViewSet):
    queryset = Team.objects.all().prefetch_related(
        'team_season_registrations__season',
        'team_season_registrations__division',
    )
    lookup_field = 'short_name'
    serializer_class = TeamReadOnlySerializer
    ordering = ('name',)
    ordering_fields = ('name', 'short_name')
    search_fields = ('name', 'short_name')
    filterset_class = TeamFilterSet


class TeamSeasonRegistrationViewSet(BaseModelViewSet):
    queryset = TeamSeasonRegistration.objects.with_place_by_season().select_related('team', 'season', 'division')
    serializer_class = TeamSeasonRegistrationReadOnlySerializer
    ordering = ('-season__start', 'place',)
    ordering_fields = (
        'team', 'season', 'division',
        'points', 'wins', 'losses', 'ties',
        'overtime_losses', 'shootout_losses',
        'games_played',
        'goals_for', 'goals_against', 'goal_differential',
        'place',
    )
    search_fields = ('division__name', 'team__name',)
    filterset_class = TeamSeasonRegistrationFilterSet
