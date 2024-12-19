"use client";

import GameDay from "@/components/schedule/game-day";

import { useGameDays } from "@/hooks/requests/useGameDays";
import { useSeasonStore } from "@/stores/season-store";

export default function Schedule() {
  const { selectedSeasonId } = useSeasonStore();
  const { data, placeholder } = useGameDays({ season: selectedSeasonId });

  return (
    <div>
      <div className="container p-2">
        <h1 className="text-3xl font-bold mb-6 text-center">BTSH Schedule</h1>
      </div>

      <div className="container mx-auto p-4 text-center">
        {!!placeholder
          ? placeholder
          : data?.results.map((r) => <GameDay key={r.id} gameDay={r} />)}
      </div>
    </div>
  );
}
