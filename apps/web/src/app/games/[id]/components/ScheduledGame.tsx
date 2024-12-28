"use client";
import TeamName from "@/components/teams/team-name";
import formatDateNoTimezone, { formatTime } from "@/lib/dates";
import { useGame } from "@/hooks/requests/useGame";
import clsx from "clsx";
import { useParams } from "next/navigation";
import { GamePlayers } from "@/app/games/[id]/components/GamePlayers";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { GameScoring } from "@/app/games/[id]/components/GameScoring";
import { GameReferees } from "./GameReferees";

export default function ScheduledGame({ game }) {
  const homeTeamWin =
    game.status === "completed" && game.winning_team_id === game.home_team.id;
  const awayTeamWin =
    game.status === "completed" && game.winning_team_id === game.away_team.id;

  return (
    <div className="container mx-auto p-8">
      <div className="grid gap-4">
        <Card>
          <CardContent>
            <div className="flex flex-row gap-8 justify-center p-4">
              <div className="flex flex-row gap-2">
                <TeamName
                  team={game.away_team}
                  className="text-2xl font-bold"
                  link={true}
                />
              </div>

              <div className="text-2xl">@</div>

              <div className="flex flex-row gap-2">
                <TeamName
                  team={game.home_team}
                  className="text-2xl font-bold"
                  link={true}
                />
              </div>
            </div>
            <div className="flex flex-col items-center gap-0">
              <div className="text-md text-bold">{game.get_status_display}</div>
              <div className="text-md">
                {formatDateNoTimezone(game.game_day.day, "eeee, MMMM do y")} |{" "}
                {formatTime(game.start.toString())}
              </div>
              <div className="text-md">
                {game.location} | {game.get_court_display} Court
              </div>
              <GameReferees game={game} />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
