from common.views import BaseModelReadOnlyViewSet
from .filtersets import TeamFilterSet
from .models import Team, TeamSeasonRegistration
from .serializers import TeamReadOnlySerializer, TeamSeasonRegistrationReadOnlySerializer


class TeamViewSet(BaseModelReadOnlyViewSet):
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


class TeamSeasonRegistrationViewSet(BaseModelReadOnlyViewSet):
    queryset = TeamSeasonRegistration.objects.all().select_related('team', 'season', 'division')
    serializer_class = TeamSeasonRegistrationReadOnlySerializer
    ordering = ('-season__start', 'division', 'team',)
    ordering_fields = TeamSeasonRegistration.FIELDS
    search_fields = ('division__name', 'team__name',)
    filterset_fields = TeamSeasonRegistration.FIELDS
