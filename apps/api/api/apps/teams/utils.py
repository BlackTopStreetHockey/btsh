from django.db.models import Count, Q

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


def get_games(team, season):
    """Get the completed games for the given team in the given season."""
    from games.models import Game

    return Game.objects.for_team(team).filter(
        status=Game.COMPLETED,
        game_day__season=season,
    ).select_related(
        'home_team',
        'away_team',
        'game_day__season',
    ).prefetch_related(
        'goals',
    ).with_scores()


def calculate_team_season_registration_stats(limit_to_team=None, limit_to_season=None, debug=False):
    """
    Calculates stats, this can also be called as a management command or from the team and seasons admins.

    If the args are not provided will calculate stats for all teams in all seasons.

    Args:
        limit_to_team: Only calculate stats for the provided team. If season is also provided only calculate stats for the team and season.
        limit_to_season: Only calculate stats for the provided season. If team is also provided only calculate stats for the season and team.
    """

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

            games = get_games(team, season)
            games_with_aggregates = games.aggregate(
                home_games_played=Count('id', filter=Q(home_team=team)),
                away_games_played=Count('id', filter=Q(away_team=team)),
            )

            for game in games:
                pass

            home_games_played = games_with_aggregates.get('home_games_played')
            away_games_played = games_with_aggregates.get('away_games_played')
            kwargs = {
                'home_games_played': home_games_played,
                'away_games_played': away_games_played,
            }
            for k, v in kwargs.items():
                setattr(team_season_registration, k, v)
            team_season_registration.save()
