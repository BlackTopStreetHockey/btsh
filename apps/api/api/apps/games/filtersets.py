from django_filters import rest_framework as filters

from .models import Game, GameDay


class GameDayFilterSet(filters.FilterSet):
    day = filters.DateFromToRangeFilter()

    class Meta:
        model = GameDay
        fields = ('day', 'season', 'opening_team', 'closing_team')


class GameFilterSet(filters.FilterSet):
    start = filters.TimeRangeFilter()
    end = filters.TimeRangeFilter()

    class Meta:
        model = Game
        fields = (
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court'
        )
