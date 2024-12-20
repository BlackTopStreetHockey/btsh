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
    """Get the completed regular season games for the given team in the given season."""
    from games.models import Game

    return Game.objects.for_team(team).filter(
        status=Game.COMPLETED,
        type=Game.REGULAR,
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

    from games.models import GameResultsEnum

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

            regulation_filter = Q(result=GameResultsEnum.FINAL)
            overtime_filter = Q(result=GameResultsEnum.FINAL_OT)
            shootout_filter = Q(result=GameResultsEnum.FINAL_SO)
            home_team_filter = Q(home_team=team)
            away_team_filter = Q(away_team=team)
            winning_team_filter = Q(winning_team_id=team.id)
            losing_team_filter = Q(losing_team_id=team.id)
            tie_filter = Q(winning_team_id=None) & Q(losing_team_id=None)

            games = get_games(team, season)
            stats = games.aggregate(
                # Games played
                home_games_played=Count('id', filter=home_team_filter),
                away_games_played=Count('id', filter=away_team_filter),

                # Home wins, losses, ties
                home_regulation_wins=Count('id', filter=home_team_filter & regulation_filter & winning_team_filter),
                home_regulation_losses=Count('id', filter=home_team_filter & regulation_filter & losing_team_filter),
                home_overtime_wins=Count('id', filter=home_team_filter & overtime_filter & winning_team_filter),
                home_overtime_losses=Count('id', filter=home_team_filter & overtime_filter & losing_team_filter),
                home_shootout_wins=Count('id', filter=home_team_filter & shootout_filter & winning_team_filter),
                home_shootout_losses=Count('id', filter=home_team_filter & shootout_filter & losing_team_filter),
                home_ties=Count('id', filter=home_team_filter & tie_filter),

                # Away wins, losses, ties
                away_regulation_wins=Count('id', filter=away_team_filter & regulation_filter & winning_team_filter),
                away_regulation_losses=Count('id', filter=away_team_filter & regulation_filter & losing_team_filter),
                away_overtime_wins=Count('id', filter=away_team_filter & overtime_filter & winning_team_filter),
                away_overtime_losses=Count('id', filter=away_team_filter & overtime_filter & losing_team_filter),
                away_shootout_wins=Count('id', filter=away_team_filter & shootout_filter & winning_team_filter),
                away_shootout_losses=Count('id', filter=away_team_filter & shootout_filter & losing_team_filter),
                away_ties=Count('id', filter=away_team_filter & tie_filter),
            )

            # The kwargs in the above aggregate intentionally match the model field names
            for k, v in stats.items():
                setattr(team_season_registration, k, v)
            team_season_registration.save()
