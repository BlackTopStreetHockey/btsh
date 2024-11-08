"use client";

import { Suspense, useState, useCallback, useEffect } from "react";
import { format, isSameDay } from "date-fns";
import { Calendar } from "@/components/ui/calendar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

// Types for our API response
type Game = {
  date: string;
  homeTeam: string;
  awayTeam: string;
  time: string;
};

type GameDaysResponse = {
  games: Game[];
};

// Add a cache object outside the component
const requestCache: Record<string, Promise<GameDaysResponse>> = {};

// Update the getGameDays function with caching and better error handling
async function getGameDays(
  month: number,
  year: number
): Promise<GameDaysResponse> {
  const cacheKey = `${month}-${year}`;
  
  // Return cached request if it exists
  if (await requestCache[cacheKey]) {
    return requestCache[cacheKey];
  }

  // Create the request promise
  const requestPromise = new Promise<GameDaysResponse>(async (resolve, reject) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/game_days`);
      if (!res.ok) {
        throw new Error(`Failed to fetch game days: ${res.statusText}`);
      }
      const data = await res.json();
      resolve(data);
    } catch (error) {
      console.error("Error fetching game days:", error);
      // Remove failed request from cache
      delete requestCache[cacheKey];
      reject(error);
    }
  });

  // Store in cache
  requestCache[cacheKey] = requestPromise;
  return requestPromise;
}

// Update the GameList component to handle errors gracefully
function GameList({ selectedDate }: { selectedDate: Date }) {
  const [error, setError] = useState<string | null>(null);
  const [games, setGames] = useState<Game[]>([]);

  // Use useCallback to prevent recreation of the fetch function
  const fetchGames = useCallback(async () => {
    try {
      setError(null);
      const data = await getGameDays(
        selectedDate.getMonth(),
        selectedDate.getFullYear()
      );
      setGames(data.games);
    } catch (err) {
      console.error(err);
      setError(`Unable to load games. Please try again.`);
    }
  }, [selectedDate]);

  // Use useEffect to fetch games when the date changes
  useEffect(() => {
    fetchGames();
  }, [fetchGames]);

  // Show error state if there's an error
  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>{format(selectedDate, "MMMM d, yyyy")}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-red-500">{error}</div>
          <button 
            onClick={fetchGames}
            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Retry
          </button>
        </CardContent>
      </Card>
    );
  }

  const gamesForSelectedDate = games.filter((game) =>
    isSameDay(new Date(game.date), selectedDate)
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>{format(selectedDate, "MMMM d, yyyy")}</CardTitle>
      </CardHeader>
      <CardContent>
        {gamesForSelectedDate.length > 0 ? (
          <ul className="space-y-4">
            {gamesForSelectedDate.map((game, index) => (
              <li key={index} className="flex items-center justify-between">
                <span className="font-semibold">
                  {game.homeTeam} vs {game.awayTeam}
                </span>
                <Badge variant="secondary">{game.time}</Badge>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-muted-foreground">
            No games scheduled for this date.
          </p>
        )}
      </CardContent>
    </Card>
  );
}

// Loading skeleton for GameList
function GameListSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-2/3" />
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {[1, 2, 3].map((_, index) => (
            <div key={index} className="flex items-center justify-between">
              <Skeleton className="h-4 w-1/2" />
              <Skeleton className="h-4 w-1/4" />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export default function HockeyLeagueSchedule() {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [currentMonth, setCurrentMonth] = useState(new Date());

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Hockey League Schedule</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>{format(currentMonth, "MMMM yyyy")}</CardTitle>
          </CardHeader>
          <CardContent>
            <Calendar
              mode="single"
              selected={selectedDate}
              onSelect={(date) => date && setSelectedDate(date)}
              onMonthChange={setCurrentMonth}
              className="rounded-md border"
              components={{
                day: ({ date, ...props }) => (
                  <div {...props} className={`relative ${props.className}`}>
                    {props.children}
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-blue-500 rounded-full" />
                  </div>
                ),
              }}
            />
          </CardContent>
        </Card>
        <Suspense fallback={<GameListSkeleton />}>
          <GameList selectedDate={selectedDate} />
        </Suspense>
      </div>
    </div>
  );
}
