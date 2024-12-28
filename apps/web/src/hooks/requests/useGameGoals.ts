import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";


export function useGameGoals({ gameId }: { gameId: number }) {
  const { data, error, loading, placeholder } = usePlaceholder(useRequest({
    route: 'game_goals',
    params: {
      game: gameId
    },
    skip: !gameId
  }));

  return {
    data,
    goals: data?.results,
    loading,
    error,
    placeholder,
  };
}