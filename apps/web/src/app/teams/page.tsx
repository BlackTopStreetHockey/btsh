"use client";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { useTeams } from "@/hooks/requests/useTeams";
import { useSeasons } from "@/hooks/requests/useSeasons";
import { useDivisions } from "@/hooks/requests/useDivisions";
export default function SchedulePage() {
  const { teams, placeholder, error } = useTeams();
  const { seasons } = useSeasons({});
  const { divisions } = useDivisions({});

  const [seasonId, setSeasonId] = useState<string>("");
  // // Get the current season ID from URL params or use the current season
  const currentSeason = seasons?.find((season: Season) => season.is_current);
  const handleSeasonChange = (newSeasonId: string) => {
    setSeasonId(newSeasonId);
  };
  console.log("currentSeason:", currentSeason);
  console.log("teams:", teams);
  console.log("seasons:", seasons);
  console.log("divisions:", divisions);

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold mb-6">Teams</h1>
        <div className="w-32">
          <Select value={seasonId} onValueChange={handleSeasonChange}>
            <SelectTrigger>
              <SelectValue placeholder="Select Season" />
            </SelectTrigger>
            <SelectContent>
              {seasons?.sort((a, b) => b.year - a.year).map(
                (season: { id: number; year: string; is_current: boolean }) => (
                  <SelectItem key={season.id} value={season.id.toString()}>
                    {season.year}
                  </SelectItem>
                ),
              )}
            </SelectContent>
          </Select>
        </div>
      </div>

      {divisions?.map((division: Division) => (
        <Card key={division.id} className="mb-4">
          <CardHeader>
            <CardTitle>{division.name}</CardTitle>
          </CardHeader>
        </Card>
      ))}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {teams?.map((team: Team) => (
          <Link href={`/teams/${team.short_name}`} key={team.id}>
            <Card key={team.id}>
              <CardHeader>
                <CardTitle>{team.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4">
                  <Image
                    src={team.logo}
                    alt={team.name}
                    width={100}
                    height={100}
                  />
                  <div className="flex flex-col justify-center gap-4">
                    {team.jersey_colors?.map((color) => (
                      <div
                        key={color}
                        className="w-8 h-8 rounded-full border"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
