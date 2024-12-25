import random

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from common.management.commands.utils import get_default_created_by, get_or_create, print_separator
from games.models import Game, GameGoal, GamePlayer, GameReferee
from users.models import User, UserSeasonRegistration


NOW = 'now'
NUM_REFS = 2
MIN_PLAYERS_PER_GAME = 8


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
            status=Game.SCHEDULED,
        ).select_related('game_day__season', 'home_team', 'away_team')

        print(
            f'Simulating {games.count()} scheduled games from {simulate_from.isoformat()} to {simulate_to.isoformat()}.'
        )

        for game in games:
            print(f'Simulating game {game}.')
            teams = game.teams
            home_team = game.home_team
            away_team = game.away_team
            season = game.game_day.season

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
                    # Grab the users registered for the team + season
                    user_season_registrations = UserSeasonRegistration.objects.filter(
                        season=season, team=team
                    ).order_by('user__first_name', 'user__last_name')

                    num_user_season_registrations = user_season_registrations.count()
                    # Simulate varying attendances
                    if num_user_season_registrations < MIN_PLAYERS_PER_GAME:
                        num_players_for_game = num_user_season_registrations
                    else:
                        num_players_for_game = random.randint(MIN_PLAYERS_PER_GAME, num_user_season_registrations)

                    user_season_registrations = list(user_season_registrations)
                    random.shuffle(user_season_registrations)
                    user_season_registrations_for_game = random.sample(
                        user_season_registrations,
                        num_players_for_game,
                    )

                    print(f'Seeding {num_players_for_game} game players for {team.name}.')
                    for i, user_season_registration in enumerate(user_season_registrations_for_game):
                        kwargs = {
                            'game': game,
                            'user': user_season_registration.user,
                            'team': team,
                        }

                        # TODO add more entropy with subs, users not registered for the team, x male + y female
                        get_or_create(
                            GamePlayer,
                            get_kwargs={**kwargs},
                            create_kwargs={
                                **kwargs,
                                'is_substitute': False,
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
                                    'team_against': home_team if team == away_team else away_team,
                                    'period': period,
                                    'scored_by': scored_by,
                                    'assisted_by1': assisted_by1,
                                    'assisted_by2': assisted_by2,
                                }
                            )

            game.status = Game.COMPLETED
            game.save()

            print_separator()
