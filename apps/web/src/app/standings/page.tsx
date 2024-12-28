"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SortableTable } from "@/components/ui/sortable-table";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { useTeamSeasonRegistrations } from "@/hooks/requests/useTeamSeasonRegistrations";
import { numberToOrdinal } from "@/lib/utils";
import { useSeasonStore } from "@/stores/season-store";
import { useState } from "react";
import { groupBy } from "lodash";

export default function StandingsPage() {
  const { selectedSeasonId } = useSeasonStore();
  const { teams, placeholder } = useTeamSeasonRegistrations({
    season: selectedSeasonId,
  });
  console.log(teams);
  const [mode, setMode] = useState("overall");

  const columns = [
    {
      id: "team",
      Header: "Team",
      accessor: "team.name",
    },
    {
      id: "division",
      Header: "Division",
      accessor: (d) => numberToOrdinal(d.division.short_name),
    },
    {
      Header: "Wins",
      accessor: "wins",
    },
    {
      Header: "Losses",
      accessor: "losses",
    },
    {
      Header: "Ties",
      accessor: "ties",
    },
    {
      id: "points",
      Header: "Points",
      accessor: "points",
      sort: (a, b) => a.place - b.place,
    },
    {
      Header: "GF",
      accessor: "goals_for",
    },
    {
      Header: "GA",
      accessor: "goals_against",
    },
  ];
  const byDivision = teams?.reduce((acc, team) => {
    if (!acc.find((d) => d.division.id === team.division.id))
      acc.push({ division: team.division, teams: [] });
    acc.find((d) => d.division.id === team.division.id)?.teams.push(team);
    return acc;
  }, []);

  if (!!placeholder) return placeholder;
  return (
    <div className="min-h-screen">
      <main className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>
              <div className="flex flex-row justify-between">
                <h1 className="text-3xl font-bold mb-4">BTSH Standings</h1>
                <div>
                  <ToggleGroup
                    type="single"
                    value={mode}
                    onValueChange={setMode}
                  >
                    <ToggleGroupItem value="overall">Overall</ToggleGroupItem>
                    <ToggleGroupItem value="divisions">
                      Divisions
                    </ToggleGroupItem>
                  </ToggleGroup>
                </div>
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {mode === "overall" ? (
              <SortableTable
                columns={columns}
                data={teams}
                defaultSortBy={[{ id: "points", desc: true }]}
              />
            ) : mode === "divisions" ? (
              <div className="flex flex-col gap-16">
                {byDivision.map((division) => (
                  <div key={division.division.id}>
                    <h2 className="text-lg font-bold mb-4">
                      {division.division.name}
                    </h2>
                    <SortableTable
                      columns={columns.filter((c) => c.id !== "division")}
                      data={division.teams}
                      defaultSortBy={[{ id: "points", desc: true }]}
                    />
                  </div>
                ))}
              </div>
            ) : null}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
