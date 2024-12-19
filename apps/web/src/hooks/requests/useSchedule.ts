import { usePlaceholder, useRequest } from "@/hooks";

export const useSchedule = ({
  seasonId = "1",
  teamId = "2",
}: {
  seasonId?: string;
  teamId?: string;
}) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: "game_days",
      params: {
        season: seasonId,
        team: teamId,
      },
    })
  );
  return {
    data,
    schedule: data?.results,
    placeholder,
    loading,
    error,
    ...rest,
  };
};
