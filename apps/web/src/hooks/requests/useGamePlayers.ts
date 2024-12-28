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
  return {
    data,
    players: data?.results,
    placeholder,
    ...rest
  }
}