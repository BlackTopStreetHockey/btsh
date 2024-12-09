import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useGamePlayers = ({ 
  gameId 
}: { 
  gameId: number | string
}) => {
  const { data, placeholder, ...rest } = usePlaceholder(useRequest({
    route: 'game_players',
    params: {
      game: gameId
    },
    skip: !gameId
  }));

  const players = data?.results;

  const teamToPlayers = players?.reduce((acc: any, player: GamePlayer) => {
    if (!acc[player.team.id]) acc[player.team.id] = [];
    acc[player.team.id].push(player);
    return acc;
  }, {});


  return {
    data,
    players,
    teamToPlayers,
    placeholder,
    ...rest
  }
}