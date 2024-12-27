/**
 * If you are wondering why fields like gender and get_gender_display exist it's because Django's CharField supports a
 * choices kwarg allowing for code friendly (male, female, non_binary) and end user friendly (Male, Female, Non-binary)
 * values. You will see fields and their get_*_display equivalents in the types below.
 *
 * Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#choices
 */

interface User {
  id: number;
  first_name: string;
  last_name: string;
  full_name: string;
  date_joined: Date;
  gender?: string;
  get_gender_display?: string;
}

interface Division {
  id: number;
  name: string;
}

interface Season {
  id: number;
  start: Date;
  end: Date;
  is_past: boolean;
  is_current: boolean;
  is_future: boolean;
  year: number;
}

interface NestedTeam {
  id: number;
  name: string;
  logo: string;
  jersey_colors?: string[];
  short_name: string;
}

interface TeamSeasonRegistration {
  team: NestedTeam;
  season: Season;
  division: Division;
  points: number;
  wins: number;
  losses: number;
  ties: number;
  overtime_losses: number;
  shootout_losses: number;
  games_played: number;
  goals_for: number;
  goals_against: number;
  goal_differential: number;
  home_wins: number;
  home_losses: number;
  away_wins: number;
  away_losses: number;
  regulation_wins: number;
  regulation_losses: number;
  overtime_wins: number;
  shootout_wins: number;
  home_games_played: number;
  away_games_played: number;
  home_regulation_wins: number;
  home_regulation_losses: number;
  home_overtime_wins: number;
  home_overtime_losses: number;
  home_shootout_wins: number;
  home_shootout_losses: number;
  home_ties: number;
  away_regulation_wins: number;
  away_regulation_losses: number;
  away_overtime_wins: number;
  away_overtime_losses: number;
  away_shootout_wins: number;
  away_shootout_losses: number;
  away_ties: number;
  home_goals_for: number;
  home_goals_against: number;
  away_goals_for: number;
  away_goals_against: number;
  place: number;
  point_percentage: number;
}

interface Team extends NestedTeam {
  seasons: TeamSeasonRegistration[];
}

interface UserSeasonRegistration {
  id: number;
  user: User;
  season: Season;
  team: Team;
  is_captain: boolean;
  position: string;
  get_position_display: string;
  registered_at: Date;
  location: string;
  get_location_display: string;
  games_played: number;
  goals: number;
  primary_assists: number;
  secondary_assists: number;
  assists: number;
  points: number;
  place: number;
}

interface NestedGameDay {
  id: number;
  day: Date;
  season: Season;
  opening_team: NestedTeam;
  closing_team: NestedTeam;
}

interface Game {
  id: number;
  game_day: NestedGameDay;
  start: string;
  duration: string;
  end: string;
  home_team: NestedTeam;
  home_team_division_name: string;
  home_team_num_goals: number;
  home_team_display: string;
  away_team: NestedTeam;
  away_team_division_name: string;
  away_team_num_goals: number;
  away_team_display: string;
  location: string;
  court: string;
  get_court_display: string;
  type: string;
  get_type_display: string;
  winning_team_id?: number;
  losing_team_id?: number;
  status: string;
  get_status_display: string;
  result: string;
  get_result_display: string;
}

interface GameDay extends NestedGameDay {
  games: Game[];
}

interface GameReferee {
  id: number;
  game: number;
  user: User;
  type: string;
  get_type_display: string;
}

interface GamePlayer {
  id: number;
  game: number;
  user: User;
  team: NestedTeam;
  is_substitute: boolean;
  is_goalie: boolean;
}

interface GameGoal {
  id: number;
  game: number;
  team: NestedTeam;
  team_against: NestedTeam;
  period: string;
  get_period_display: string;
  scored_by: GamePlayer;
  assisted_by1?: GamePlayer;
  assisted_by2?: GamePlayer;
}
