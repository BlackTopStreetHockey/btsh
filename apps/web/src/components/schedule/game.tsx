"use client";

import Link from "next/link"
import TeamLink from "../teams/team-link";
import formatDateNoTimezone from "@/lib/dates";


export default function Game({ game }: { game: Game }) {
  const startTime = game.start.toString().split(':').slice(0, 2).join(':')
  return (
    <div key={game.id} className='flex flex-row gap-2'>
      <div className='text-sm'>{startTime}</div>
      <TeamLink team={game.home_team} />
      <div className='text-sm'>vs</div>
      <TeamLink team={game.away_team} />
    </div>
  );
}