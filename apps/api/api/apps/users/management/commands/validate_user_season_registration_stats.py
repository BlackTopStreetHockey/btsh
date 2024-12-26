from django.core.management import BaseCommand

from games.models import Game, GameGoal, GamePlayer
from users.models import UserSeasonRegistration


class Command(BaseCommand):
    help = 'Validate the user season registration stats computations.'

    def handle(self, *args, **options):
        game_type = Game.REGULAR

        user_season_registrations = UserSeasonRegistration.objects.with_place_by_team_and_season(
            game_type=game_type
        ).select_related('user', 'season', 'team')
        for usr in user_season_registrations:
            user = usr.user
            team = usr.team
            season = usr.season

            filter_kwargs = {
                'team': team,
                'game__game_day__season': season,
                'game__status': Game.COMPLETED,
                'game__type': game_type,
            }

            games_played = GamePlayer.objects.filter(**filter_kwargs, user=user).count()
            goals = GameGoal.objects.filter(**filter_kwargs, scored_by__user=user).count()
            primary_assists = GameGoal.objects.filter(**filter_kwargs, assisted_by1__user=user).count()
            secondary_assists = GameGoal.objects.filter(**filter_kwargs, assisted_by2__user=user).count()
            assists = primary_assists + secondary_assists
            points = goals + assists

            print(f'Validating: {usr}')
            assert usr.games_played == games_played, f'{usr.games_played} | {games_played}'
            assert usr.goals == goals, f'{usr.goals} | {goals}'
            assert usr.primary_assists == primary_assists, f'{usr.primary_assists} | {primary_assists}'
            assert usr.secondary_assists == secondary_assists, f'{usr.secondary_assists} | {secondary_assists}'
            assert usr.assists == assists
            assert usr.points == points
