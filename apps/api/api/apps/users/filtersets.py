from django_filters import rest_framework as filters

from .models import UserSeasonRegistration


class UserSeasonRegistrationFilterSet(filters.FilterSet):
    class Meta:
        model = UserSeasonRegistration
        fields = ('user', 'season', 'team', 'is_captain', 'position', 'location')
