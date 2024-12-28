
const GamePlayerName = ({ gamePlayer, team }: { gamePlayer: GamePlayer, team: Team}) => {
  return (
    <div className="flex flex-row gap-2">
      <img className="rounded" src={team.logo} alt="" width={24} />
      <div className="text-sm">{gamePlayer.user.full_name}</div>
    </div>
  );
}

export default function GameGoal({
  goal
}: {
  goal: GameGoal
}) {
  const scorer = goal.scored_by;
  const scorerUser = scorer.user;
  return (
    <div>
      <GamePlayerName gamePlayer={goal.scored_by} team={goal.team} />      
    </div>
  )
}