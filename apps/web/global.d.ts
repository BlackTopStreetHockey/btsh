interface Game {
    date: string;
    time: string | 'BYE';
    court?: 'EAST' | 'WEST' | '' | string;
    home?: string;
    away?: string;
    homeScore?: string;
    awayScore?: string;
    status?: 'SCHEDULED' | 'ACTIVE' | 'CANCELLED' | 'POSTPONED' | 'FINAL' | 'FINAL/OT' | 'FINAL/SO' | string;
    title?: string;
    description?: string;
  }
  
  type TeamShortName =
    | 'LBS'
    | 'FK'
    | 'FUZZ'
    | 'CK'
    | 'IK'
    | 'VERT'
    | 'HOOK'
    | 'GANK'
    | 'POU'
    | 'FLTH'
    | 'MEGA'
    | 'SKYF'
    | 'WTP'
    | 'DEM'
    | 'GREM'
    | 'DARK'
    | 'BTC'
    | 'RIOT'
    | 'REN'
    | 'MOBY'
    | 'BTSH';
  
  type TeamInfo = {
    name: string;
    shortName: TeamShortName;
    logoUrl?: string;
    roster?: Player[];
  };
  
  type TeamRecord = {
    wins: number;
    losses: number;
    otLosses: number;
  };
  
  type Team = TeamInfo & TeamRecord;
  
  interface TeamStanding {
    div: 1 | 2 | 3 | 4 | 0;
    record: TeamRecord;
    points: number;
    diff: number;
    wkChange: number;
  }
  
  interface Player {
    id: string;
    name: string;
    gender?: 'M' | 'F' | string;
    team: string;
    position?: 'F' | 'D' | 'G' | string;
  }
  
  interface Goalie extends Player {
    wins: number;
    svp: string;
  }
  
  interface BoxScore {
    game: Game;
    homeScores: number[];
    awayScores: number[];
    away: Team;
    home: Team;
  }
  
  interface Division {
    name: string;
    teams: Team[];
  }
  
  type ReducedGame = Record<string, Game[]>;