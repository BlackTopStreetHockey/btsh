from seasons.models import Season
from teams.models import Team, TeamSeasonRegistration


def get_teams(team: Team | None):
    kwargs = {}
    if team:
        kwargs.update({'id': team.id})
    return Team.objects.filter(**kwargs)


def get_seasons(season: Season | None):
    kwargs = {}
    if season:
        kwargs.update({'id': season.id})
    return Season.objects.filter(**kwargs)


def calculate_team_season_registration_stats(game_type, limit_to_team=None, limit_to_season=None, debug=False):
    """
    Calculates stats, this can also be called as a management command or from the team and seasons admins.

    If the args are not provided will calculate stats for all teams in all seasons.

    Args:
        game_type: Game type to compute stats for (i.e. regular or playoff)
        limit_to_team: Only calculate stats for the provided team. If season is also provided only calculate stats for the team and season.
        limit_to_season: Only calculate stats for the provided season. If team is also provided only calculate stats for the season and team.
        debug: Whether to print debug messages.
    """

    from games.models import Game

    for team in get_teams(limit_to_team):
        if debug:
            print(f'Processing {team.name}.')

        for season in get_seasons(limit_to_season):
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
