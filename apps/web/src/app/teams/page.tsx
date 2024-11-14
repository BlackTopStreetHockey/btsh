"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
import { useTeams } from "@/requests/hooks/useTeams";

export default function SchedulePage() {
  const { data, placeholder, error } = useTeams({});

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Hockey League Teams</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {data?.results.map((team: Team) => (
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
