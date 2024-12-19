"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import { ScrollArea } from "@/components/ui/scroll-area";

import { useSchedule } from "@/hooks/requests/useSchedule";
import { formatTime } from "@/lib/dates";
export function TeamSchedule({
  seasonId = "2",
  teamId = "2",
  seasonYear,
}: {
  seasonId: string;
  teamId: string;
  seasonYear: string;
}) {
  const { schedule } = useSchedule({ seasonId, teamId });

  const seasonSchedule = schedule?.filter(
    (game: GameDay) => game.season.id.toString() === seasonId
  );

  const teamSchedule = seasonSchedule?.filter((gameDay: GameDay) => {
    return gameDay.games.find(
      (g) =>
        g.home_team.id.toString() === teamId.toString() ||
        g.away_team.id.toString() === teamId.toString()
    );
  });

  console.log("teamSchedule:", teamSchedule);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{seasonYear} Schedule</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          <ScrollArea className="h-[500px]">
            {teamSchedule?.map((gameDay: GameDay) => (
              <li
                key={gameDay.id}
                className="flex justify-between items-center border-b pb-2 last:border-b-0"
              >
                {gameDay.games
                  .filter(
                    (g) =>
                      g.home_team.id.toString() === teamId.toString() ||
                      g.away_team.id.toString() === teamId.toString()
                  )
                  .map((game) => {
                    const isHomeGame =
                      game.home_team.id.toString() === teamId.toString();
                    return (
                      <div
                        key={game.id}
                        className="flex flex-col justify-between"
                      >
                        <p className="text-xs text-gray-500">
                          {gameDay.day} - {formatTime(game.start.toString())} -{" "}
                          {game.get_court_display}
                        </p>
                        <div className="flex items-center space-x-2">
                          <Image
                            src={
                              isHomeGame
                                ? game.away_team.logo
                                : game.home_team.logo
                            }
                            alt={
                              isHomeGame
                                ? game.away_team.name
                                : game.home_team.name
                            }
                            width={30}
                            height={30}
                          />
                          <p className="font-semibold leading-2">
                            {isHomeGame
                              ? "vs " + game.away_team.name
                              : "@ " + game.home_team.name}
                          </p>

                          {game.away_team_num_goals &&
                            game.home_team_num_goals && (
                              <span
                                className={`font-bold text-sm ${
                                  isHomeGame &&
                                  game.home_team_num_goals >
                                    game.away_team_num_goals
                                    ? "text-red-500"
                                    : "text-green-500"
                                }`}
                              >
                                ({game.away_team_num_goals} &ndash;{" "}
                                {game.home_team_num_goals})
                              </span>
                            )}
                        </div>
                      </div>
                    );
                  })}
              </li>
            ))}
          </ScrollArea>
        </ul>
      </CardContent>
    </Card>
  );
}
