import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useGameGoals = ({ 
  gameId 
}: { 
  gameId: number | string
}) => {
  const { data, placeholder, ...rest } = usePlaceholder(useRequest({
    route: 'game_goals',
    params: {
      game: gameId
    },
    skip: !gameId
  }));

  const goals = data?.results;

  const teamToGoals = goals?.reduce((acc: any, goal: GameGoal) => {
    if (!acc[goal.team.id]) acc[goal.team.id] = [];
    let per = acc[goal.team.id].find((p: any) => p.period == goal.period);
    if (!per) {
      per = { period: goal.period, goals: [] };
      acc[goal.team.id].push(per);
    }
    per.goals.push(goal);
    return acc;
  }, {});

  return {
    data,
    goals,
    teamToGoals,
    placeholder,
    ...rest
  }
}