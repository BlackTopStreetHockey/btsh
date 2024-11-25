interface User {
  id: number;
  first_name: string;
  last_name: string;
  full_name: string;
  date_joined: string;
}
interface Team {
  id: number;
  name: string;
  logo: string;
  jersey_colors?: string[];
  short_name: string;
}

interface Season {
  id: number;
  year: number;
  start: Date;
  end: Date;
  is_current: boolean;
  is_past: boolean;
  is_future: boolean;
}

interface Division {
  id: number;
  name: string;
}

interface GameDay {
  id: number;
  day: Date;
  season: Season;
  opening_team: Team;
  closing_team: Team;
  games: Game[];
}

interface GamePlayer {
  id: number;
  game: Game;
  user: User;
  team: Team;
  is_substitute: boolean;
  is_goalie: boolean;
}

interface GameReferee {
  id: number;
  game: Game;
  user: User;
  type: string;
}

interface GameGoal {
  id: number;
  game: Game;
  team: Team;
  period: string;
  scored_by: GamePlayer;
  assisted_by1: GamePlayer;
  assisted_by2: GamePlayer;
}
interface Game {
  id: number;
  start: Date;
  duration: number;
  end: Date;
  home_team: Team;
  away_team: Team;
  location: string;
  court: string;
  get_court_display: string;
  get_status_display: string;
  get_type_display: string;
  status: string;
  game_day?: GameDay;
  home_team_num_goals: number;
  away_team_num_goals: number;
  winning_team_id: number;
  losing_team_id: number;
  goals: GameGoal[];
  players: GamePlayer[];
  referees: GameReferee[];
}

