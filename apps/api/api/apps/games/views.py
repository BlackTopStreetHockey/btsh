from common.views import BaseModelReadOnlyViewSet
from .filtersets import GameDayFilterSet, GameFilterSet, GamePlayerFilterSet, GameRefereeFilterSet
from .models import Game, GameDay, GamePlayer, GameReferee
from .serializers import (
    GameDayWithGamesReadOnlySerializer,
    GamePlayerReadOnlySerializer,
    GameReadOnlySerializer,
    GameRefereeReadOnlySerializer
)


class GameDayViewSet(BaseModelReadOnlyViewSet):
    queryset = GameDay.objects.all().select_related(
        'opening_team__created_by',
        'opening_team__updated_by',
        'closing_team__created_by',
        'closing_team__updated_by',
        'season__created_by',
        'season__updated_by',
    ).prefetch_related('games', 'games__home_team', 'games__away_team')
    serializer_class = GameDayWithGamesReadOnlySerializer
    ordering = ('day',)
    ordering_fields = ('day', 'season',)
    filterset_class = GameDayFilterSet


class GameViewSet(BaseModelReadOnlyViewSet):
    queryset = Game.objects.all().select_related(
        'game_day__opening_team__created_by',
        'game_day__opening_team__updated_by',
        'game_day__closing_team__created_by',
        'game_day__closing_team__updated_by',
        'game_day__season__created_by',
        'game_day__season__updated_by',
        'game_day__created_by',
        'game_day__updated_by',
        'home_team__created_by',
        'home_team__updated_by',
        'away_team__created_by',
        'away_team__updated_by',
    )
    serializer_class = GameReadOnlySerializer
    ordering = ('-game_day__day', 'start')
    ordering_fields = ('game_day__day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court')
    search_fields = ('home_team__name', 'away_team__name', 'location', 'court')
    filterset_class = GameFilterSet


class GameRefereeViewSet(BaseModelReadOnlyViewSet):
    queryset = GameReferee.objects.all().select_related('user')
    serializer_class = GameRefereeReadOnlySerializer
    ordering = ('-game__game_day__day', 'game__start', 'user__email')
    ordering_fields = ('game', 'type',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',)
    filterset_class = GameRefereeFilterSet


class GamePlayerViewSet(BaseModelReadOnlyViewSet):
    queryset = GamePlayer.objects.all().select_related('user', 'team')
    serializer_class = GamePlayerReadOnlySerializer
    ordering = ('-game__game_day__day', 'game__start', 'user__email', 'team')
    ordering_fields = ('game', 'team', 'is_substitute', 'is_goalie')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'team__name',)
    filterset_class = GamePlayerFilterSet
