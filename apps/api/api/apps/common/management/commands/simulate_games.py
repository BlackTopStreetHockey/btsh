import datetime
import random

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_date as django_parse_date

from common.management.commands.utils import get_default_created_by, get_or_create, print_separator
from games.models import Game, GameGoal, GamePlayer, GameReferee
from users.models import User, UserSeasonRegistration


NOW = 'now'
NUM_REFS = 2
MIN_PLAYERS_PER_GAME = 8
MIN_PLAYERS_PER_GAME_SUBS_NEEDED = MIN_PLAYERS_PER_GAME // 2


def parse_date(d):
    return timezone.now().date() if d == NOW else django_parse_date(d)


def create_game_players(users, team, game, are_subs, created_by):
    count = len(users)

    if count <= 0:
        return

    if are_subs:
        print(f'Seeding {count} game player subs for {team.name}.')
    else:
        print(f'Seeding {count} game players for {team.name}.')

    for i, user in enumerate(users):
        kwargs = {
            'game': game,
            'user_id': user,
            'team': team,
        }

        # TODO add more entropy with users not registered for the team, x male + y female, goalie subs
        get_or_create(
            GamePlayer,
            get_kwargs={**kwargs},
            create_kwargs={
                **kwargs,
                'is_substitute': are_subs,
                'is_goalie': i == 0 if not are_subs else False,
                'created_by': created_by,
            }
        )


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

        games = Game.objects.filter(
            game_day__day__gte=simulate_from,
            game_day__day__lte=simulate_to,
            status=Game.SCHEDULED,
        ).select_related('game_day__season', 'home_team', 'away_team')

        print(
            f'Simulating {games.count()} scheduled games from {simulate_from.isoformat()} to {simulate_to.isoformat()}.'
        )

        start = datetime.datetime.now()
        for game in games:
            print(f'Simulating game id {game.id} - {game}.')
            teams = game.teams
            home_team = game.home_team
            away_team = game.away_team
            season = game.game_day.season

            if not GameReferee.objects.filter(game=game).exists():
                print(f'Seeding {NUM_REFS} game refs.')
                user_ids = UserSeasonRegistration.objects.filter(
                    season=season,
                    team__in=teams,
                ).values_list('user__id', flat=True)
                # Exclude users that are registered for the home or away team since they may be playing in the game
                available_refs = list(User.objects.exclude(id__in=user_ids))
                random.shuffle(available_refs)
                ref_users = random.sample(available_refs, NUM_REFS)
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
                    # Grab the eligible users for the game (i.e. users registered for the team + season)
                    game_users = UserSeasonRegistration.objects.filter(
                        season=season, team=team
                    ).order_by('user__first_name', 'user__last_name').values_list('user__id', flat=True)
                    # Grab the eligible subs
                    sub_users = UserSeasonRegistration.objects.filter(
                        season=season
                    ).exclude(
                        user__in=game_users
                    ).order_by('user__first_name', 'user__last_name').values_list('user__id', flat=True)

                    num_game_users = random.randint(MIN_PLAYERS_PER_GAME_SUBS_NEEDED, game_users.count())
                    # Simulate varying attendances
                    if num_game_users <= MIN_PLAYERS_PER_GAME:
                        num_game_users_for_game = num_game_users
                        num_sub_users_for_game = MIN_PLAYERS_PER_GAME - num_game_users
                    else:
                        num_game_users_for_game = random.randint(MIN_PLAYERS_PER_GAME, num_game_users)
                        num_sub_users_for_game = 0

                    game_users_list = list(game_users)
                    random.shuffle(game_users_list)
                    sub_users_list = list(sub_users)
                    random.shuffle(sub_users_list)

                    sampled_game_users = random.sample(game_users_list, num_game_users_for_game)
                    sampled_sub_users = random.sample(sub_users_list, num_sub_users_for_game)

                    create_game_players(sampled_game_users, team, game, False, created_by)
                    create_game_players(sampled_sub_users, team, game, True, created_by)

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

        print(f'Took: {datetime.datetime.now() - start}')
