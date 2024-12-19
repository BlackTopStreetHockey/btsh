import formatDateNoTimezone from "@/lib/dates";
import Game from "./game";
import { GAME_COURTS } from "@/constants/games";
import Link from "next/link";
import { Card } from "@/components/ui/card";

export default function GameDay({ gameDay }: { gameDay: GameDay }) {
  const eastGames = gameDay.games.filter((g) => g.court === GAME_COURTS.east);
  const westGames = gameDay.games.filter((g) => g.court === GAME_COURTS.west);
  const gameSets = [
    { label: "West", games: westGames },
    { label: "East", games: eastGames },
  ];
  return (
    <Card className="p-4 border mb-4 bg-white">
      <div className="text-lg font-bold">
        {formatDateNoTimezone(gameDay.day, "eeee, MMMM do y")}
      </div>
      <div className="text-gray-600">
        <div className="flex flex-row justify-center">
          <div className="flex flex-col items-start">
            <div className="flex flex-row gap-2">
              <div className="font-bold text-sm">Opening Team</div>
              <Link href={`/teams/${gameDay.opening_team.short_name}`}>
                <div className="text-sm">{gameDay.opening_team.name}</div>
              </Link>
            </div>
            <div className="flex flex-row gap-2">
              <div className="font-bold text-sm">Closing Team</div>
              <Link href={`/teams/${gameDay.closing_team.short_name}`}>
                <div className="text-sm">{gameDay.closing_team.name}</div>
              </Link>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-2">
          {gameSets.map(({ label, games }) => (
            <div key={label} className="flex flex-col items-center">
              <div className="font-bold text-sm">{label}</div>
              <div className="flex flex-col gap-1">
                {games.map((g) => (
                  <Game key={g.id} game={g} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
