from common.views import BaseModelReadOnlyViewSet
from .filtersets import GameDayFilterSet
from .models import GameDay
from .serializers import GameDayReadOnlySerializer


class GameDayViewSet(BaseModelReadOnlyViewSet):
    queryset = GameDay.objects.all().select_related(
        'opening_team__created_by',
        'opening_team__updated_by',
        'closing_team__created_by',
        'closing_team__updated_by',
        'season__created_by',
        'season__updated_by',
    )
    serializer_class = GameDayReadOnlySerializer
    ordering = ('day',)
    ordering_fields = ('day', 'season',)
    filterset_class = GameDayFilterSet
