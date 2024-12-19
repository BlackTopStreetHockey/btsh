import { usePlaceholder, useRequest } from "@/hooks";

export const useRoster = ({
  seasonId = "1",
  teamId = "2",
}: {
  seasonId?: string;
  teamId?: string;
}) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: "user-season-registrations",
      params: {
        seasons: seasonId,
        team: teamId,
      },
    })
  );
  return {
    data,
    roster: data?.results,
    placeholder,
    loading,
    error,
    ...rest,
  };
};
