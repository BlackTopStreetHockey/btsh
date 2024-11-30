import { usePlaceholder, useRequest } from "@/hooks";

export const useTeams = () => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: "teams",
    })
  );
  return {
    data,
    teams: data?.results,
    placeholder,
    loading,
    error,
    ...rest,
  };
};
