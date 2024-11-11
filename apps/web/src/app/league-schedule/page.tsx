"use client";

import GameDay from "@/components/schedule/game-day";
import { useSeasonSelect } from "@/components/schedule/useSeasonSelect";
import { Button } from "@/components/ui/button";
import { useDropdownMenu } from "@/components/ui/hooks/useDropdownMenu";
import { useSelect } from "@/components/ui/hooks/useSelect";
import { useGameDays } from "@/requests/hooks/useGameDays";

export default function Schedule() {
  const { select, selectedValue } = useSeasonSelect({ defaultActive: true });
  const { data, placeholder } = useGameDays({ season: selectedValue });


  return (
    <div>
      <div className="container p-2">
        <h1 className="text-3xl font-bold mb-6 text-center">BTSH Schedule</h1>
      </div>
      
      <div className="container mx-auto p-2 text-center">
        {select}
      </div>

      <div className="container mx-auto p-4 text-center">
        {!!placeholder ? placeholder
        : data?.results.map((r) => (
          <GameDay key={r.id} gameDay={r} />
        ))}
      </div>
    </div>
  );
}