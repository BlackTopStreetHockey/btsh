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
  seasons: TeamSeason[];
  short_name: string;
}

interface Player {
  id?: number;
  name: string;
  gender?: string;
  number?: number;
  position?: string;
  gp?: number;
  goals?: number;
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

interface TeamSeason {
  season: Season;
  division: Division;
}

interface Game {
  id: number;
  court: string;
  home_team: Team;
  away_team: Team;
  result: string;
}

interface GameDay {
  id: number;
  day: Date;
  season: Season;
  opening_team: Team;
  closing_team: Team;
  games: Game[];
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
  game_day?: GameDay;
}
