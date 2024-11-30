"use client";

import { useGameDays } from "@/requests/hooks";
import { useSeasonSelect } from "./useSeasonSelect";
import formatDateNoTimezone, { formatTime, timeToHours } from "@/lib/dates";
import { useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

interface GameTimeSlot {
  start: string;
  east: Game;
  west: Game;
}

export default function ScheduleCarousel() {
  const ref = useRef(null);
  const { selectedSeason } = useSeasonSelect({ defaultActive: true });
  const { data } = useGameDays({ season: selectedSeason?.id });
  console.log(data);
  const handleScroll = () => {
    if (ref.current) {
      ref.current.scroll += 100;
    }
  };

  const getGamesByTime = (games: Game[]) => {
    return games
      .reduce((acc: any, game: Game) => {
        let slot = acc.find((a: any) => a.start === game.start);
        if (!slot) {
          slot = { start: game.start };
          acc.push(slot);
        }
        slot[game.court] = game;
        return acc;
      }, [])
      .sort(
        (a: GameTimeSlot, b: GameTimeSlot) =>
          timeToHours(a.start) - timeToHours(b.start)
      );
  };

  return (
    <div>
      <ScrollArea className="w-full h-36">
        <div ref={ref} className="flex flex-row gap-1 overflow-x-hidden">
          {data?.results.map((gameDay: GameDay) => {
            const gamesByTime = getGamesByTime(gameDay.games);
            console.log(gamesByTime);
            return (
              <div key={gameDay.id} className="flex flex-row rounded border shadow">
                <div className="border h-32 flex flex-col justify-center">
                  <div className="text-xs font-bold text-center w-16">
                    <div>{formatDateNoTimezone(gameDay.day, "MMM do")}</div>
                    <div>{formatDateNoTimezone(gameDay.day, "y")}</div>
                  </div>
                </div>

                <div className="flex flex-col items-center">
                  <div className="flex-grow text-xs text-gray-400 text-center [writing-mode:vertical-lr] rotate-180">
                    EAST
                  </div>
                  <div className="flex-grow text-xs text-gray-400 text-center [writing-mode:vertical-lr] rotate-180">
                    WEST
                  </div>
                </div>
                {gamesByTime.map((timeSlot: GameTimeSlot) => (
                  <div key={timeSlot.start} className="w-8">
                    <div className="text-xs text-center">
                      {formatTime(timeSlot.start, false)}
                    </div>
                    <div className="flex flex-col gap-1">
                      {[timeSlot.east, timeSlot.west].map((game: Game, i) => (
                        <div
                          key={game.id}
                          className={`w-8 pb-1 ${i === 0 ? "border-b" : ""}`}
                        >
                          <Link
                            href={`/games/${game.id}`}
                            className="flex flex-col justify-center items-center rounded hover:shadow-inner-lg cursor-pointer"
                          >
                            <Image
                              className="rounded"
                              src={game.away_team.logo}
                              alt={game.away_team.short_name}
                              width={24}
                              height={24}
                            />
                            <Image
                              className="rounded"
                              src={game.home_team.logo}
                              alt={game.home_team.short_name}
                              width={24}
                              height={24}
                            />
                          </Link>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
      <button onClick={() => handleScroll()}>Click</button>
    </div>
  );
}
