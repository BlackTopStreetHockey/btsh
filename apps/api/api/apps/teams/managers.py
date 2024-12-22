from django.db import models
from django.db.models import F, Window
from django.db.models.functions import RowNumber


class TeamSeasonRegistrationQuerySet(models.QuerySet):
    def with_place_by_season(self):
        """Computes a team's season placing/ranking."""
        return self.annotate(
            place=Window(
                expression=RowNumber(),
                partition_by=[F('season')],
                order_by=[
                    F('points').desc(),
                    # including head to head wins here would require another db table to store that or some subquery
                    # that isn't obvious at this time, going to descope that for now in favor of a manual override field
                    # TODO eventually add other tie breaker rules
                ]
            )
        )


class TeamSeasonRegistrationManager(models.Manager):
    ...
