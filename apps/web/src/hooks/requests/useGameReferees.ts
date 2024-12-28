import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";


export function useGameReferees({ gameId }: { gameId: number }) {
  const { data, error, loading, placeholder } = usePlaceholder(useRequest({
    route: 'game_referees',
    params: {
      game: gameId
    },
    skip: !gameId
  }));

  return {
    data,
    referees: data?.results,
    loading,
    error,
    placeholder,
  };
}