import GameGoal from "@/components/games/GameGoal";
import TeamName from "@/components/teams/team-name";
import { useGameGoals } from "@/hooks/requests/useGameGoals";
import { useGamePlayers } from "@/hooks/requests/useGamePlayers";
import { useGameReferees } from "@/hooks/requests/useGameReferees";
import formatDateNoTimezone, { formatTime } from "@/lib/dates";
import { numberToOrdinal } from "@/lib/utils";
import clsx from "clsx";
import { Card, CardContent } from "../ui/card";

export default function CompletedGame({ game }: { game: Game }) {
  const { teamToGoals, placeholder: goalsPlaceholder } = useGameGoals({
    gameId: game.id,
  });
  const { referees, placeholder: refereesPlaceholder } = useGameReferees({
    gameId: game.id,
  });
  const { teamToPlayers, placeholder: playersPlaceholder } = useGamePlayers({
    gameId: game.id,
  });

  const homeTeamWin = game.winning_team_id === game.home_team.id;
  const awayTeamWin = game.winning_team_id === game.away_team.id;

  if (!!goalsPlaceholder) {
    return goalsPlaceholder;
  }
  if (!!refereesPlaceholder) {
    return refereesPlaceholder;
  }
  if (!!playersPlaceholder) {
    return playersPlaceholder;
  }
  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardContent>
          <div className="flex flex-row gap-8 justify-center">
            <div className="flex flex-row gap-2">
              <TeamName team={game.away_team} link={true} />

              <div className={clsx("text-2xl", { "font-bold": awayTeamWin })}>
                {game.away_team_num_goals}
              </div>
              {awayTeamWin && <div className="text-2xl font-bold">(W)</div>}
            </div>

            <div className="text-2xl">@</div>

            <div className="flex flex-row gap-2">
              <TeamName team={game.home_team} link={true} />

              <div className={clsx("text-2xl", { "font-bold": homeTeamWin })}>
                {game.home_team_num_goals}
              </div>
              {homeTeamWin && <div className="text-2xl font-bold">(W)</div>}
            </div>
          </div>
          <div className="flex flex-col items-center gap-0">
            <div className="text-md text-bold">{game.get_result_display}</div>
            <div className="text-md">
              {formatDateNoTimezone(game.game_day.day, "eeee, MMMM do y")} |{" "}
              {formatTime(game.start.toString())}
            </div>
            <div className="text-md">
              {game.location} | {game.get_court_display} Court
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <div className="flex flex-col items-center">
            <div className="text-lg font-bold bg-white">Scoring</div>
            <div className="flex flex-row gap-8">
              {[game.away_team.id, game.home_team.id].map((teamId) => (
                <div className="bg-white">
                  {teamToGoals[teamId]?.map((period: any) => (
                    <div
                      key={period.period}
                      className="flex flex-col gap-1 p-2 bg-white"
                    >
                      <div className="font-bold text-sm">
                        {numberToOrdinal(period.period)}
                      </div>
                      {period.goals.map((goal: GameGoal) => (
                        <GameGoal goal={goal} key={goal.id} />
                      ))}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <div className="flex flex-col items-center">
            <div className="text-lg font-bold bg-white">Referees</div>
            {referees.map((referee: GameReferee) => (
              <div
                key={referee.id}
                className="flex flex-row gap-4 items-center justify-between"
              >
                <div className="text-gray-400 text-xs">
                  {referee.type.toUpperCase()}
                </div>
                <div className="text-sm">{referee.user.full_name}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <div className="flex flex-col items-center">
            <div className="text-lg font-bold bg-white">Players</div>
            <div className="flex flex-row gap-8">
              {[game.away_team.id, game.home_team.id].map((teamId) => (
                <div key={teamId} className="flex flex-col gap-1 p-2 bg-white">
                  <div className="font-bold text-sm">
                    {teamToPlayers[teamId]?.length} players
                  </div>
                  {teamToPlayers[teamId]?.map((player: GamePlayer) => (
                    <div
                      key={player.id}
                      className="flex flex-row gap-4 items-center justify-between"
                    >
                      <div className="text-sm">{player.user.full_name}</div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
