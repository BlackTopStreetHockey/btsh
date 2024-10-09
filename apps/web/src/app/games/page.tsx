"use client";

import React, { useState, useEffect, useCallback } from 'react';
import { Calendar, Clock, LogOut, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function RefereeDashboard() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Game state
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [ws, setWs] = useState(null);

  // WebSocket connection management
  const connectWebSocket = useCallback(() => {
    const socket = new WebSocket('ws://your-websocket-server/games');

    socket.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'GAME_UPDATE':
          setGames(prevGames => 
            prevGames.map(game => 
              game.id === data.game.id ? { ...game, ...data.game } : game
            )
          );
          break;
        case 'NEW_GAME':
          setGames(prevGames => [...prevGames, data.game]);
          break;
        case 'DELETE_GAME':
          setGames(prevGames => 
            prevGames.filter(game => game.id !== data.gameId)
          );
          break;
      }
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
      setTimeout(connectWebSocket, 5000);
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWs(socket);

    return () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      connectWebSocket();
    }
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [isAuthenticated]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const userData = await response.json();
      setUser(userData);
      setIsAuthenticated(true);
      fetchGames();
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
      setUser(null);
      setIsAuthenticated(false);
      setGames([]);
      if (ws) {
        ws.close();
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const handleUpdateScore = async (gameId, homeScore, awayScore, status) => {
    try {
      const response = await fetch(`/api/games/${gameId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ homeScore, awayScore, status }),
      });
      
      if (response.ok) {
        ws.send(JSON.stringify({
          type: 'SCORE_UPDATE',
          gameId,
          homeScore,
          awayScore,
          status,
        }));
      }
    } catch (error) {
      console.error('Error updating game:', error);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-2xl text-center">Referee Login</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="email" className="block text-sm font-medium">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full p-2 border rounded-md"
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="password" className="block text-sm font-medium">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full p-2 border rounded-md"
                  required
                />
              </div>
              {loginError && (
                <div className="text-red-500 text-sm">{loginError}</div>
              )}
              <Button 
                type="submit" 
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Signing in...
                  </>
                ) : (
                  'Sign In'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Referee Dashboard</h1>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            <span>{new Date().toLocaleDateString()}</span>
          </div>
          <Button variant="outline" onClick={handleLogout} className="flex items-center gap-2">
            <LogOut className="h-4 w-4" />
            Sign Out
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Today's Games</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {games.filter(game => 
                new Date(game.startTime).toDateString() === new Date().toDateString()
              ).length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Games This Week</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {games.filter(game => {
                const gameDate = new Date(game.startTime);
                const today = new Date();
                const weekFromNow = new Date();
                weekFromNow.setDate(today.getDate() + 7);
                return gameDate >= today && gameDate <= weekFromNow;
              }).length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Completed Games</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {games.filter(game => game.status === 'COMPLETED').length}
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="upcoming" className="space-y-4">
        <TabsList>
          <TabsTrigger value="upcoming">Upcoming Games</TabsTrigger>
          <TabsTrigger value="in-progress">In Progress</TabsTrigger>
          <TabsTrigger value="completed">Completed</TabsTrigger>
        </TabsList>

        <TabsContent value="upcoming" className="space-y-4">
          <Card>
            <CardContent className="pt-6">
              <div className="w-full overflow-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="border-b">
                      <th className="px-4 py-2 text-left font-medium">Time</th>
                      <th className="px-4 py-2 text-left font-medium">Teams</th>
                      <th className="px-4 py-2 text-left font-medium">Venue</th>
                      <th className="px-4 py-2 text-left font-medium">Status</th>
                      <th className="px-4 py-2 text-left font-medium">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {games
                      .filter(game => game.status === 'SCHEDULED')
                      .map((game) => (
                        <tr key={game.id} className="border-b">
                          <td className="px-4 py-2">
                            {new Date(game.startTime).toLocaleTimeString()}
                          </td>
                          <td className="px-4 py-2">
                            {game.homeTeam} vs {game.awayTeam}
                          </td>
                          <td className="px-4 py-2">{game.venue}</td>
                          <td className="px-4 py-2">{game.status}</td>
                          <td className="px-4 py-2">
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => handleUpdateScore(game.id, game.homeScore, game.awayScore, 'IN_PROGRESS')}
                            >
                              Start Game
                            </Button>
                          </td>
                        </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}