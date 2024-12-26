from common.views import BaseModelReadOnlyViewSet
from games.models import Game
from .filtersets import UserSeasonRegistrationFilterSet
from .models import UserSeasonRegistration
from .serializers import UserSeasonRegistrationReadOnlySerializer


class UserSeasonRegistrationViewSet(BaseModelReadOnlyViewSet):
    queryset = UserSeasonRegistration.objects.with_place_by_team_and_season(game_type=Game.REGULAR).select_related(
        'user',
        'season',
        'team',
    )
    serializer_class = UserSeasonRegistrationReadOnlySerializer
    ordering = ('-season__start', 'place')
    ordering_fields = ('season', 'team', 'place')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'team__name',)
    filterset_class = UserSeasonRegistrationFilterSet
