from django_filters import rest_framework as filters

from .models import Game, GameDay, GamePlayer, GameReferee


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
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'game_day__season'
        )


class GameRefereeFilterSet(filters.FilterSet):
    game = filters.ModelChoiceFilter(queryset=Game.objects.all().select_related('game_day', 'home_team', 'away_team'))

    class Meta:
        model = GameReferee
        fields = ('game', 'type',)


class GamePlayerFilterSet(filters.FilterSet):
    game = filters.ModelChoiceFilter(queryset=Game.objects.all().select_related('game_day', 'home_team', 'away_team'))

    class Meta:
        model = GamePlayer
        fields = ('game', 'team', 'is_substitute', 'is_goalie',)
