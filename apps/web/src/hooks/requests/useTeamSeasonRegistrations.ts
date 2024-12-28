import { usePlaceholder, useRequest } from "@/hooks";

export const useTeamSeasonRegistrations = ({ season }) => {
  const { data, placeholder, loading, error } = usePlaceholder(
    useRequest({
      route: "team-season-registrations",
      params: {
        season
      },
      skip: !season
    }),
  );
  return {
    data,
    teams: data?.results,
    placeholder,
    loading,
    error,
  };
};
