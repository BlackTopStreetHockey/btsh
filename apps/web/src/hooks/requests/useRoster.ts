import { usePlaceholder, useRequest } from "@/hooks";

export const useRoster = ({ id }: { id?: string }) => {
  const { data, placeholder, loading, error, ...rest } = usePlaceholder(
    useRequest({
      route: `season-registrations/${id}`,
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
