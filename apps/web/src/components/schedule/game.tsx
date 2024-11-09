"use client";

import Link from "next/link"
import TeamName from "../teams/team-name";
import formatDateNoTimezone from "@/lib/dates";


export default function Game({ game }: { game: Game }) {
  const startTime = game.start.toString().split(':').slice(0, 2).join(':')
  return (
    <div key={game.id} className='flex flex-row gap-2'>
      <div className='text-sm'>{startTime}</div>
      <TeamName team={game.home_team} />
      <div className='text-sm'>vs</div>
      <TeamName team={game.away_team} />
    </div>
  );
}