"use client";

import GameDay from "@/components/schedule/game-day";
import { Card } from "@/components/ui/card";
import { useRequest, usePlaceholder } from "@/requests/hooks";
import { useMemo } from "react";

export default function Schedule() {
  const season = 4;
  const { data: gameDays, placeholder: daysPlaceholder } = usePlaceholder(useRequest({ 
    route: 'game_days', 
    params: {
      season
    }
  }));

  // const { data: games, placeholder: gamesPlaceholder } = usePlaceholder(useRequest({ 
  //   route: 'games', 
  //   params: {
  //     game_day__season: season
  //   }
  // }));

  // const gameDaysWithGames = useMemo(() =>{
  //   if (!games || !gameDays) return [];
  //   const ret = {};
  //   games.results.forEach(g => {
  //     if (!ret[g.gameDay.id]) ret[g.gameDay.id] = {gameDay: }
  //   })
  // }, [games, gameDays]);
  console.log(gameDays)

  return (
    <div>
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6 text-center">BTSH Schedule</h1>
      </div>
      
      <div className="container mx-auto p-4 text-center">
        {!!daysPlaceholder ? daysPlaceholder
        // : gamesPlaceholder ? gamesPlaceholder
        : gameDays.results.map((r) => (
          <GameDay key={r.id} gameDay={r} />
        ))}
      </div>
    </div>
  );
}