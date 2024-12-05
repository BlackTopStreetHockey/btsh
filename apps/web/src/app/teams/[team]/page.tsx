"use client";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { useDivisions } from "@/hooks/requests/useDivisions";
import { useSeasons } from "@/hooks/requests/useSeasons";
import { useTeam } from "@/hooks/requests/useTeam";
import { useRoster } from "@/hooks/requests/useRoster";

import { TeamInfo } from "./components/team-info";
import { TeamRoster } from "./components/team-roster";
import { TeamSchedule } from "./components/team-schedule";
import { TeamPerformance } from "./components/team-performance";

export default function TeamPage() {
  const { team } = useParams();
  const { data, placeholder, loading, error } = useTeam({
    short_name: team as string,
  });
  const { data: divisions } = useDivisions({});
  const { data: seasons } = useSeasons({});

  console.log("data:", data);
  console.log("divisions:", divisions);
  console.log("seasons:", seasons);

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
                <TeamRoster team={data.name} data={data} />
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
