from django_filters import rest_framework as filters

from .models import Season


class SeasonFilterSet(filters.FilterSet):
    start = filters.DateFromToRangeFilter()
    end = filters.DateFromToRangeFilter()

    class Meta:
        model = Season
        fields = ('start', 'end')
