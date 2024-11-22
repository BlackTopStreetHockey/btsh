"use client";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
import { Instagram, ArrowLeft } from "lucide-react";

import useImageColor from "@/hooks/useImageColor";
import { getContrastingColor } from "@/lib/utils";

import { useDivisions } from "@/hooks/requests/useDivisions";
import { useSeasons } from "@/hooks/requests/useSeasons";
import { useTeams } from "@/hooks/requests/useTeams";

export default function TeamPage() {
  const { team } = useParams();
  const { data, placeholder, loading, error } = useTeams({
    short_name: team as string,
  });
  const { data: divisions } = useDivisions({});
  const { data: seasons } = useSeasons({});

  const { colors } = useImageColor(data?.logo, {
    colors: 2,
    cors: true,
    format: "hex",
  });

  console.log("colors:", colors);
  console.log("divisions:", divisions);
  console.log("seasons:", seasons);

  return error ? (
    <div>{error.message}</div>
  ) : loading ? (
    placeholder
  ) : (
    data && (
      <div className="container mx-auto p-4">
        <div className="flex mb-4">
          <Link href="/teams" className="text-muted-foreground">
            <span className="flex text-sm gap-2 items-center">
              <ArrowLeft size={24} /> Back to Teams
            </span>
          </Link>
        </div>
        <Card className="max-w-4xl mx-auto">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-3xl font-bold">
                  {data?.name}
                </CardTitle>
                <p className="text-xs text-muted-foreground">
                  {data.established && `Est. ${data.established}`}
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
                priority
              />
            </div>

            <div>
              {data.jersey_colors && (
                <h3 className="text-lg font-semibold mb-2">Team Colors</h3>
              )}
              <div className="flex gap-2">
                {colors &&
                  colors.map((color: string, index: number) => (
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
                {data.jersey_colors &&
                  data.jersey_colors.map((color: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 rounded-full text-sm border"
                      style={{
                        backgroundColor: color,
                        color: getContrastingColor(color),
                      }}
                    >
                      {!color.startsWith("#") ? (
                        <span
                          style={{
                            filter: "invert(1)",
                            mixBlendMode: "difference",
                          }}
                        >
                          {color}
                        </span>
                      ) : (
                        color
                      )}
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
