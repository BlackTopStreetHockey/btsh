from django.db.models import Prefetch

from common.views import BaseModelReadOnlyViewSet
from .filtersets import GameDayFilterSet, GameFilterSet, GameGoalFilterSet, GamePlayerFilterSet, GameRefereeFilterSet
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee
from .serializers import (
    GameDayReadOnlySerializer,
    GameGoalReadOnlySerializer,
    GamePlayerReadOnlySerializer,
    GameReadOnlySerializer,
    GameRefereeReadOnlySerializer
)


class GameDayViewSet(BaseModelReadOnlyViewSet):
    queryset = GameDay.objects.all().select_related(
        'opening_team', 'closing_team', 'season'
    ).prefetch_related(
        Prefetch('games', queryset=Game.objects.select_related('home_team', 'away_team').with_scores()),
    )
    serializer_class = GameDayReadOnlySerializer
    ordering = ('day',)
    ordering_fields = ('day', 'season',)
    filterset_class = GameDayFilterSet


class GameViewSet(BaseModelReadOnlyViewSet):
    queryset = Game.objects.with_scores().select_related('home_team', 'away_team')
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


class GameGoalViewSet(BaseModelReadOnlyViewSet):
    queryset = GameGoal.objects.all().select_related(
        'team',
        'scored_by__user',
        'scored_by__team',
        'assisted_by1__user',
        'assisted_by1__team',
        'assisted_by2__user',
        'assisted_by2__team',
    )
    serializer_class = GameGoalReadOnlySerializer
    ordering = ('-game__game_day__day', 'game__start', 'scored_by__user__email', 'team')
    ordering_fields = ('game', 'team', 'period',)
    search_fields = ('team__name',)
    filterset_class = GameGoalFilterSet
