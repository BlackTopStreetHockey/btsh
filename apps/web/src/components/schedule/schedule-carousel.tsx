"use client";

import { useGameDays } from "@/hooks/requests/useGameDays";
import { useSeasonStore } from "@/stores/season-store";
import formatDateNoTimezone, { formatTime, timeToHours } from "@/lib/dates";
import { useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";

interface GameTimeSlot {
  start: Date;
  east: Game | null;
  west: Game | null;
}

export default function ScheduleCarousel() {
  const viewportRef = useRef<HTMLDivElement>(null);

  const clickHandler = (direction: "left" | "right") => {
    if (viewportRef !== null && viewportRef.current !== null) {
      viewportRef.current.style.scrollBehavior = "smooth";
      viewportRef.current.scrollLeft += direction === "left" ? -250 : 250;
    }
  };

  const { selectedSeasonId } = useSeasonStore();
  const { data } = useGameDays({ season: selectedSeasonId });

  const getGamesByTime = (games: Game[]) => {
    return games
      .reduce((acc: GameTimeSlot[], game: Game) => {
        let slot = acc.find((a: GameTimeSlot) => a.start === game.start);
        if (!slot) {
          slot = {
            start: game.start,
            east: null,
            west: null,
          };
          acc.push(slot);
        }
        slot[game.court] = game;
        return acc;
      }, [])
      .sort(
        (a: GameTimeSlot, b: GameTimeSlot) =>
          timeToHours(a.start) - timeToHours(b.start),
      );
  };

  return (
    <div className="m-1">
      <div className="flex flex-row gap-1">
        <div className="">
          <Button
            variant={"secondary"}
            className="h-full rounded-xl rounded-r"
            onClick={() => clickHandler("left")}
          >
            &larr;
          </Button>
        </div>
        <ScrollArea
          viewportRef={viewportRef}
          className="w-full h-36"
          scrollHideDelay={100}
        >
          <div className="flex flex-row gap-1">
            {data?.results.map((gameDay: GameDay) => {
              const gamesByTime = getGamesByTime(gameDay.games);
              return (
                <div
                  key={gameDay.id}
                  className="flex flex-row rounded-xl border"
                >
                  <div className="h-full border-r flex flex-col justify-center">
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
                    <div key={timeSlot.start.toString()} className="w-8">
                      <div className="text-xs text-center">
                        {formatTime(timeSlot.start, false)}
                      </div>
                      <div className="flex flex-col divide-y">
                        {[timeSlot.east, timeSlot.west].map(
                          (game: Game | null) =>
                            game && (
                              <Link
                                key={game.id}
                                href={`/games/${game.id}`}
                                className="w-8 py-1 flex flex-col gap-1 justify-center items-center cursor-pointer hover:bg-gray-400"
                              >
                                <Image
                                  className="rounded opacity-80"
                                  src={game.away_team.logo}
                                  alt={game.away_team.short_name}
                                  width={24}
                                  height={24}
                                  loading="lazy"
                                />
                                <Image
                                  className="rounded opacity-80"
                                  src={game.home_team.logo}
                                  alt={game.home_team.short_name}
                                  width={24}
                                  height={24}
                                  loading="lazy"
                                />
                              </Link>
                            ),
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
        <div className="">
          <Button
            variant={"secondary"}
            className="h-full rounded-xl rounded-l"
            onClick={() => clickHandler("right")}
          >
            &rarr;
          </Button>
        </div>
      </div>
    </div>
  );
}
