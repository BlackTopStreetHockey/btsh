import datetime

from seasons.models import Season
from teams.models import Team, TeamSeasonRegistration


def get_teams(teams: list[Team] | None):
    kwargs = {}
    if teams:
        kwargs.update({'id__in': [t.id for t in teams]})
    return Team.objects.filter(**kwargs)


def get_seasons(seasons: list[Season] | None):
    kwargs = {}
    if seasons:
        kwargs.update({'id__in': [s.id for s in seasons]})
    return Season.objects.filter(**kwargs)


def calculate_team_season_registration_stats(game_type, limit_to_teams=None, limit_to_seasons=None, debug=False):
    """
    Calculates stats, this can also be called as a management command or from the team and seasons admins.

    If the args are not provided will calculate stats for all teams in all seasons.

    Args:
        game_type: Game type to compute stats for (i.e. regular or playoff)
        limit_to_teams: Only calculate stats for the provided teams. If seasons are also provided only calculate stats
            for the teams and seasons.
        limit_to_seasons: Only calculate stats for the provided seasons. If teams are also provided only calculate stats
            for the seasons and teams.
        debug: Whether to print debug messages.
    """

    from games.models import Game

    start = datetime.datetime.now()
    for team in get_teams(limit_to_teams):
        if debug:
            print(f'Processing {team.name}.')

        for season in get_seasons(limit_to_seasons):
            if debug:
                print(f'  Processing {season}.')

            try:
                team_season_registration = TeamSeasonRegistration.objects.get(team=team, season=season)
            except TeamSeasonRegistration.DoesNotExist:
                if debug:
                    print(f'  {team.name} is not registered for the {season}, skipping...')
                continue

            # The keys of this dict match the model field names
            stats: dict = Game.objects.with_stats(team, season, game_type)
            for k, v in stats.items():
                setattr(team_season_registration, k, v)
            team_season_registration.save()
            if debug:
                print('    Updated stats.')

    if debug:
        print(f'Took: {datetime.datetime.now() - start}')


def calculate_team_season_registration_stats_from_game(game, statuses=None):
    """Helper function since we'll generally calculate stats when a game or game goal is created, updated, deleted"""
    from games.models import Game

    if statuses is None or game.status in statuses:
        season = game.game_day.season
        calculate_team_season_registration_stats(
            game_type=Game.REGULAR,
            limit_to_teams=game.teams,
            limit_to_seasons=[season],
        )
