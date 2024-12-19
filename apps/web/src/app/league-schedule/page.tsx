"use client";

import GameDay from "@/components/schedule/game-day";
import { fetcher } from "@/hooks/requests/fetcher";
import useSWR from "swr";

import { useGameDays } from "@/hooks/requests/useGameDays";
import { useSeasonStore } from "@/stores/season-store";

export default function Schedule() {
  const { selectedSeasonId } = useSeasonStore();
  const { data, placeholder } = useGameDays({ season: selectedSeasonId });
  const currentSeason = useSWR(
    `${process.env.NEXT_PUBLIC_API_URL}/api/seasons/${selectedSeasonId}`,
    fetcher,
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container p-2">
        <h1 className="text-3xl font-bold mb-6 text-center">
          {currentSeason?.data?.year} BTSH Schedule
        </h1>
      </div>

      <div className="container mx-auto p-4 text-center">
        {!!placeholder
          ? placeholder
          : data?.results.map((r) => <GameDay key={r.id} gameDay={r} />)}
      </div>
    </div>
  );
}
