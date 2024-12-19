"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

import { Scoreboard } from "@/components/scoreboard";
import { BoxScore } from "@/components/box-score";
import { Timer } from "@/components/timer";
import GameDetails from "@/components/game-details";
import { teams } from "@/data/teams";
import { mockPlayers } from "@/data/__mocks__/players";

type Period = "1st" | "2nd" | "3rd" | "OT" | "SO";

interface Player {
  id: string;
  name: string;
}

type GoalEvent = {
  id: string;
  player: Player;
  time: number;
  period: Period;
};

export default function RefPage() {
  const [homeTeam, setHomeTeam] = useState<Team>(teams[9] as Team);
  const [awayTeam, setAwayTeam] = useState<Team>(teams[10] as Team);
  const [court, setCourt] = useState<string>("");
  const [goalEvents, setGoalEvents] = useState<GoalEvent[]>([]);
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [totalSeconds, setTotalSeconds] = useState(25 * 60); // 25 minutes
  const [timeLeft, setTimeLeft] = useState(totalSeconds);
  const [period, setPeriod] = useState<Period>("1st");
  const [isActive, setIsActive] = useState(false);
  const [isTimeout, setIsTimeout] = useState(false);
  const [stringRef, setStringRef] = useState<string>("");
  const [fenceRef, setFenceRef] = useState<string>("");

  const resetTimeouts = () => {
    // Implementation of resetTimeouts
  };

  const handleTimeout = () => {
    setIsTimeout(true);
    setIsActive(false);
  };

  return (
    <>
      <main className="flex-1 overflow-auto p-4">
        <div className="grid gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Scoresheet</CardTitle>
            </CardHeader>
            <CardContent>
              <Scoreboard
                homeTeam={homeTeam}
                awayTeam={awayTeam}
                goalEvents={goalEvents}
                setGoalEvents={setGoalEvents}
                players={mockPlayers}
                totalSeconds={totalSeconds}
                timeLeft={timeLeft}
                period={period}
                onTimeout={handleTimeout}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle>Timer</CardTitle>
            </CardHeader>
            <CardContent>
              <Timer
                resetTimeouts={resetTimeouts}
                totalSeconds={totalSeconds}
                setTotalSeconds={setTotalSeconds}
                timeLeft={timeLeft}
                setTimeLeft={setTimeLeft}
                period={period}
                setPeriod={setPeriod}
                isActive={isActive}
                setIsActive={setIsActive}
                isTimeout={isTimeout}
              />
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-4 mt-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle>Box Score</CardTitle>
              <div className="flex flex-row justify-between">
                <GameDetails
                  date={date}
                  setDate={(newDate: Date) => setDate(newDate)}
                  setCourt={(court: string) => setCourt(court)}
                  setHomeTeam={(team: Team) => setHomeTeam(team)}
                  setAwayTeam={(team: Team) => setAwayTeam(team)}
                  setStringRef={(ref: string) => setStringRef(ref)}
                  setFenceRef={(ref: string) => setFenceRef(ref)}
                  stringRef={stringRef}
                  fenceRef={fenceRef}
                />
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4 mb-4">
                <div className="flex flex-col w-1/2">
                  <div className="font-bold text-sm">Date</div>
                  <div className="text-gray-500">
                    {date?.toLocaleDateString()}
                  </div>

                  <Separator className="my-2" />

                  <div className="font-bold text-sm">Court</div>
                  <div className="text-gray-500">{court}</div>
                </div>

                <div className="flex flex-col w-1/2">
                  <div className="font-bold text-sm">String Ref</div>
                  <div className="text-gray-500">{stringRef}</div>

                  <Separator className="my-2" />

                  <div className="font-bold text-sm">Fence Ref</div>
                  <div className="text-gray-500">{fenceRef}</div>
                </div>
              </div>
              <BoxScore
                goalEvents={goalEvents}
                homeTeam={homeTeam}
                awayTeam={awayTeam}
              />
              <Button
                onClick={() => {
                  // TODO: Implement sending to Box Scores
                }}
              >
                Send to Box Scores &rarr;
              </Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </>
  );
}
