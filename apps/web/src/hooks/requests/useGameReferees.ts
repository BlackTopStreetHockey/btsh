import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useGameReferees = ({ 
  gameId 
}: { 
  gameId: number | string
}) => {
  const { data, placeholder, ...rest } = usePlaceholder(useRequest({
    route: 'game_referees',
    params: {
      game: gameId
    },
    skip: !gameId
  }));

  const referees = data?.results;
  
  return {
    data,
    referees,
    placeholder,
    ...rest
  }
}