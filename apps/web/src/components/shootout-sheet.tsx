import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { CheckCircle, XCircle, Undo2 } from "lucide-react";

type ShootoutAttempt = {
  player: string;
  successful: boolean;
};

type ShootoutSheetProps = {
  homeTeam: Team;
  awayTeam: Team;
};

export function ShootoutSheet({ homeTeam, awayTeam }: ShootoutSheetProps) {
  const [homeAttempts, setHomeAttempts] = useState<ShootoutAttempt[]>([]);
  const [awayAttempts, setAwayAttempts] = useState<ShootoutAttempt[]>([]);

  const addAttempt = (team: 'home' | 'away', successful: boolean) => {
    const newAttempt: ShootoutAttempt = {
      player: `Player ${team === 'home' ? homeAttempts.length + 1 : awayAttempts.length + 1}`,
      successful,
    };

    if (team === 'home') {
      setHomeAttempts([...homeAttempts, newAttempt]);
    } else {
      setAwayAttempts([...awayAttempts, newAttempt]);
    }
  };

  const removeLastAttempt = (team: 'home' | 'away') => {
    if (team === 'home' && homeAttempts.length > 0) {
      setHomeAttempts(homeAttempts.slice(0, -1));
    } else if (team === 'away' && awayAttempts.length > 0) {
      setAwayAttempts(awayAttempts.slice(0, -1));
    }
  };

  const renderAttempts = (attempts: ShootoutAttempt[]) => {
    return attempts.map((attempt, index) => (
      <div key={index} className="flex items-center space-x-2">
        <span>{attempt.player}</span>
        {attempt.successful ? (
          <CheckCircle className="text-green-500" />
        ) : (
          <XCircle className="text-red-500" />
        )}
      </div>
    ));
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h4 className="font-bold mb-2">{homeTeam.name}</h4>
          {renderAttempts(homeAttempts)}
          <div className="mt-2 space-x-2">
            <Button size="sm" onClick={() => addAttempt('home', true)}>Goal</Button>
            <Button size="sm" variant="outline" onClick={() => addAttempt('home', false)}>Miss</Button>
            <Button size="sm" variant="ghost" onClick={() => removeLastAttempt('home')} disabled={homeAttempts.length === 0}>
              <Undo2 className="h-4 w-4 mr-1" />
              Undo
            </Button>
          </div>
        </div>
        <div>
          <h4 className="font-bold mb-2">{awayTeam.name}</h4>
          {renderAttempts(awayAttempts)}
          <div className="mt-2 space-x-2">
            <Button size="sm" onClick={() => addAttempt('away', true)}>Goal</Button>
            <Button size="sm" variant="outline" onClick={() => addAttempt('away', false)}>Miss</Button>
            <Button size="sm" variant="ghost" onClick={() => removeLastAttempt('away')} disabled={awayAttempts.length === 0}>
              <Undo2 className="h-4 w-4 mr-1" />
              Undo
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
