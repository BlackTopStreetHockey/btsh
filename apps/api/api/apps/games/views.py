from common.views import BaseModelReadOnlyViewSet
from .filtersets import GameDayFilterSet, GameFilterSet
from .models import Game, GameDay
from .serializers import GameDayReadOnlySerializer, GameReadOnlySerializer
from django.db.models import Prefetch


class GameDayViewSet(BaseModelReadOnlyViewSet):
    queryset = GameDay.objects.all().select_related(
        'opening_team__created_by',
        'opening_team__updated_by',
        'closing_team__created_by',
        'closing_team__updated_by',
        'season__created_by',
        'season__updated_by',
    ).prefetch_related('games')
    serializer_class = GameDayReadOnlySerializer
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
