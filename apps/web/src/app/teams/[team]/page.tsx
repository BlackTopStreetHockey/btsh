"use client";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
import { Instagram } from "lucide-react";

import { getContrastingColor } from "@/lib/utils";
import { useTeams } from "@/requests/hooks/useTeams";

export default function TeamPage() {
  const { team } = useParams();
  const { data, placeholder, loading, error } = useTeams({
    short_name: team as string,
  });

  return error ? (
    <div>{error.message}</div>
  ) : loading ? (
    placeholder
  ) : (
    data && (
      <div className="container mx-auto p-4">
        <Card className="max-w-4xl mx-auto">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-3xl font-bold">
                  {data?.name}
                </CardTitle>
                <p className="text-muted-foreground">
                  {data.short_name} • Est. {data.established}
                </p>
              </div>
              {data.instagram_url && (
                <Link
                  href={data.instagram_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-blue-500"
                >
                  <Instagram size={24} />
                </Link>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="relative w-full h-24">
              <Image
                src={data.logo}
                alt={`${data.name} logo`}
                fill
                className="object-contain"
              />
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Team Colors</h3>
              <div className="flex gap-2">
                {data.jersey_colors?.map((color: string, index: number) => (
                  <span
                    key={index}
                    className="px-3 py-1 rounded-full text-sm border"
                    style={{
                      backgroundColor: color,
                      color: getContrastingColor(color),
                    }}
                  >
                    {color}
                  </span>
                ))}
              </div>
            </div>

            {data.description && (
              <div>
                <h3 className="text-lg font-semibold mb-2">History</h3>
                <p className="text-muted-foreground">{data.description}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    )
  );
}
