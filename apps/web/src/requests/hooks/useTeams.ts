import { usePlaceholder, useRequest } from "@/requests/hooks";

export const useTeams = ({ short_name }: { short_name?: string }) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: short_name ? `team/${short_name}` : "teams",
    })
  );
  return {
    data,
    seasons: data?.results,
    placeholder,
    loading,
    error,
    ...rest,
  };
};
