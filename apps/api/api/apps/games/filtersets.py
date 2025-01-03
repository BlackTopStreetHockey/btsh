from django_filters import rest_framework as filters

from teams.models import Team
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee, GameResultsEnum


class GameDayFilterSet(filters.FilterSet):
    day = filters.DateFromToRangeFilter()

    class Meta:
        model = GameDay
        fields = ('day', 'season', 'opening_team', 'closing_team')


class GameFilterSet(filters.FilterSet):
    start = filters.TimeRangeFilter()
    end = filters.TimeRangeFilter()
    result = filters.ChoiceFilter(label='Result', choices=GameResultsEnum)
    team = filters.ModelChoiceFilter(label='Team', queryset=Team.objects.all(), method='filter_team')

    def filter_team(self, queryset, name, value):
        return queryset.for_team(value) if value else queryset

    class Meta:
        model = Game
        fields = (
            'game_day', 'start', 'duration', 'end', 'home_team', 'away_team', 'location', 'court', 'game_day__season',
            'status', 'result',
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


class GameGoalFilterSet(filters.FilterSet):
    game = filters.ModelChoiceFilter(queryset=Game.objects.all().select_related('game_day', 'home_team', 'away_team'))

    class Meta:
        model = GameGoal
        fields = ('game', 'team', 'team_against', 'period',)
