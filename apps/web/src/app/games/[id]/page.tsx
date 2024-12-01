"use client";
import GameGoal from "@/components/games/GameGoal";
import TeamName from "@/components/teams/team-name";
import formatDateNoTimezone, { formatTime } from "@/lib/dates";
import { numberToOrdinal } from "@/lib/utils";
import { useGame } from "@/requests/hooks/useGame";
import clsx from "clsx";
import { useParams } from "next/navigation";


export default function GamePage() {
  const { id } = useParams();
  const { game, placeholder } = useGame({ id });
  console.log(game);


  if (!!placeholder) return placeholder;
  const isCompleted = game.status === 'completed';
  const homeTeamWin = game.status === 'completed' && game.winning_team_id === game.home_team.id;
  const awayTeamWin = game.status === 'completed' && game.winning_team_id === game.away_team.id;
  
  const teamToGoals = game.goals.reduce((acc: any, goal: GameGoal) => {
    if (!acc[goal.team.id]) acc[goal.team.id] = [];
    let per = acc[goal.team.id].find((p: any) => p.period == goal.period);
    if (!per) {
      per = { period: goal.period, goals: [] };
      acc[goal.team.id].push(per);
    }
    per.goals.push(goal);
    return acc;
  }, {});

  const teamToPlayers = game.players.reduce((acc: any, player: GamePlayer) => {
    if (!acc[player.team.id]) acc[player.team.id] = [];
    acc[player.team.id].push(player);
    return acc;
  }, {});

  return (
    <div className='bg-gray-50 min-h-screen'>
      <div className='flex flex-col gap-4'>

        <div className='flex flex-col items-center gap-1 bg-white pb-2 shadow'>
          <div className='flex flex-row gap-8 justify-center'>
            <div className='flex flex-row gap-2'>
              <TeamName 
                team={game.away_team} 
                className='text-2xl font-bold' 
                link={true}
              />

              {isCompleted && <div className={clsx('text-2xl', { 'font-bold': awayTeamWin })}>{game.away_team_num_goals}</div>}
              {awayTeamWin && <div className='text-2xl font-bold'>(W)</div>}
              </div>

            <div className='text-2xl'>@</div>
            
            <div className='flex flex-row gap-2'>
              <TeamName 
                team={game.home_team} 
                className='text-2xl font-bold' 
                link={true}
              />

              {isCompleted && <div className={clsx('text-2xl', { 'font-bold': homeTeamWin })}>{game.home_team_num_goals}</div>}
              {homeTeamWin && <div className='text-2xl font-bold'>(W)</div>}
            </div>
          </div>
          <div className='flex flex-col items-center gap-0'>
            <div className="text-md text-bold">
              {isCompleted ? game.get_result_display : game.get_status_display}
            </div>
            <div className="text-md">{formatDateNoTimezone(game.game_day.day, "eeee, MMMM do y")} | {formatTime(game.start.toString())}</div>
            <div className="text-md">{game.location} | {game.get_court_display} Court</div>
          </div>
        </div>

        <div className='grid md:grid-cols-2 gap-4'>

          <div className='flex flex-col items-center'>
            <div className='border p-2 bg-white'>
              <div className='text-lg font-bold bg-white'>Scoring</div>
              <div className='flex flex-row gap-8'>
                {[game.away_team.id, game.home_team.id].map((teamId) => (
                  <div className='bg-white'>
                    {teamToGoals[teamId]?.map((period: any) => (
                      <div key={period.period} className='flex flex-col gap-1 p-2 bg-white'>
                        <div className='font-bold text-sm'>{numberToOrdinal(period.period)}</div>
                        {period.goals.map((goal: GameGoal) => (
                          <GameGoal goal={goal} key={goal.id} />
                        ))}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className='flex flex-col items-center'>
            <div className='border p-2 bg-white'>
              <div className='text-lg font-bold bg-white'>Referees</div>
              {game.referees.map((referee: GameReferee) => (
                <div key={referee.id} className='flex flex-row gap-4 items-center justify-between'>
                  <div className='text-gray-400 text-xs'>{referee.type.toUpperCase()}</div>
                  <div className='text-sm'>{referee.user.full_name}</div>
                </div>
              ))}
            </div>
          </div>

        </div>
        
        <div className='flex flex-col items-center'>
          <div className='border p-2 bg-white'>
            <div className='text-lg font-bold bg-white'>Players</div>
            <div className='flex flex-row gap-8'>
              {[game.away_team.id, game.home_team.id].map((teamId) => (
                <div key={teamId} className='flex flex-col gap-1 p-2 bg-white'>
                  <div className='font-bold text-sm'>{teamToPlayers[teamId]?.length} players</div>
                  {teamToPlayers[teamId]?.map((player: GamePlayer) => (
                    <div key={player.id} className='flex flex-row gap-4 items-center justify-between'>
                      <div className='text-sm'>{player.user.full_name}</div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}