"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Scoreboard } from "@/components/scoreboard";
import { BoxScore } from "@/components/box-score";
import { Timer } from "@/components/timer";
import GameDetails from "@/components/game-details";
import { teams } from "@/data/teams";
import { mockPlayers } from "@/data/__mocks__/players";

type Period = "1st" | "2nd" | "3rd" | "OT" | "SO";
type GoalEvent = {
  id: string;
  player: Player;
  time: number;
  period: Period;
};

export default function RefPage() {
  const [homeTeam, setHomeTeam] = useState<Team>(teams[9]);
  const [awayTeam, setAwayTeam] = useState<Team>(teams[10]);
  const [goalEvents, setGoalEvents] = useState<GoalEvent[]>([]);
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [totalSeconds, setTotalSeconds] = useState(25 * 60); // 25 minutes
  const [timeLeft, setTimeLeft] = useState(totalSeconds);
  const [period, setPeriod] = useState<Period>("1st");
  const [isActive, setIsActive] = useState(false);
  const [isTimeout, setIsTimeout] = useState(false);

  const resetTimeouts = () => {
    // Implementation of resetTimeouts
  };

  const handleTimeout = () => {
    setIsTimeout(true);
    setIsActive(false);
  };

  const endTimeout = () => {
    setIsTimeout(false);
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
                endTimeout={endTimeout}
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
                  setDate={setDate}
                  homeTeam={homeTeam}
                  awayTeam={awayTeam}
                  setHomeTeam={setHomeTeam}
                  setAwayTeam={setAwayTeam}
                />
              </div>
            </CardHeader>
            <CardContent>
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
                Send to Box Scores
              </Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </>
  );
}
