"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
import { Heart, Diamond, Club, Spade } from "lucide-react";

import { useTeams } from "@/hooks/requests/useTeams";
import { useSeasons } from "@/hooks/requests/useSeasons";
import { useDivisions } from "@/hooks/requests/useDivisions";

import { useSeasonStore } from "@/stores/season-store";

export default function TeamsPage() {
  const { data: teamsData } = useTeams();
  const { data: seasonsData } = useSeasons();
  const { data: divisionsData } = useDivisions();
  const { selectedSeasonId } = useSeasonStore();

  // Get current season
  const currentSeason = seasonsData?.results.find(
    (season: Season) => season.id == selectedSeasonId,
  );

  const cardSymbols = [
    <Spade className="w-4 h-4" />,
    <Club className="w-4 h-4" />,
    <Diamond className="w-4 h-4" />,
    <Heart className="w-4 h-4" />,
  ];

  // Group teams by division
  const teamsByDivision = divisionsData?.results.reduce(
    (
      acc: Record<number, { division: Division; teams: Team[] }>,
      division: Division,
    ) => {
      acc[division.id] = {
        division,
        teams:
          teamsData?.results.filter((team: Team) => {
            const teamRegistration = team.seasons?.find(
              (reg) => reg.season.id === currentSeason?.id,
            );
            return teamRegistration?.division.id === division.id;
          }) || [],
      };
      return acc;
    },
    {} as Record<number, { division: Division; teams: Team[] }>,
  );

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">
        {currentSeason?.year} Teams
      </h1>

      <div className="space-y-8">
        {teamsByDivision &&
          Object.values(teamsByDivision).map(
            (divisionGroup: { division: Division; teams: Team[] }) =>
              divisionGroup.teams.length > 0 && (
                <div key={divisionGroup.division.id}>
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex gap-2">
                        {divisionGroup.division.name}{" "}
                        {cardSymbols[divisionGroup.division.id - 1]}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {divisionGroup.teams.map((team) => (
                          <Link
                            href={`/teams/${team.short_name}`}
                            key={team.id}
                            className="transition-transform hover:scale-105"
                          >
                            <Card>
                              <CardHeader>
                                <CardTitle className="text-lg">
                                  {team.name}
                                </CardTitle>
                              </CardHeader>
                              <CardContent>
                                <div className="flex gap-4">
                                  <Image
                                    src={team.logo}
                                    alt={team.name}
                                    width={100}
                                    height={100}
                                    className="object-contain"
                                  />
                                  <div className="flex flex-col justify-center gap-2">
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
                    </CardContent>
                  </Card>
                </div>
              ),
          )}
      </div>
    </div>
  );
}
