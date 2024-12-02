import { usePlaceholder } from "./usePlaceholder";
import { useRequest } from "./useRequest";

export const useGameDays = ({ season }: { season: number | string }) => {
  const { data, placeholder, ...rest } = usePlaceholder(
    useRequest({
      route: "game_days",
      params: {
        season,
      },
      skip: !season,
    }),
  );
  return {
    data,
    placeholder,
    ...rest,
  };
};
