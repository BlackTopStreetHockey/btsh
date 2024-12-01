"use client";

import TeamName from "../teams/team-name";
import { formatTime } from "@/lib/dates";

export default function Game({ game }: { game: Game }) {
  const startTime = formatTime(game.start.toString());

  return (
    <div
      key={game.id}
      className="rounded-md shadow-sm border w-64 flex flex-row p-1 gap-2 mb-2 items-center"
    >
      <div className="text-sm text-gray-400">{startTime}</div>
      <div className="flex flex-col gap-1">
        <TeamName team={game.away_team} link={true} />
        <TeamName team={game.home_team} link={true} />
      </div>
    </div>
  );
}
