from django_filters import rest_framework as filters

from divisions.models import Division
from seasons.models import Season
from .models import Team, TeamSeasonRegistration


class TeamFilterSet(filters.FilterSet):
    season = filters.ModelChoiceFilter(label='Season', queryset=Season.objects.all(), method='filter_season')
    division = filters.ModelChoiceFilter(label='Division', queryset=Division.objects.all(), method='filter_division')

    def filter_season(self, queryset, name, value):
        return queryset.filter(team_season_registrations__season=value) if value else queryset

    def filter_division(self, queryset, name, value):
        return queryset.filter(team_season_registrations__division=value) if value else queryset

    class Meta:
        model = Team
        fields = ('season', 'division',)


class TeamSeasonRegistrationFilterSet(filters.FilterSet):
    class Meta:
        model = TeamSeasonRegistration
        fields = ('team', 'season', 'division',)
