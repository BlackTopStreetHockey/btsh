"use client";

import Link from "next/link";
import TeamName from "../teams/team-name";
import { Card } from "../ui/card";
import { formatTime } from "@/lib/dates";
import clsx from "clsx";

export default function GameBoxscore({ game }: { game: Game }) {
  const startTime = formatTime(game.start.toString());
  return (
    <div>
      <Link href={`/games/${game.id}`} className='block rounded-md shadow-sm border w-80'>
        <div className="flex flex-row gap-3 p-1">
          <div>
            <div className="text-sm text-gray-400">{startTime}</div>
            <div className='text-gray-400 text-sm'>{game.get_court_display}</div>
          </div>

          <div className="flex flex-col gap-1 flex-grow">
            <div className='flex flex-row gap-2 justify-between items-center'>
              <div className={clsx('', { "font-bold": game.winning_team_id == game.away_team.id })}>
                <TeamName team={game.away_team} link={false} />
              </div>
              <div className={clsx('text-sm text-400', { "font-bold": game.winning_team_id == game.away_team.id, 'text-gray-400': game.losing_team_id == game.away_team.id })}>
                {game.away_team_num_goals}
              </div>
            </div>
            <div className='flex flex-row gap-2 justify-between items-center'>
              <div className={clsx('', { "font-bold": game.winning_team_id == game.home_team.id })}>
                <TeamName team={game.home_team} link={false} />
              </div>
              <div className={clsx('text-sm text-400', { "font-bold": game.winning_team_id == game.home_team.id, 'text-gray-400': game.losing_team_id == game.home_team.id })}>
                {game.home_team_num_goals}
              </div>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
}
