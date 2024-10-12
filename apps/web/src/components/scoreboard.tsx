"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { PlusCircle, MinusCircle, Clock } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Image from "next/image";

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

type ScoreboardProps = {
  homeTeam: Team;
  awayTeam: Team;
  goalEvents: GoalEvent[];
  setGoalEvents: React.Dispatch<React.SetStateAction<GoalEvent[]>>;
  totalSeconds: number;
  timeLeft: number;
  period: Period;
  players: Player[];
  onTimeout: () => void;
};

export function Scoreboard({
  homeTeam,
  awayTeam,
  goalEvents,
  setGoalEvents,
  totalSeconds,
  timeLeft,
  period,
  players,
  onTimeout,
}: ScoreboardProps) {
  const [homeScore, setHomeScore] = useState(0);
  const [awayScore, setAwayScore] = useState(0);
  const [homeTimeouts, setHomeTimeouts] = useState(1);
  const [awayTimeouts, setAwayTimeouts] = useState(1);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);

  const addGoal = (team: Team) => {
    if (selectedPlayer && selectedPlayer.team === team.name) {
      const newGoal: GoalEvent = {
        id: `goal-${goalEvents.length + 1}`,
        player: selectedPlayer,
        time: totalSeconds - timeLeft,
        period: period,
      };
      setGoalEvents([...goalEvents, newGoal]);
      if (team.name === homeTeam.name) {
        setHomeScore((score) => score + 1);
      } else {
        setAwayScore((score) => score + 1);
      }
      setSelectedPlayer(null);
    }
  };

  const removeGoal = (team: Team) => {
    const lastGoal = [...goalEvents]
      .reverse()
      .find((goal) => goal.player.team === team.name);
    if (lastGoal) {
      setGoalEvents(goalEvents.filter((goal) => goal.id !== lastGoal.id));
      if (team.name === homeTeam.name) {
        setHomeScore((score) => Math.max(0, score - 1));
      } else {
        setAwayScore((score) => Math.max(0, score - 1));
      }
    }
  };

  const handleTimeout = (team: Team) => {
    if (team === homeTeam && homeTimeouts > 0) {
      setHomeTimeouts(homeTimeouts - 1);
      onTimeout();
    } else if (team === awayTeam && awayTimeouts > 0) {
      setAwayTimeouts(awayTimeouts - 1);
      onTimeout();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="grid grid-cols-2 gap-2 mb-4 w-full max-w-md">
        <div className="flex flex-col items-center">
          <Image
            className="mb-2 rounded-full"
            src={homeTeam?.logoUrl || "/teams/btsh.jpg"}
            alt={homeTeam?.name || "BTSH"}
            width={48}
            height={48}
          />
          <h3 className="text-sm font-bold">{homeTeam?.name || ""}</h3>
          <div className="rounded-xl border bg-card text-card-foreground shadow m-2 p-2 w-16 text-center">
            <div className="text-4xl font-bold p-2">{homeScore}</div>
          </div>
          <div className="flex space-x-2">
            <Button
              onClick={() => addGoal(homeTeam)}
              size="icon"
              variant="outline"
              disabled={
                !selectedPlayer || selectedPlayer.team !== homeTeam.name
              }
            >
              <PlusCircle className="h-4 w-4" />
            </Button>
            <Button
              onClick={() => removeGoal(homeTeam)}
              size="icon"
              variant="outline"
            >
              <MinusCircle className="h-4 w-4" />
            </Button>
          </div>
          <div className="mt-2 flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>{homeTimeouts}</span>
            <Button
              onClick={() => handleTimeout(homeTeam)}
              size="sm"
              variant="ghost"
              disabled={homeTimeouts === 0}
              className="ml-1"
            >
              Use
            </Button>
          </div>
        </div>

        <div className="flex flex-col items-center">
          <Image
            className="mb-2 rounded-full"
            src={awayTeam?.logoUrl || "/teams/btsh.jpg"}
            alt={awayTeam?.name || "BTSH"}
            width={48}
            height={48}
          />
          <h3 className="text-sm font-bold">{awayTeam?.name || ""}</h3>
          <div className="rounded-xl border bg-card text-card-foreground shadow m-2 p-2 w-16 text-center">
            <div className="text-4xl font-bold p-2">{awayScore}</div>
          </div>
          <div className="flex space-x-2">
            <Button
              onClick={() => addGoal(awayTeam)}
              size="icon"
              variant="outline"
              disabled={
                !selectedPlayer || selectedPlayer.team !== awayTeam.name
              }
            >
              <PlusCircle className="h-4 w-4" />
            </Button>
            <Button
              onClick={() => removeGoal(awayTeam)}
              size="icon"
              variant="outline"
            >
              <MinusCircle className="h-4 w-4" />
            </Button>
          </div>
          <div className="mt-2 flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>{awayTimeouts}</span>
            <Button
              onClick={() => handleTimeout(awayTeam)}
              size="sm"
              variant="ghost"
              disabled={awayTimeouts === 0}
              className="ml-1"
            >
              Use
            </Button>
          </div>
        </div>
      </div>
      <div className="w-full max-w-md mb-4">
        <Select
          onValueChange={(value) =>
            setSelectedPlayer(players.find((p) => p.id === value) || null)
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select player" />
          </SelectTrigger>
          <SelectContent>
            {players
              .filter(
                (player) =>
                  player.team === homeTeam?.name ||
                  player.team === awayTeam?.name
              )
              .map((player) => (
                <SelectItem key={player.id} value={player.id}>
                  {player.name} ({player.team})
                </SelectItem>
              ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
