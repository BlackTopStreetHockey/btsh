import Image from "next/image";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { Instagram } from "lucide-react";
import { getContrastingColor } from "@/lib/utils";

export function TeamInfo({ team }: { team: Team }) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center space-x-6">
          <Image
            src={team.logo}
            alt={team.name}
            width={120}
            height={120}
            className="rounded-full"
          />
          <div>
            <h1 className="text-3xl font-bold text-gray-800">{team.name}</h1>
            <p className="text-xl text-gray-600">
              Season Record: {team.record || "0-0-0"}
            </p>
            <p className="text-gray-600">
              Conference: {team.conference || "N/A"} | Division:{" "}
              {team.division || "N/A"}
            </p>
          </div>
          <div className="flex-1">
            <p className="text-xs text-muted-foreground">
              {team.established && `Est. ${team.established}`}
            </p>

            {team.description && (
              <div>
                <h3 className="text-lg font-semibold mb-2">History</h3>
                <p className="text-muted-foreground">{team.description}</p>
              </div>
            )}
            {team.instagram_url && (
              <Link
                href={team.instagram_url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-blue-500"
              >
                <Instagram size={24} />
              </Link>
            )}
          </div>
          <div>
            {team.jersey_colors && (
              <h3 className="text-lg font-semibold mb-2">Team Colors</h3>
            )}
            <div className="flex gap-2">
              {team.jersey_colors?.map((color: string, index: number) => (
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
        </div>
      </CardContent>
    </Card>
  );
}
