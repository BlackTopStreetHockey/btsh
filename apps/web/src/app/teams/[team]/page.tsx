"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { useSeasons } from "@/hooks/requests/useSeasons";
import { useTeam } from "@/hooks/requests/useTeam";

import { TeamInfo } from "./components/team-info";
import { TeamRoster } from "./components/team-roster";
import { TeamSchedule } from "./components/team-schedule";
import { TeamPerformance } from "./components/team-performance";

export default function TeamPage() {
  const { team } = useParams();
  const { seasons } = useSeasons({});
  // const searchParams = useSearchParams();
  const { data, placeholder, loading, error } = useTeam({
    short_name: team as string,
  });
  const [seasonId, setSeasonId] = useState<string>("");
  // // Get the current season ID from URL params or use the current season
  const currentSeason = seasons?.find((season: Season) => season.is_current);
  console.log("currentSeason:", currentSeason);
  const handleSeasonChange = (newSeasonId: string) => {
    setSeasonId(newSeasonId);
  };

  return error ? (
    <div>{error.message}</div>
  ) : loading ? (
    placeholder
  ) : (
    data && (
      <main>
        <div className="container mx-auto p-4">
          <div className="flex justify-between items-center mb-4">
            <Link href="/teams" className="text-muted-foreground">
              <span className="flex text-sm gap-2 items-center">
                <ArrowLeft size={24} /> Back to Teams
              </span>
            </Link>

            <div className="w-32">
              <Select value={seasonId} onValueChange={handleSeasonChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select Season" />
                </SelectTrigger>
                <SelectContent>
                  {seasons?.sort((a, b) => b.year - a.year).map(
                    (season: {
                      id: number;
                      year: string;
                      is_current: boolean;
                    }) => (
                      <SelectItem key={season.id} value={season.id.toString()}>
                        {season.year}
                      </SelectItem>
                    )
                  )}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid gap-4">
            <TeamInfo team={data} />

            <div className="grid gap-4 md:grid-cols-3">
              <div className="md:col-span-2">
                <TeamRoster
                  seasonId={seasonId}
                  teamId={data.id}
                  seasonYear={
                    seasons?.find(
                      (season: Season) => season.id.toString() === seasonId
                    )?.year
                  }
                />
              </div>
              <div>
                <TeamSchedule
                  seasonId={seasonId}
                  teamId={data.id}
                  seasonYear={
                    seasons?.find(
                      (season: Season) => season.id.toString() === seasonId
                    )?.year
                  }
                />
              </div>
            </div>
            <TeamPerformance />
          </div>
        </div>
      </main>
    )
  );
}
