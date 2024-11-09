"use client";

import Link from "next/link"


export default function Game({ game }) {
  return (
    <div key={game.id} className='flex flex-row gap-2'>
      <Link href={`/teams/${game.home_team.id}`} className='text-sm'>{game.home_team.name}</Link>
      <div className='text-sm'>vs</div>
      <Link href={`/teams/${game.away_team.id}`} className='text-sm'>{game.away_team.name}</Link>
    </div>
  );
}