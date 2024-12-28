"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useGameGoals } from "@/hooks/requests/useGameGoals";
import { numberToOrdinal } from "@/lib/utils";
import GameGoal from "./GameGoal";

export function GameScoring({ game }: { game: Game }) {
  const { goals, placeholder } = useGameGoals({ gameId: game.id });

  const teamToGoals = goals?.reduce((acc: any, goal: GameGoal) => {
    if (!acc[goal.team.id]) acc[goal.team.id] = [];
    let per = acc[goal.team.id].find((p: any) => p.period == goal.period);
    if (!per) {
      per = { period: goal.period, goals: [] };
      acc[goal.team.id].push(per);
      acc[goal.team.id].sort((a: any, b: any) => a.period - b.period);
    }
    per.goals.push(goal);
    return acc;
  }, {});
  if (!!placeholder) return placeholder;
  return (
    <div className="flex flex-col items-center">
      <div className="flex flex-row gap-8">
        {[game.away_team.id, game.home_team.id].map((teamId) => (
          <div key={teamId} className="bg-white">
            {teamToGoals[teamId]?.map((period: any) => (
              <div
                key={period.period}
                className="flex flex-col gap-1 p-2 bg-white"
              >
                <div className="font-bold text-sm">
                  {numberToOrdinal(period.period)}
                </div>
                {period.goals.map((goal: GameGoal) => (
                  <GameGoal goal={goal} key={goal.id} />
                ))}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
