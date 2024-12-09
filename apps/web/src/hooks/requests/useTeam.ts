import { usePlaceholder, useRequest } from "@/hooks";

export const useTeam = ({ short_name }: { short_name?: string }) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: `teams/${short_name}`,
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
