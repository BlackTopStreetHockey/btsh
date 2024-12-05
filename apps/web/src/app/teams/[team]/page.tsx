"use client";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { useTeam } from "@/hooks/requests/useTeam";

import { TeamInfo } from "./components/team-info";
import { TeamRoster } from "./components/team-roster";
import { TeamSchedule } from "./components/team-schedule";
import { TeamPerformance } from "./components/team-performance";

export default function TeamPage() {
  const { team } = useParams();
  // const searchParams = useSearchParams();
  const { data, placeholder, loading, error } = useTeam({
    short_name: team as string,
  });
  // const { data: divisions } = useDivisions({});
  // const { data: seasons } = useSeasons({});

  // // Get the current season ID from URL params or use the current season
  // const currentSeason = seasons?.results.find(season => season.is_current);
  // const seasonId = searchParams.get('season') || currentSeason?.id.toString() || "1";

  console.log("data:", data);
  // console.log("divisions:", divisions);
  // console.log("seasons:", seasons);

  return error ? (
    <div>{error.message}</div>
  ) : loading ? (
    placeholder
  ) : (
    data && (
      <main>
        <div className="container mx-auto p-4">
          <div className="flex mb-4">
            <Link href="/teams" className="text-muted-foreground">
              <span className="flex text-sm gap-2 items-center">
                <ArrowLeft size={24} /> Back to Teams
              </span>
            </Link>
          </div>
          <div className="grid gap-4">
            <TeamInfo team={data} />

            <div className="grid gap-4 md:grid-cols-3">
              <div className="md:col-span-2">
                <TeamRoster teamId={data.id} />
              </div>
              <div>
                <TeamSchedule />
              </div>
            </div>
            <TeamPerformance />
          </div>
        </div>
      </main>
    )
  );
}
