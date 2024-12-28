import { useGameReferees } from "@/hooks/requests/useGameReferees";

export const GameReferees = ({ game }: { game: Game }) => {
  const { referees, placeholder } = useGameReferees({
    gameId: game.id,
  });

  if (placeholder) return placeholder;

  return (
    <div className="flex flex-col items-center">
      <div className="flex flex-row gap-8">
        {referees.map((referee: GameReferee) => (
          <div
            key={referee.id}
            className="flex flex-row gap-4 items-center justify-between"
          >
            <div className="text-gray-400 text-xs">
              {referee.type.toUpperCase()}
            </div>
            <div className="text-sm">{referee.user.full_name}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
