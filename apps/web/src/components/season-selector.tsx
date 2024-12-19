"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useSeasons } from "@/hooks/requests/useSeasons";
import { useSeasonStore } from "@/stores/season-store";
import { useEffect } from "react";

export function SeasonSelector() {
  const { data: seasonsData } = useSeasons();
  const { selectedSeasonId, setSelectedSeason } = useSeasonStore();

  // Set current season on initial load if none selected
  useEffect(() => {
    if (!selectedSeasonId && seasonsData?.results) {
      const currentSeason = seasonsData.results.find(
        (season: Season) => season.is_current,
      );
      if (currentSeason) {
        setSelectedSeason(currentSeason.id);
      }
    }
  }, [seasonsData, selectedSeasonId, setSelectedSeason]);

  return (
    <div className="group-data-[collapsible=icon]:hidden">
      <Select
        value={selectedSeasonId?.toString()}
        onValueChange={(value) => setSelectedSeason(parseInt(value))}
      >
        <SelectTrigger className="w-[80px]">
          <SelectValue placeholder="Select Season" />
        </SelectTrigger>
        <SelectContent>
          {seasonsData?.results
            .sort((a: Season, b: Season) => b.year - a.year)
            .map((season: Season) => (
              <SelectItem key={season.id} value={season.id.toString()}>
                {season.year}
              </SelectItem>
            ))}
        </SelectContent>
      </Select>
    </div>
  );
}
