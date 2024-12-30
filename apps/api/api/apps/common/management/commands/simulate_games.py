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


def create_game_referees(count, exclude_user_ids, game, created_by):
    print(f'Seeding {count} game refs.')
    # Exclude users that are playing in the game, including subs
    refs = list(User.objects.exclude(id__in=exclude_user_ids))
    random.shuffle(refs)
    sampled_refs = random.sample(refs, k=count)
    for i, user in enumerate(sampled_refs):
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


def get_potential_scorers_assisters(game_players, team):
    players = game_players.filter(team=team).exclude(is_goalie=True)
    return players, list(players)


def compute_scored_by_assisted_by1_assisted_by2(players):
    sampled_players = random.sample(players, k=3)
    scored_by = sampled_players[0]
    assisted_by1 = sampled_players[1] if random.randint(0, 1) == 0 else None
    assisted_by2 = sampled_players[2] if assisted_by1 and random.randint(0, 1) == 0 else None
    return scored_by, assisted_by1, assisted_by2


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

            if not GameReferee.objects.filter(game=game).exists():
                exclude_user_ids = GamePlayer.objects.filter(game=game).values_list('user__id', flat=True)
                create_game_referees(NUM_REFS, exclude_user_ids, game, created_by)

            if not GameGoal.objects.filter(game=game).exists():
                periods = [GameGoal.FIRST, GameGoal.SECOND]
                game_players = GamePlayer.objects.filter(game=game)
                for period in periods:
                    for team in teams:
                        players, players_list = get_potential_scorers_assisters(game_players, team)
                        num_goals = random.randint(0, 5)
                        print(f'Seeding {num_goals} goals for {team.name} in period {period}.')
                        for i in range(num_goals):
                            scored_by, assisted_by1, assisted_by2 = compute_scored_by_assisted_by1_assisted_by2(
                                players_list
                            )

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

                game_goals = GameGoal.objects.filter(game=game)
                if game_goals.filter(team=home_team).count() == game_goals.filter(team=away_team).count():
                    # None represents the game stays a tie
                    period = random.choice([GameGoal.OT, GameGoal.SO, None])
                    if period is None:
                        continue

                    team = random.choice(teams)
                    team_against = home_team if team == away_team else away_team

                    players, players_list = get_potential_scorers_assisters(game_players, team)
                    scored_by, assisted_by1, assisted_by2 = compute_scored_by_assisted_by1_assisted_by2(players_list)

                    print(f'\n{team.name} wins in {period.upper()}!\n')
                    get_or_create(
                        GameGoal,
                        get_kwargs={'pk': None},
                        create_kwargs={
                            'game': game,
                            'team': team,
                            'team_against': team_against,
                            'period': period,
                            'scored_by': scored_by,
                            'assisted_by1': None if period == GameGoal.SO else assisted_by1,
                            'assisted_by2': None if period == GameGoal.SO else assisted_by2,
                        }
                    )

            game.status = Game.COMPLETED
            game.save()

            print_separator()

        print(f'Took: {datetime.datetime.now() - start}')
