from django_filters import rest_framework as filters

from .models import GameDay


class GameDayFilterSet(filters.FilterSet):
    day = filters.DateFromToRangeFilter()

    class Meta:
        model = GameDay
        fields = ('day', 'season', 'opening_team', 'closing_team')
