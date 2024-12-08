from django_filters import rest_framework as filters

from .models import Season, SeasonRegistration


class SeasonFilterSet(filters.FilterSet):
    start = filters.DateFromToRangeFilter()
    end = filters.DateFromToRangeFilter()

    class Meta:
        model = Season
        fields = ('start', 'end')


class SeasonRegistrationFilterSet(filters.FilterSet):
    class Meta:
        model = SeasonRegistration
        fields = ('user', 'season', 'team', 'is_captain', 'position', 'location')
