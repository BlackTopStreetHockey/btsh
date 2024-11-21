from django.db import models
from django.db.models import Case, Count, F, Q, Value, When


class GameQuerySet(models.QuerySet):
    def with_scores(self):
        from games.models import GameGoal, GameResultsEnum, Game

        return self.annotate(
            home_team_num_goals=Case(
                When(status=Game.COMPLETED, then=Count('goals', filter=Q(goals__team=F('home_team')))),
                default=None,
            ),
            away_team_num_goals=Case(
                When(status=Game.COMPLETED, then=Count('goals', filter=Q(goals__team=F('away_team')))),
                default=None,
            ),
            winning_team_id=Case(
                When(home_team_num_goals__gt=F('away_team_num_goals'), then=F('home_team')),
                When(home_team_num_goals__lt=F('away_team_num_goals'), then=F('away_team')),
                When(home_team_num_goals=F('away_team_num_goals'), then=None),  # Tie or game not completed
            ),
            losing_team_id=Case(
                When(winning_team_id=F('home_team'), then=F('away_team')),
                When(winning_team_id=F('away_team'), then=F('home_team')),
                When(winning_team_id=None, then=None),  # Tie or game not completed
            ),

            # TODO tweak this if changing how we handle shootouts, currently if a game has a goal with period "SO" it's
            # treated as Final/SO
            num_shootout_goals=Count('goals', filter=Q(goals__period=GameGoal.SO)),
            num_ot_goals=Count('goals', filter=Q(goals__period=GameGoal.OT)),
            result=Case(
                When(~Q(status=Game.COMPLETED), then=None),
                When(num_shootout_goals__gt=0, then=Value(GameResultsEnum.FINAL_SO.value)),
                When(num_ot_goals__gt=0, then=Value(GameResultsEnum.FINAL_OT.value)),
                default=Value(GameResultsEnum.FINAL.value),
            ),
            get_result_display=Case(
                When(result=None, then=None),
                When(result=GameResultsEnum.FINAL_SO.value, then=Value(GameResultsEnum.FINAL_SO.label)),
                When(result=GameResultsEnum.FINAL_OT.value, then=Value(GameResultsEnum.FINAL_OT.label)),
                default=Value(GameResultsEnum.FINAL.label),
            )
        )


class GameManager(models.Manager):
    ...
