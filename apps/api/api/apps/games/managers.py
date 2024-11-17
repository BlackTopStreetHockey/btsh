from django.db import models
from django.db.models import Case, Count, F, Q, Value, When


class GameQuerySet(models.QuerySet):
    def with_scores(self):
        return self.annotate(
            home_team_num_goals=Count('goals', filter=Q(goals__team=F('home_team'))),
            away_team_num_goals=Count('goals', filter=Q(goals__team=F('away_team'))),
            winning_team_id=Case(
                When(home_team_num_goals__gt=F('away_team_num_goals'), then=F('home_team')),
                When(home_team_num_goals__lt=F('away_team_num_goals'), then=F('away_team')),
                default=Value(None),
            ),
            losing_team_id=Case(
                When(winning_team_id=F('home_team'), then=F('away_team')),
                When(winning_team_id=F('away_team'), then=F('home_team')),
                default=Value(None),
            ),
            # TODO handle ties, ot, so
        )


class GameManager(models.Manager):
    ...
