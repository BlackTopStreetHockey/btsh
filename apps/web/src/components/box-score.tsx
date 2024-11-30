"use client";

import Image from "next/image";
import { formatSeconds } from "@/lib/dates";
type Period = "1st" | "2nd" | "3rd" | "OT" | "SO";

type Player = {
  id: string;
  name: string;
  team: string;
};

type GoalEvent = {
  id: string;
  player: Player;
  time: number;
  period: Period;
};

export function BoxScore({
  goalEvents,
  homeTeam,
  awayTeam,
}: {
  goalEvents: GoalEvent[];
  homeTeam: Team;
  awayTeam: Team;
}) {
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="w-full max-w-md">
        <ol className="relative border-s border-gray-200 dark:border-gray-700">
          {goalEvents.map((event, index) => (
            <li key={`goal-${index}`} className="mb-10 ms-6">
              <span className="absolute flex items-center justify-center w-6 h-6 bg-blue-100 border-2 border-gray-200 rounded-full -start-3 ring-8 ring-white dark:ring-gray-900 dark:bg-blue-900">
                <Image
                  width={24}
                  height={24}
                  className="rounded-full shadow-lg"
                  src={event.player.team === homeTeam.name ? homeTeam.logoUrl || "" : awayTeam.logoUrl || ""}
                  alt="Event Team"
                />
              </span>
              <div className="items-center justify-between p-4 bg-white border border-gray-200 rounded-lg shadow-sm sm:flex dark:bg-gray-700 dark:border-gray-600">
                <time className="mb-1 text-xs font-normal text-gray-400 sm:order-last sm:mb-0">
                  {formatSeconds(event.time)} - {event.period}
                </time>
                <div className="text-sm font-normal text-gray-500 dark:text-gray-300">
                  <span className="font-semibold text-blue-600 dark:text-blue-500">
                    {event.player.team === homeTeam.name
                      ? homeTeam.name
                      : awayTeam.name}
                  </span>{" "}
                  goal scored by{" "}
                  <span className="font-semibold text-blue-600 dark:text-blue-500">
                    {event.player.name}
                  </span>
                </div>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
