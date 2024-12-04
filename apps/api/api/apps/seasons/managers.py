from django.db import models


class SeasonRegistrationQuerySet(models.QuerySet):
    def for_team(self, team, season=None):
        kwargs = {'team': team}
        if season:
            kwargs.update({'season': season})
        return self.filter(**kwargs).select_related('user', 'team', 'season')


class SeasonRegistrationManager(models.Manager):
    ...
