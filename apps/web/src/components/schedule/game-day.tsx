import formatDateNoTimezone from "@/lib/dates";
import Game from "./game";

export default function GameDay({ gameDay }) {
  const eastGames = gameDay.games.filter(g => g.court === 'east');
  const westGames = gameDay.games.filter(g => g.court === 'west');
  const gameSets = [
    { label: 'West', games: westGames }, 
    { label: 'East', games: eastGames }
  ];
  return (
    <div className="p-4 border"> 
      <div className='text-lg font-bold'>{formatDateNoTimezone(gameDay.day, "eeee, MMMM do y")}</div>
      
      <div className="">
        <div className='flex flex-row justify-center'>
          <div className="flex flex-col items-start">
            <div className='flex flex-row gap-2'>
              <div className='font-bold text-sm'>Opening Team</div>
              <div className='text-sm'>{gameDay.opening_team.name}</div>
            </div>
            <div className='flex flex-row gap-2'>
              <div className='font-bold text-sm'>Closing Team</div>
              <div className='text-sm'>{gameDay.closing_team.name}</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-2">
          {gameSets.map(({ label, games }) => (
            <div key={label} className="flex flex-col items-center">
              <div className='font-bold text-sm'>{label}</div>
              {games.map(g => (
                <Game key={g.id} game={g} />
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}