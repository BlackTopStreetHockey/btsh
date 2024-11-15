import random

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from common.management.commands.utils import get_default_created_by, print_separator
from games.models import Game, GamePlayer, GameReferee
from users.models import User


NOW = 'now'
NUM_REFS = 2


def parse_date(d):
    return timezone.now().date() if d == NOW else parse_datetime(d).date()


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

            if not GameReferee.objects.filter(game=game).exists():
                print(f'Seeding {NUM_REFS} game refs.')
                ref_users = random.sample(users_list, NUM_REFS)
                for i, user in enumerate(ref_users):
                    GameReferee.objects.get_or_create(
                        game=game,
                        user=user,
                        type=list(GameReferee.TYPES.keys())[i],
                        defaults={'created_by': created_by}
                    )

            if not GamePlayer.objects.filter(game=game).exists():
                for team in game.teams:
                    num_players = random.randint(8, 23)
                    # TODO use players from the team's roster instead of the full pool of users, choose x male and y
                    #  female
                    player_users = random.sample(users_list, num_players)
                    print(f'Seeding {num_players} game players for {team.name}.')
                    for i, user in enumerate(player_users):
                        GamePlayer.objects.get_or_create(
                            game=game,
                            user=user,
                            team=team,
                            # TODO add more entropy with subs
                            defaults={'is_substitute': False, 'is_goalie': i == 0, 'created_by': created_by}
                        )

            print_separator()
