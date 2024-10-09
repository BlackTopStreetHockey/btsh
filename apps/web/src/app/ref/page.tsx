"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, Plus, X } from 'lucide-react';

export default function GameScoringInterface({ game, onScoreUpdate }) {
  const [selectedPeriod, setSelectedPeriod] = useState(1);
  const [showScoringModal, setShowScoringModal] = useState(false);
  const [scoringDetails, setScoringDetails] = useState({
    scorerId: '',
    assists: [],
    timeInPeriod: '',
  });

  const handleAddGoal = async () => {
    try {
      const response = await fetch(`/api/games/${game.id}/goals`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...scoringDetails,
          periodId: selectedPeriod,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to add goal');
      }

      setShowScoringModal(false);
      setScoringDetails({ scorerId: '', assists: [], timeInPeriod: '' });
      onScoreUpdate();
    } catch (error) {
      console.error('Error adding goal:', error);
    }
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Game Score</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between items-center text-2xl font-bold">
            <div>{game?.homeTeam.name}</div>
            <div className="flex items-center gap-8">
              <span>{game?.homeScore}</span>
              <span>-</span>
              <span>{game?.awayScore}</span>
            </div>
            <div>{game?.awayTeam.name}</div>
          </div>

          <div className="mt-4 flex justify-center gap-2">
            {[1, 2, 3].map((period) => (
              <Button
                key={period}
                variant={selectedPeriod === period ? "default" : "outline"}
                onClick={() => setSelectedPeriod(period)}
              >
                Period {period}
              </Button>
            ))}
          </div>

          <div className="mt-6">
            <Button
              onClick={() => setShowScoringModal(true)}
              className="w-full flex items-center justify-center gap-2"
            >
              <Plus className="h-4 w-4" />
              Add Goal
            </Button>
          </div>
        </CardContent>
      </Card>

      {showScoringModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Add Goal</CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowScoringModal(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </CardHeader>
            <CardContent>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">
                    Scorer
                  </label>
                  <select
                    className="w-full p-2 border rounded-md"
                    value={scoringDetails.scorerId}
                    onChange={(e) => setScoringDetails(prev => ({
                      ...prev,
                      scorerId: e.target.value
                    }))}
                  >
                    <option value="">Select player</option>
                    {[...game?.homeTeam.players, ...game?.awayTeam.players].map((player) => (
                      <option key={player.id} value={player.id}>
                        {player.firstName} {player.lastName} (#{player.number})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    Time in Period
                  </label>
                  <input
                    type="text"
                    placeholder="MM:SS"
                    className="w-full p-2 border rounded-md"
                    value={scoringDetails.timeInPeriod}
                    onChange={(e) => setScoringDetails(prev => ({
                      ...prev,
                      timeInPeriod: e.target.value
                    }))}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    Assists (max 2)
                  </label>
                  {[0, 1].map((index) => (
                    <select
                      key={index}
                      className="w-full p-2 border rounded-md mb-2"
                      value={scoringDetails.assists[index] || ''}
                      onChange={(e) => {
                        const newAssists = [...scoringDetails.assists];
                        newAssists[index] = e.target.value;
                        setScoringDetails(prev => ({
                          ...prev,
                          assists: newAssists
                        }));
                      }}
                    >
                      <option value="">Select player</option>
                      {[...game.homeTeam.players, ...game.awayTeam.players].map((player) => (
                        <option key={player.id} value={player.id}>
                          {player.firstName} {player.lastName} (#{player.number})
                        </option>
                      ))}
                    </select>
                  ))}
                </div>

                <Button
                  type="button"
                  className="w-full"
                  onClick={handleAddGoal}
                >
                  Save Goal
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}