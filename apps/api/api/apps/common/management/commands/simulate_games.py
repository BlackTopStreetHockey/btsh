import random

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_date as django_parse_date

from common.management.commands.utils import get_default_created_by, get_or_create, print_separator
from games.models import Game, GameGoal, GamePlayer, GameReferee
from users.models import User


NOW = 'now'
NUM_REFS = 2


def parse_date(d):
    return timezone.now().date() if d == NOW else django_parse_date(d)


class Command(BaseCommand):
    help = 'Simulate games for local development purposes.'

    def add_arguments(self, parser):
        parser.add_argument('from', help=f'YYYY-MM-DD or "{NOW}"')
        parser.add_argument('to', help=f'YYYY-MM-DD or "{NOW}"')

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print('This should only be run for local development.')
            return

        created_by = get_default_created_by()
        simulate_from = parse_date(options.get('from'))
        simulate_to = parse_date(options.get('to'))

        users = User.objects.all()
        users_list = list(users)
        games = Game.objects.filter(
            game_day__day__gte=simulate_from,
            game_day__day__lte=simulate_to,
        ).select_related('game_day', 'home_team', 'away_team')

        print(f'Simulating {games.count()} games from {simulate_from.isoformat()} to {simulate_to.isoformat()}.')

        for game in games:
            print(f'Simulating game {game}.')
            teams = game.teams

            if not GameReferee.objects.filter(game=game).exists():
                print(f'Seeding {NUM_REFS} game refs.')
                ref_users = random.sample(users_list, NUM_REFS)
                for i, user in enumerate(ref_users):
                    kwargs = {
                        'game': game,
                        'user': user,
                        'type': list(GameReferee.TYPES.keys())[i],
                    }
                    get_or_create(
                        GameReferee,
                        get_kwargs={**kwargs},
                        create_kwargs={**kwargs, 'created_by': created_by},
                    )

            if not GamePlayer.objects.filter(game=game).exists():
                for team in teams:
                    num_players = random.randint(8, 23)
                    # TODO use players from the team's roster instead of the full pool of users, choose x male and y
                    #  female
                    player_users = random.sample(users_list, num_players)
                    print(f'Seeding {num_players} game players for {team.name}.')
                    for i, user in enumerate(player_users):
                        kwargs = {
                            'game': game,
                            'user': user,
                            'team': team,
                        }
                        get_or_create(
                            GamePlayer,
                            get_kwargs={**kwargs},
                            create_kwargs={
                                **kwargs,
                                'is_substitute': False,  # TODO add more entropy with subs
                                'is_goalie': i == 0,
                                'created_by': created_by,
                            }
                        )

            if not GameGoal.objects.filter(game=game).exists():
                # TODO OT, SO
                periods = [GameGoal.FIRST, GameGoal.SECOND]
                game_players = GamePlayer.objects.filter(game=game)
                for period in periods:
                    for team in teams:
                        players = game_players.filter(team=team).exclude(is_goalie=True)
                        players_list = list(players)
                        num_goals = random.randint(0, 5)
                        print(f'Seeding {num_goals} goals for {team.name} in period {period}.')
                        for i in range(num_goals):
                            player_choices = random.sample(players_list, k=3)
                            scored_by = player_choices[0]
                            assisted_by1 = player_choices[1] if random.randint(0, 1) == 0 else None
                            assisted_by2 = player_choices[2] if assisted_by1 and random.randint(0, 1) == 0 else None

                            get_or_create(
                                GameGoal,
                                get_kwargs={'pk': None},
                                create_kwargs={
                                    'game': game,
                                    'team': team,
                                    'period': period,
                                    'scored_by': scored_by,
                                    'assisted_by1': assisted_by1,
                                    'assisted_by2': assisted_by2,
                                }
                            )

            game.status = Game.COMPLETED
            game.save()

            print_separator()
